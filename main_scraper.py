import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient

# config.py에서 설정과 DB 객체를 가져옵니다
from config import API_ID, API_HASH, TARGET_CHANNEL, collection

# 텔레그램 클라이언트 생성
client = TelegramClient('my_session', API_ID, API_HASH)

async def main():
    print(f"🚀 [{TARGET_CHANNEL}] 최신 위협 정보 수집 시작(중복 제거 모드)...")
    
    # 3개월 전 날짜 계산 (UTC 기준)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)
    print(f"📅 수집 기준일: {cutoff_date.strftime('%Y-%m-%d')} 이후 데이터만 수집합니다.")

    # limit=None으로 설정 (개수 제한 없이 날짜로 끊기)
    async for message in client.iter_messages(TARGET_CHANNEL, limit=None):
        
        # 1. 날짜 확인: 3개월 이전 글이면 종료
        if message.date < cutoff_date:
            print("🛑 3개월치 데이터 수집 완료! 루프를 종료합니다.")
            break

        # 2. 텍스트 없으면 건너뛰기
        if not message.text:
            continue      
            
        # 3. 텔레그램 공유(Forward) 정보 안전하게 추출하기
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

        # 4. 저장할 데이터 뭉치 만들기 (Dictionary)
        doc = {
            "channel_name": TARGET_CHANNEL,
            "message_id": message.id,
            "date": message.date,          # 글 쓴 시간 (UTC)
            "text": message.text,          # 원문 (러시아어)
            "text_translated": None,       # [추가 1] 번역본 (나중에 채울 공간)
            "views": message.views,        # [추가 2] 조회수 (영향력 측정용)
            "is_forwarded": bool(message.fwd_from), # [추가 3] 공유글 여부 (True/False)
            "forward_from": forward_info,  # [추가 4] 공유 출처
            "url": f"https://t.me/{TARGET_CHANNEL}/{message.id}",
            "crawled_at": datetime.now(timezone.utc) # [추가 5] 수집된 시점
        }

        # 5. 몽고DB에 저장
        try:
            # 중복이면 덮어쓰고(Update), 없으면 새로 저장(Insert)
            result = collection.update_one(
                {"message_id": message.id, "channel_name": TARGET_CHANNEL}, 
                {"$set": doc}, 
                upsert=True
            )

            if result.upserted_id:
                print(f"🆕 [신규] {message.id}번 게시물 저장 완료")
            else:
                print(f"♻️ [중복] {message.id}번은 이미 있어서 갱신함")

        except Exception as e:
            print(f"⚠️ 저장 에러: {e}")

        # 봇 탐지 방지 (1초 휴식)
        await asyncio.sleep(1.0)
        
    print("\n🎉 모든 작업이 끝났습니다!")

# 프로그램 실행
with client:
    client.loop.run_until_complete(main())