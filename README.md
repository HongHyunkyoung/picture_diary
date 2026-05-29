\# 그림일기 (Picture Diary) — 멀티 LLM 파이프라인



일기 텍스트를 입력하면 GPT가 장면을 추출하고

이미지 모델이 4장면을 자동 생성하는 멀티 LLM 파이프라인입니다.



\---



\## 빠른 시작



```bash

uv venv --python 3.11

.venv\\Scripts\\activate

uv pip install -r requirements.txt



\# .env 설정

\# OPENAI\_API\_KEY=sk-...



python pipeline.py

```



\---



\## 결과 미리보기



<!-- 대표 이미지 1장 경로 입력 -->

<img width="500" height="500" alt="대표 이미지" src="https://github.com/user-attachments/assets/07ac804f-dd3c-4db0-8ea8-0a0f8011a1f3" />
<!-- outputs/ 폴더가 .gitignore에 포함된 경우 아래처럼 설명 -->

로컬 실행 시 `outputs/{날짜}/` 폴더에 scene\_1.png \~ scene\_4.png가 생성됩니다.



\---



\## 운영 지표



<!-- cost\_report.md에서 가져온 값 -->

| Day | 주요 작업 | 호출 수 | 합계 |

|---|---|---:|---:|

| Day 1 | 환경 확인 + 첫 호출 | 1 | \~$0.04 |

| Day 2 | fal.ai 첫 호출 | 1 | \~$0.003 |

| Day 3 | 이미지 4장 생성 | 4 | \~$0.16 |

| Day 4 | Mock 영상 | 0 | $0 |

| Day 5 | 도메인 A/B 테스트 | 6 | \~$0.24 |



\## A/B 테스트 요약



<!-- ab\_test\_results.json에서 가져온 값 -->

| 그룹 | seed | P95 지연 |

|---|---:|---:|

| A | 42 | (p95\_a 값)초 |

| B | 137 | (p95\_b 값)초 |



\---



\## 도메인 응용



선택 도메인: \*\*product (제품 카탈로그)\*\*



| 항목 | 값 |

|---|---|

| shot | close-up |

| lighting | studio lighting |

| mood | clean, professional |



\---



\## 파일 구조

picture\_diary/

├── pipeline.py          # 전체 파이프라인 진입점

├── agents/

│   ├── scene.py         # 일기 → 장면 JSON 추출

│   ├── image.py         # 장면 → 이미지 생성

│   └── video.py         # 이미지 → 영상 생성 (Mock)

├── domains/

│   └── product\_prompts.json

├── cost\_report.md

└── ab\_test\_results.json



\---



\## 보안



\- API 키는 `.env`에만 저장합니다

\- `.env`는 `.gitignore`에 등록되어 있습니다

\- 코드에 키를 직접 쓰지 않습니다



\---



\## 라이선스



MIT

