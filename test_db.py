from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

# .env 열기
load_dotenv()

# 환경변수에서 값 꺼내오기
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client["CTI_DB"]
    
    # 테스트 데이터 저장
    db.logs.insert_one({"status": "Connect Success!"})
    
    print("✅ MongoDB 연결 성공! 데이터가 저장되었습니다.")

except Exception as e:
    print(f"❌ 연결 실패: {e}")