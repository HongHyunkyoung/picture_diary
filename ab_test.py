import time
import statistics
from agents.image import generate_image

def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    """이미지 1회 호출에 걸린 시간을 초 단위로 반환한다."""
    start = time.perf_counter()
    generate_image(prompt=prompt, model=model, seed=seed)
    end = time.perf_counter()
    return end - start

def run_ab_test(prompt: str, n_calls: int = 3, model: str = "dalle") -> dict:
    """같은 prompt를 seed A/B로 나누어 여러 번 호출한다."""
    seed_a = 42
    seed_b = 137

    a_latencies = []
    b_latencies = []

    print(f"[A 그룹] seed={seed_a}, {n_calls}회 호출 시작...")
    for i in range(n_calls):
        elapsed = time_one_call(prompt, seed=seed_a, model=model)
        a_latencies.append(elapsed)
        print(f"  A [{i+1}/{n_calls}] {elapsed:.2f}초")

    print(f"[B 그룹] seed={seed_b}, {n_calls}회 호출 시작...")
    for i in range(n_calls):
        elapsed = time_one_call(prompt, seed=seed_b, model=model)
        b_latencies.append(elapsed)
        print(f"  B [{i+1}/{n_calls}] {elapsed:.2f}초")

    return {
        "a_latencies": a_latencies,
        "b_latencies": b_latencies,
        "seed_a": seed_a,
        "seed_b": seed_b,
    }

def compute_p95(latencies: list[float]) -> float:
    """지연 시간 목록에서 P95 값을 계산한다."""
    if not latencies:
        return 0.0

    sorted_latencies = sorted(latencies)
    idx = int(len(sorted_latencies) * 0.95)
    idx = min(idx, len(sorted_latencies) - 1)
    return sorted_latencies[idx]