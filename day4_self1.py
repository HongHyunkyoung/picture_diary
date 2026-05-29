# day4_self1.py — Kling 영상 submit 시범 (Mock 버전)
from pathlib import Path
from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-29" / "scene_1.png"

if not IMAGE_PATH.exists():
    print(f"[오류] {IMAGE_PATH} 파일 없어요.")
    exit(1)
    
print(f"[확인] 이미지 경로: {IMAGE_PATH}")
print(f"[확인] 파일 크기: {IMAGE_PATH.stat().st_size:,} bytes")
print("[Mock] 이미지 업로드 시뮬레이션...")
image_url = f"https://mock.fal.ai/uploads/{IMAGE_PATH.name}"
print(f"[Mock] 암시 URL: {IMAGE_PATH}")

# 실제 버전:
# import fal_client
# image_url = fal_client.upload_file(str(IMAGE_PATH))

PROMPT = "slow zoom in, gentle camera movement, cinematic, soft motion"
# Kling에 제출 (Mock)
print("\n[제출] Kling에 영상 생성 작업 제출 중...")
task_id = submit_kling(image_url, PROMPT, duration=5)
print(f"[번호표] task_id: {task_id}")

# task_id를 파일로 저장
task_id_path = Path("kling_task_id.txt")
task_id_path.write_text(task_id, encoding="utf-8")
print(f"[저장 완료] {task_id_path}")

print("\n[안내] Mock 모드: 실제 영상은 생성되지 않았습니다.")
print("[안내] Day 4 self2에서 task_id로 status 폴링 구조를 만듭니다.")
print("[안내] 실제 API로 바꾸려면 agents/video.py의 MOCK = False로 변경하세요.")