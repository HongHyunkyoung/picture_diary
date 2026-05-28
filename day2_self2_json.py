import json
from pathlib import Path
REQUIRED_FIELDS = ["scene_id", "scene_kr", "shot", "angle", "lighting", "lens", "prompt_en"]
data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
scenes = data.get("scenes", [])
print(f"장면 수: {len(scenes)}")

for i, scene in enumerate(scenes, 1):
    # missng -> missing 으로 오타 수정
    missing = [f for f in REQUIRED_FIELDS if f not in scene]
    if missing:
        print(f"장면 {i} 누락 필드: {missing}")
    else:
        print(f"장면 {i} OK - shot={scene['shot']}, angle={scene['angle']}")