import time
import requests
from pathlib import Path
from datetime import date

from agents.video import status_kling, result_kling
from guardrails import (
    check_max_iter,
    check_timeout,
    check_predicate,
    check_budget,
)

task_id = Path("kling_task_id.txt").read_text(encoding="utf-8").strip()
print(f"[task_id] {task_id}")

if not task_id:
    print("[오류] kling_task_id.txt가 비어있어요. Day 4 self1을 먼저 완료하세요.")
    exit(1)

print("\n[폴링 시작] status 확인 중...")
iteration = 0
start_ts = time.time()
status = ""

while True:
    if not (check_max_iter(iteration) and check_timeout(start_ts)):
        print(f"[가드 발동] 중단 — iteration={iteration}, elapsed={time.time()-start_ts:.1f}초")
        break

    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")

    if check_predicate(status):
        print("[완료] 영상 생성 완료 판정")
        break

    iteration += 1
    time.sleep(1) 

print(f"\n[폴링 종료] 최종 status: {status}, 총 {iteration}회 조회")

if check_predicate(status):
    print("\n[영상 수신] result_kling() 호출...")
    video_url = result_kling(task_id)
    print(f"[영상 URL] {video_url}")

    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / "scene_1.mp4"

    video_path.write_text(f"[Mock] video from {video_url}")
    print(f"[저장 완료] {video_path}")
    print("[안내] Mock 모드: 실제 mp4가 아닌 텍스트 파일로 저장됨")

    # 실제 버전:
    # response = requests.get(video_url, timeout=60)
    # response.raise_for_status()
    # video_path.write_bytes(response.content)

else:
    print("[안내] 영상이 완료되지 않았어요. 폴링 가드가 먼저 발동됐습니다.")
    video_path = None