from pathlib import Path
from agents.scene import extract_scenes, validate_scenes, save_scenes

diary_path = Path("diary.md")
if diary_path.exists():
    diary_text = diary_path.read_text(encoding="utf-8")
    print(f"[일기 로드] {len(diary_text)}자")
else:
    diary_text = """
    아침에 감자를 갈다가 블렌더 뚜껑을 열어서 사방에 튀겼다.
    부엌 천장에도 감자가 붙어 있었다.
    그래도 포기하지 않고 감자전을 부쳤다.
    막걸리 한 잔과 함께 먹으니 뿌듯했다.
    """
    print("[일기 로드] diary.md 없음 — 임시 일기 사용")
    
print("[1] 장면 추출 중...")
scenes = extract_scenes(diary_text)
print(f" -> {len(scenes)}개 장면 추출 완료")

print("[2] 장면 검증 중 ...")
errors = validate_scenes(scenes)
if errors:
    print(" -> 검증 실패:")
    for error in errors:
        print(f"    -{error}")
    print(" ->SYSTEM_PROMPT를 확인하고 다시 실행하세요.")
    exit(1)
else:
    print(" -> 검증 통과")
    
print("[3] scene_extracted.json 저장 중...")
save_scenes(scenes, "scene_extracted.json")
print(" -> 저장 완료")

print("[완료] Day 3 self2의 agents/image.py에서 scene_extracted.json을 입력으로 사용할 수 있어요.")