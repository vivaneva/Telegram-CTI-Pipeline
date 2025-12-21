# 🕵️‍♂️ Telegram Threat Intelligence Scraper (CTI)

텔레그램 내 위협 정보(Threat Intel) 채널을 모니터링하여 데이터를 수집하고, 
MongoDB에 적재하는 자동화 파이프라인입니다.

## 🚀 Key Features
- **Real-time Monitoring**: 특정 타겟 채널의 게시글 실시간 수집
- **ETL Pipeline**: Python(Telethon) -> Data Cleaning -> MongoDB Atlas 적재
- **Duplication Check**: `update_one(upsert=True)`를 활용한 데이터 중복 방지 로직 구현
- **Security**: `.env`를 활용한 민감 정보(API Key) 분리 및 관리

## 🛠 Tech Stack
- **Language**: Python 3.12
- **Library**: Telethon, Pymongo, Python-dotenv
- **Database**: MongoDB Atlas (Cloud)

## ⚠️ Disclaimer
이 프로젝트는 사이버 보안 연구 및 학습 목적으로 개발되었습니다.
수집된 데이터는 분석 목적으로만 사용됩니다.