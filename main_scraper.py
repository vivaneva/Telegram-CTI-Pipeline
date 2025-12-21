import asyncio
from telethon import TelegramClient
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

# 1. .env 열기
load_dotenv()

# ======================================================
# 설정 정보 (환경변수에서 가져오기)
# ======================================================
api_id = int(os.getenv("API_ID")) # 숫자로 바꿔주기
api_hash = os.getenv("API_HASH")
mongo_uri = os.getenv("MONGO_URI")
target_channel = 'BleepingComputer'
# ======================================================

# 2. 몽고DB 연결
try:
    db_client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    db = db_client["CTI_DB"]      # DB 이름
    collection = db["telegram_logs"] # 데이터를 넣을 Collection 이름
    print("✅ MongoDB 연결 성공!")
except Exception as e:
    print(f"❌ DB 연결 실패: {e}")
    exit() # DB 안 되면 프로그램 종료

# 3. 텔레그램 클라이언트 생성
client = TelegramClient('my_session', api_id, api_hash)

async def main():
    print(f"🚀 [{target_channel}] 데이터 수집을 시작합니다.")
    
    # 최근 글 20개 긁어오기 (테스트용)
    # reverse=True: 과거 -> 현재 순서로 저장
    async for message in client.iter_messages(target_channel, limit=20, reverse=True):
        
        # 1. 내용이 없으면(사진만 있으면) 패스
        if not message.text:
            continue
            
        # 2. 저장할 데이터 뭉치 만들기 (Dictionary)
        doc = {
            "channel_name": target_channel,     # 채널명
            "message_id": message.id,           # 메시지 고유 번호
            "date": message.date,               # 작성 시간
            "text": message.text,               # 본문 내용
            "url": f"https://t.me/{target_channel}/{message.id}" # 게시글 링크
        }

        # 3. 몽고DB에 저장 (중복 방지 로직은 나중에 추가)
        try:
            # 같은 메시지 ID가 있어도 일단은 무조건 저장(insert)
            collection.insert_one(doc)
            print(f"💾 저장 완료: {message.id}번 게시물")
        except Exception as e:
            print(f"⚠️ 저장 에러: {e}")

    print("\n🎉 모든 작업이 끝났습니다!")

# 프로그램 실행
with client:
    client.loop.run_until_complete(main())