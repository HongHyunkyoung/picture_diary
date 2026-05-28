from pathlib import Path
seed = Path("scene_draft_seed.md")
if seed.exists():
    print(seed.read_text(encoding="utf-8")[:500])
else:
    print("scene_draft_seed.md 없음 — Day 1 self2 산출물을 확인하세요.")
