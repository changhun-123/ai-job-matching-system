# DEV_LOG

## 2026-04-15

### 작업 내용

* VS Code 기반 Python 개발 환경 설정
* 가상환경(venv) 생성 및 패키지 설치
* SQLite 기반 DB 구조 설계
* mock crawler 데이터를 raw_jobs 테이블에 저장하는 파이프라인 구축
* GitHub repository 생성 및 초기 코드 업로드
* Saramin 검색 결과 페이지 기반 실제 공고 리스트 크롤링 테스트
* test_crawler.py를 통해 공고 40건 수집 확인
* 수집 결과를 jobs_preview.csv로 저장해 데이터 구조 확인

### 문제

* Python 실행 환경이 제대로 잡히지 않아 명령어가 동작하지 않았음
* PowerShell에서 activate 스크립트 실행이 막힘
* database.py와 mock 데이터의 key 이름이 달라 KeyError 발생
* Git push 과정에서 remote branch와 충돌 발생
* requests 설치 후에도 다른 Python 인터프리터로 실행되어 모듈을 찾지 못하는 문제 발생

### 해결

* Python 설치 및 PATH 설정 후 VS Code에서 정상 실행 환경 구성
* ExecutionPolicy 설정 변경으로 venv 활성화 해결
* raw_jobs 기준 컬럼명을 site, title, company, deadline, url, job_text로 통일
* 기존 jobs.db 삭제 후 schema.sql 기준으로 DB 재생성
* Git pull 및 merge commit 후 GitHub push 완료
* VS Code 인터프리터를 venv 기준으로 맞추고 python test_crawler.py로 실행 방식 통일

### 배운 점

* 크롤링/DB/실행 환경 문제는 코드보다 “구조와 일관성”이 중요함
* SQLite는 파일을 직접 여는 방식이 아니라 쿼리로 확인해야 함
* Git은 덮어쓰기가 아니라 변경사항을 병합하는 도구라는 점을 이해함
* 실제 크롤링은 리스트 페이지와 상세 페이지를 분리해서 접근해야 함

### 현재 상태

* mock 데이터 기반 DB 저장 파이프라인 완료
* Saramin 검색 결과 리스트 크롤링 성공
* GitHub 버전 관리 완료

### 다음 할 일

* Saramin 상세 페이지 크롤링으로 job_text 본문 확보
* LLM 기반 공고 분석 기능 연결
* 개인 프로필과의 적합도 매칭 로직 고도화

## 2026-04-16

### 작업 내용

* DB 접근 모듈을 `config/database.py` 기준으로 통일
* Streamlit 앱이 `db/database.py` 대신 `config/database.py`를 사용하도록 변경
* Saramin 크롤러를 개선해 리스트 수집 후 상세 페이지 본문(`job_text`) 추출 기능 추가
* 메인 실행 흐름에서 mock + Saramin 크롤링 결과를 모두 `raw_jobs`에 저장하도록 확장
* `test_crawler.py`에서 CSV 저장뿐 아니라 SQLite `raw_jobs` 저장까지 수행하도록 보완

### 확인 사항

* Saramin 상세 페이지 접근 실패 시에도 fallback 텍스트(공고 제목)로 저장되도록 처리
* `INSERT OR IGNORE`를 유지해 동일 URL 중복 저장 방지

### 다음 할 일

* Saramin 상세 페이지 구조 변경에 대비한 selector 다중화/검증 로직 고도화
* `analyzed_jobs`, `matched_jobs`까지 실제 DB 적재 파이프라인 연결
