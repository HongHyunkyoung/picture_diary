\# 그림일기 프로젝트 — 5일 결과 회고



\## Day별 핵심 산출물



| Day | 주요 작업 | 핵심 파일 | 완료 |

|---|---|---|:---:|

| Day 1 | 환경 설정 + DALL-E 첫 호출 | day1\_self1.py | ✅ |

| Day 2 | 장면 JSON + fal.ai 첫 호출 | scene\_prompts.json | ✅ |

| Day 3 | 자동 장면 추출 + 이미지 4장 | agents/scene.py, agents/image.py | ✅ |

| Day 4 | 비동기 폴링 구조 (Mock) | agents/video.py, pipeline.py | ✅ |

| Day 5 | 도메인 응용 + A/B 테스트 | ab\_test.py, cost\_report.md | ✅ |



\## 잘 된 점



<!-- 구체적인 파일명이나 수치와 함께 작성 -->

\- pipeline.py로 장면 추출 → 이미지 생성 → 영상 제출 흐름을 하나로 묶었다

\- Mock 패턴으로 비용 없이 비동기 폴링 구조를 완성했다

\- A/B 테스트로 P95 지연을 측정하고 운영 지표를 문서화했다



\## 개선할 점



<!-- 측정 가능한 목표로 작성 -->

\- P95 지연이 15초 → 프롬프트 최적화로 10초 이하 목표

\- COMMON\_STYLE 조정으로 4장 이미지 일관성 개선 필요

\- fal.ai Wan 모델로 전환해 비용을 $0.04 → $0.005로 줄이기



\## 다음 주 시도할 것



\- 도메인 JSON을 여행 블로그로 확장

\- GitHub Actions로 pipeline.py 자동 실행 CI 추가

\- 실제 Kling API로 전환 (MOCK = False)



\## GitHub 저장소



https://github.com/HongHyunkyoung/picture\_diary\_

