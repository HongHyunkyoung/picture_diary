# 🎨 그림일기 (Picture Diary) — 멀티 LLM 파이프라인

> **일기 텍스트 → 장면 추출 → 이미지 자동 생성**  
> GPT와 이미지 생성 AI를 연결한 멀티 LLM 파이프라인 미니 프로젝트

---

## 결과 미리보기

<img width="500" height="500" alt="대표 이미지" src="https://github.com/user-attachments/assets/07ac804f-dd3c-4db0-8ea8-0a0f8011a1f3" />

로컬 실행 시 `outputs/{날짜}/` 폴더에 scene_1.png ~ scene_4.png가 생성됩니다.

---

## 📌 프로젝트 개요

하루의 일기를 텍스트로 입력하면, GPT가 핵심 장면을 자동으로 추출하고
이미지 생성 모델이 4컷 그림일기를 만들어주는 자동화 파이프라인입니다.

- **기간**: 2025년 (AI 부트캠프 5일 미니 프로젝트)
- **목적**: 멀티 LLM 파이프라인 설계 및 구현 학습
- **결과물**: 일기 입력 → 4장면 이미지 자동 생성

---

## 🔧 주요 기능

| 기능 | 설명 |
|------|------|
| 장면 추출 | GPT가 일기 텍스트에서 핵심 장면 4개를 JSON으로 추출 |
| 이미지 생성 | fal.ai 이미지 모델로 장면별 이미지 자동 생성 |
| 도메인 적용 | 제품 카탈로그(product) 도메인 특화 프롬프트 적용 |
| A/B 테스트 | seed 값(42 vs 137)에 따른 생성 결과 비교 실험 |
| 비용 추적 | API 호출 비용 일별 기록 및 리포트 생성 |

---

## 🏗 아키텍처

```
일기 텍스트 입력
      ↓
[scene.py] GPT — 장면 4개 추출 (JSON)
      ↓
[image.py] fal.ai — 장면별 이미지 생성
      ↓
[video.py] 영상 생성 (Mock)
      ↓
outputs/{날짜}/scene_1.png ~ scene_4.png
```

### 모듈 구조
```
picture_diary/
├── pipeline.py          # 전체 파이프라인 진입점
├── agents/
│   ├── scene.py         # 일기 → 장면 JSON 추출
│   ├── image.py         # 장면 → 이미지 생성
│   └── video.py         # 이미지 → 영상 생성 (Mock)
├── domains/
│   └── product_prompts.json   # 도메인 특화 프롬프트
├── ab_test.py           # A/B 테스트 실험
├── cost_report.md       # API 비용 리포트
└── ab_test_results.json # A/B 테스트 결과
```

---

## 📊 개발 일지 & 학습 기록

| Day | 주요 작업 | 핵심 학습 |
|-----|-----------|-----------|
| Day 1 | 환경 설정, OpenAI API 첫 호출 | API 키 관리, 기본 호출 구조 |
| Day 2 | fal.ai 이미지 생성 첫 연동 | 멀티모달 API 연결 방법 |
| Day 3 | 4장면 자동 생성 파이프라인 완성 | JSON 구조화 출력, 파이프라인 설계 |
| Day 4 | Mock 영상 생성 모듈 구현 | 모듈화 및 Mock 테스트 전략 |
| Day 5 | 도메인 적용 + A/B 테스트 설계 | 프롬프트 엔지니어링, 실험 설계 |

---

## 🧪 A/B 테스트

seed 값에 따른 이미지 생성 결과 차이를 실험적으로 비교했습니다.

| 그룹 | seed | 목적 |
|------|------|------|
| A | 42 | 기준 그룹 |
| B | 137 | 비교 그룹 |

---

## 💰 API 비용 추적

| Day | 주요 작업 | 예상 비용 |
|-----|-----------|-----------|
| Day 1 | 환경 확인 + 첫 호출 (1회) | ~$0.04 |
| Day 2 | fal.ai 첫 호출 (1회) | ~$0.003 |
| Day 3 | 이미지 4장 생성 (4회) | ~$0.16 |
| Day 4 | Mock 영상 (API 호출 없음) | $0 |
| Day 5 | 도메인 A/B 테스트 (6회) | ~$0.24 |

---

## 🛠 기술 스택

| 분류 | 사용 기술 |
|------|-----------|
| 언어 | Python 3.11 |
| LLM | OpenAI GPT (장면 추출) |
| 이미지 생성 | fal.ai |
| 패키지 관리 | uv |
| 데이터 직렬화 | JSON |
| 환경 변수 | python-dotenv |

---

## 🚀 실행 방법

```bash
# 환경 설정
uv venv --python 3.11
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 패키지 설치
uv pip install -r requirements.txt

# .env 파일 생성
OPENAI_API_KEY=sk-...

# 실행
python pipeline.py
```

---

## 🔒 보안

- API 키는 `.env`에만 저장
- `.env`는 `.gitignore`에 등록되어 코드에 직접 노출되지 않음

---

## 💡 배운 점 & 회고

- 단순 API 호출을 넘어 **멀티 LLM 파이프라인 설계** 경험
- agents/ domains/ 구조로 **모듈화**하여 유지보수성 향상
- A/B 테스트로 **실험적 사고방식** 적용
- API 비용을 일별로 추적하며 **운영 관점** 학습

> 📝 상세 개발 회고: [week7_retrospective.md](./week7_retrospective.md)
