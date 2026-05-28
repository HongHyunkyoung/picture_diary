import json
from pathlib import Path
from datetime import date
from agents.image import batch_generate

MODEL = "dalle"

scene_path = Path("scene_extracted.json")
if not scene_path.exists():
    print("[오류] scene_extracted.json이 없습니다.")
    exit(1)
    
data = json.loads(scene_path.read_text(encoding="utf-8"))
scenes = data["scenes"]
print(f"[로드] {len(scenes)}개 장면 확인")

today = date.today().isoformat()
out_dir = Path("outputs") / today
out_dir.mkdir(parents=True, exist_ok=True)
print(f"[폴더] {out_dir}")

print(f"\n[시작] {MODEL} 모델로 {len(scenes)}장 생성합니다.")
saved = batch_generate(scenes[:4], model=MODEL, out_dir=out_dir)

print(f"\n[완료] {len(saved)}장 저장됨")
for path in saved:
    print(f"    - {path}")