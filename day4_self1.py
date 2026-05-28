# day4_self1.py — Kling 영상 submit 시범 (Mock 버전)
from pathlib import Path
from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-28" / "scene_1.png"

if not IMAGE_PATH.exists():
    print(f"[오류] {IMAGE_PATH} 파이 없어요.")
    exit(1)일
    
print(f"[확인] 이미지 경로: {IMAGE_PATH}")
print(f"[확인] 파일 크기: {IMAGE_PATH.stat().st_size:,} bytes")