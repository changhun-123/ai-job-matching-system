# AI Job Matching System (MVP)

## 📌 Overview

채용공고 데이터를 수집하고, 이를 분석하여 개인 프로필과의 적합도를 평가하는 AI 기반 시스템입니다.

데이터 수집부터 분석, 추천까지의 전체 흐름을 직접 구현하며
데이터 기반 서비스 설계 역량을 강화하는 것을 목표로 했습니다.

---

## ⚙️ Tech Stack

* Python
* SQLite
* Pandas
* Streamlit (예정)
* LLM (예정)

---

## 🏗️ System Architecture

```text
Crawler → Data Processing → Database → Analysis → Matching → UI
```

---

## 🚀 Features

### 1. 채용공고 수집

* Mock crawler를 활용한 데이터 수집
* 추후 실제 크롤링으로 확장 가능

### 2. 데이터 저장

* SQLite 기반 데이터베이스 설계 및 구축
* raw_jobs 테이블에 공고 저장

### 3. 데이터 파이프라인 구축

* 수집 → 저장 → 조회까지 자동화

---

## 📂 Project Structure

```
ai-job-matching-system/
├── crawler/        # 채용공고 수집
├── config/         # DB 및 설정
├── ai/             # 분석 및 매칭 로직
├── app/            # UI (Streamlit)
├── data/           # 데이터 파일
├── main.py         # 실행 파일
```

---

## 🔜 Future Work

* LLM 기반 공고 분석 기능 추가
* 개인 맞춤 추천 알고리즘 고도화
* Streamlit 기반 UI 구축
* 실제 채용공고 크롤링 적용

---

## 💡 What I Learned

* 데이터 수집부터 저장까지의 전체 흐름 설계
* SQLite 기반 데이터 관리
* 프로젝트 구조 설계 및 GitHub 관리

---

## 🧑‍💻 Author

Changhoon Shin
