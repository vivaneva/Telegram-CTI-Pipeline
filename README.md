# 🕵️‍♂️ Telegram Threat Intelligence Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb&logoColor=white)
![Telegram](https://img.shields.io/badge/Telethon-API-2CA5E0?logo=telegram&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Webhook-5865F2?logo=discord&logoColor=white)

## 📌 Project Overview
**러시아 핵티비스트 그룹(UserSec 등)의 텔레그램 채널을 실시간으로 감시하고 분석하는 CTI 자동화 시스템**입니다. <br>
과거 데이터 수집부터 저장, 자동 번역, 그리고 위험 키워드 실시간 알림 기능까지의 전 과정을 자동화했습니다.

> **Target:** UserSec (Russian Hacktivist Group) <br>
> **Goal:** 잠재적인 한국 대상 사이버 위협(DDoS, Deface)을 조기에 탐지하고 대응 시간을 단축한다.

## 🚀 Key Features
### 1. Data Collection & Engineering
- **Batch Scraping (`main_scraper.py`):** 과거 90일간의 메시지를 수집하여 MongoDB에 적재.
- **Real-time Monitoring (`realtime_monitor.py`):** 24시간 가동되며 새로운 위협 정보를 실시간으로 수집.
- **Idempotency (중복 방지):** 서비스 재시작 시 중복 알림/중복 저장을 방지하는 로직 구현.

### 2. Natural Language Processing (NLP)
- **Auto Translation (`translator.py`):** 수집된 러시아어`Ru` 데이터를 한국어`Kr`로 자동 번역하여 분석 가독성 확보.
- **Incremental Processing:** 미번역된 데이터만 선별하여 처리함으로써 API 효율성 극대화.

### 3. Alerting & Dissemination
- **Keyword Filtering:** `Korea`, `DDoS`, `Attack` 등 고위험 키워드 탐지.
- **Discord Integration:** 위협 감지 시 Discord Webhook을 통해 즉시 알림 발송 (UTC -> AEST 시간 변환 적용).
- **OpSec Safety:** 수집용 계정 `텔레그램`과 알림용 채널 `디스코드`를 분리하여 운영 보안(OpSec) 확보.

## 🛠️ Tech Stack & Environment
- **Language:** Python 3.12
- **Database:** MongoDB Atlas (NoSQL)
- **Libraries:**
  - `Telethon` (Telegram API Client)
  - `Pymongo` (DB Connector)
  - `Deep-translator` (Translation)
  - `Requests` (Discord Webhook)

## 📂 Project Structure
```bash
CTI_Project/
├── config.py             # 환경 변수 및 DB 연결 설정 (Centralized Config)
├── main_scraper.py       # 과거 데이터 배치 수집 모듈
├── realtime_monitor.py   # 실시간 위협 감지 및 알림 봇
├── translator.py         # 러시아어 -> 한국어 자동 번역 모듈
├── requirements.txt      # 프로젝트 의존성 라이브러리 목록
├── .env                  # API Key 및 민감 정보 (Git 제외)
├── .gitignore            # 보안 설정 (Session, Pycache 제외)
└── README.md             # 프로젝트 문서
```

## ⚠️ Disclaimer
이 프로젝트는 사이버 보안 연구 및 학습 목적으로 개발되었습니다. <br>
수집된 데이터는 분석 목적으로만 사용됩니다.