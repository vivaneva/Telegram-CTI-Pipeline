import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient

# config.py에서 설정과 DB 객체를 가져오기
from config import API_ID, API_HASH, TARGET_CHANNEL, collection

# 텔레그램 클라이언트 생성
client = TelegramClient('my_session', API_ID, API_HASH)

async def save_message(message):

    # 1. 텔레그램 전달(Forward) 정보 안전하게 추출
        forward_info = None
        try:
            if message.fwd_from:
                # 경우1: 채널이나 유저 ID가 있는 경우 (from_id)
                if getattr(message.fwd_from, 'from_id', None):
                    forward_info = str(message.fwd_from.from_id) # 전체 정보 문자열로 저장
                # 경우2: 숨겨진 유저 이름만 있는 경우 (from_name)
                elif getattr(message.fwd_from, 'from_name', None):
                    forward_info = message.fwd_from.from_name
        except Exception:
            # 여기서 에러 발생하면 멈추지 않고 None으로 둠
            forward_info = "Unknown_Forward"

        # 2. 데이터 문서 생성
        doc = {
            "channel_name": TARGET_CHANNEL,
            "message_id": message.id,
            "date": message.date,          # 글 쓴 시간 (UTC)
            "text": message.text,          # 원문 (러시아어)
            "text_translated": None,       # 번역본 (translator.py)
            "views": message.views,        # 조회수 (영향력 측정용)
            "is_forwarded": bool(message.fwd_from), # 공유글 여부 (True/False)
            "forward_from": forward_info,  # 공유 출처
            "url": f"https://t.me/{TARGET_CHANNEL}/{message.id}",
            "crawled_at": datetime.now(timezone.utc) # 수집된 시점
        }

        # 3. 몽고DB에 저장 (Upsert)
        try:
            result = collection.update_one(
                {"message_id": message.id, "channel_name": TARGET_CHANNEL}, 
                {"$set": doc}, 
                upsert=True
            )
            if result.upserted_id:
                print(f"🆕 [신규] {message.id}번 게시물 저장 완료 ({message.date.date()})")
            else:
                print(f"♻️ [중복] {message.id}번 데이터 갱신 완료")

        except Exception as e:
            print(f"⚠️ 저장 에러: {e}")

async def main():
    print(f"🚀 [{TARGET_CHANNEL}] 데이터 수집 시작...")

    # limit=None으로 설정 (개수 제한 없이 수집)
    async for message in client.iter_messages(TARGET_CHANNEL, limit=None, reverse=True):

        # 텍스트 없으면 건너뛰기
        if not message.text:
            continue      
            
        await save_message(message)
        await asyncio.sleep(1.0) # 1초 휴식
        
    print("\n🎉 수집 작업이 끝났습니다!")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())