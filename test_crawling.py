from telethon import TelegramClient

# ------------------------------------------------------
# [내 정보 입력]
# ------------------------------------------------------
api_id = 1234567             # 본인 api_id
api_hash = 'MY_SECRET_KEY'    # 본인 api_hash
target_channel = 'BleepingComputer' 
# ------------------------------------------------------

# 클라이언트 생성
client = TelegramClient('my_session', api_id, api_hash)

async def main():
    print(f"[{target_channel}] 채널 접속 성공! 데이터 수집을 시작합니다.\n")
    
    # 최신 글 1개 가져오기
    async for message in client.iter_messages(target_channel, limit=1):
        print("--------------------------------------")
        print(f"📅 날짜: {message.date}")
        print(f"💬 내용: {message.text}")
        print("--------------------------------------")
        print("✅ Python 3.12 환경에서 완벽하게 작동합니다!")

# 프로그램 실행
with client:
    client.loop.run_until_complete(main())