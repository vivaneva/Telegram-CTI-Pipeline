import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient, errors
import certifi

# 1. 환경 변수 로드
load_dotenv()

# ======================================================
# [설정] 환경 변수 및 상수 (Centralized Config)
# ======================================================
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    MONGO_URI = os.getenv("MONGO_URI")
    
    # ★ 타겟 채널을 여기서 한 번만 바꾸면 모든 코드에 적용됩니다.
    TARGET_CHANNEL = 'usersecc'

except TypeError:
    print("❌ 오류: .env 파일 설정이 잘못되었습니다. (API_ID는 숫자여야 함)")
    sys.exit(1)

# ======================================================
# [공통] MongoDB 연결 객체 생성 (Singleton Pattern)
# ======================================================
def get_db_collection():
    """DB 연결 객체를 반환하는 공통 함수"""
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client["CTI_DB"]
        collection = db["telegram_logs"]
        return collection
    except errors.ConnectionFailure as e:
        print(f"❌ DB 연결 실패: {e}")
        sys.exit(1)

# 다른 파일에서 이 변수를 import해서 씁니다.
collection = get_db_collection()