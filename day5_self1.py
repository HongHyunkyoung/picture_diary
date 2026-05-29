import json
from pathlib import Path
from ab_test import compute_p95, run_ab_test

BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "product"  
N_CALLS = 3 
MODEL = "dalle"

def main() -> None:

    # ─── Step 1. 도메인 프롬프트 JSON 로드 ───────────────────
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"

    if not domain_path.exists():
        print(f"[오류] {domain_path} 파일이 없어요.")
        exit(1)

    data = json.loads(domain_path.read_text(encoding="utf-8"))
    scenes = data["scenes"]

    # 첫 번째 장면 사용
    scene = scenes[0]
    diary_sentence = scene["diary_sentence"]
    prompt_addons = ", ".join(scene["prompt_addons"])
    prompt_style = data["prompt_style"]

    # 프롬프트 조합
    prompt = (
    f"{scene['visual_focus']}, "
    f"{prompt_style['shot']}, "
    f"{prompt_style['angle']}, "
    f"{prompt_style['lighting']}, "
    f"{prompt_addons}, "
    f"{prompt_style['mood']}"
    )
    print(f"[도메인] {DOMAIN_NAME}")
    print(f"[장면] {diary_sentence}")
    print(f"[프롬프트] {prompt[:80]}...")

    # ─── Step 2. A/B 실행 + P95 계산 ────────────────────────
    print(f"\n[A/B 테스트] {N_CALLS}회씩 호출 시작...")
    ab_result = run_ab_test(prompt, n_calls=N_CALLS, model=MODEL)

    a_latencies = ab_result["a_latencies"]
    b_latencies = ab_result["b_latencies"]

    p95_a = compute_p95(a_latencies)
    p95_b = compute_p95(b_latencies)

    print(f"\n[결과] A P95: {p95_a:.2f}초 / B P95: {p95_b:.2f}초")

    # ─── Step 3. ab_test_results.json 저장 ──────────────────
    result_path = BASE_DIR / "ab_test_results.json"
    result_data = {
        "domain": DOMAIN_NAME,
        "prompt": prompt,
        "seed_a": ab_result["seed_a"],
        "seed_b": ab_result["seed_b"],
        "n_calls": N_CALLS,
        "a_latencies": a_latencies,
        "b_latencies": b_latencies,
        "p95_a": round(p95_a, 3),
        "p95_b": round(p95_b, 3),
    }
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    print(f"[저장] {result_path}")

    # ─── Step 4. cost_report.md 작성 ────────────────────────
    report_path = BASE_DIR / "cost_report.md"
    p95_max = max(p95_a, p95_b)
    cost_per_image = 0.04   # gpt-image-1 standard 기준 (본인 모델로 수정)
    total_images = N_CALLS * 2
    today_cost = cost_per_image * total_images

    report = f"""# 그림일기 파이프라인 5일 누적 비용 보고서

## 기본 정보

| 항목 | 값 |
|---|---|
| 작성 세션 | Day 5 self1 |
| 선택 도메인 | {DOMAIN_NAME} |
| A seed | {ab_result['seed_a']} |
| B seed | {ab_result['seed_b']} |
| A/B 호출 수 | A {N_CALLS}회 / B {N_CALLS}회 |

## 5일 누적 비용

| Day | 주요 작업 | 호출 수 | 단가 | 합계 |
|---|---|---:|---:|---:|
| Day 1 | 환경 확인 + 첫 호출 | 1 | ~$0.04 | ~$0.04 |
| Day 2 | fal.ai FLUX 첫 호출 | 1 | ~$0.003 | ~$0.003 |
| Day 3 | 이미지 4장 자동 생성 | 4 | ~$0.04 | ~$0.16 |
| Day 4 | Mock 영상 (비용 없음) | 0 | $0 | $0 |
| Day 5 self1 | 도메인 A/B 테스트 | {total_images} | ~${cost_per_image} | ~${today_cost:.3f} |
| 합계 |  | {6 + total_images} |  | ~${0.04 + 0.003 + 0.16 + today_cost:.3f} |

## P95 지연

| 그룹 | seed | 호출 수 | P95 지연 |
|---|---:|---:|---:|
| A | {ab_result['seed_a']} | {N_CALLS} | {p95_a:.2f}초 |
| B | {ab_result['seed_b']} | {N_CALLS} | {p95_b:.2f}초 |

## README로 옮길 값

| 항목 | 값 |
|---|---:|
| p95_latency_s | {p95_max:.2f} |
| cost_per_image | ${cost_per_image} |
| total_cost_usd | ~${0.04 + 0.003 + 0.16 + today_cost:.3f} |
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"[저장] {report_path}")
    print("\n[완료] Day 5 self1 종료")


if __name__ == "__main__":
    main()