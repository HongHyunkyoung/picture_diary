from pathlib import Path
import re
REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]

def load_draft(path: Path) -> str:
    """scene_draft.md를 읽어 본문을 반환."""
    return path.read_text(encoding="utf-8")

def count_scenes(text: str) -> int:
    """본문에서 '## 장면 N' 헤딩 수를 카운트."""
    matches = re.findall(r"^## 장면 \d+", text, re.M)
    return len(matches)

def check_fields(text: str, scene_idx: int) -> list[str]:
    """주어진 장면 인덱스에 빠진 필드 목록 반환."""
    pattern = rf"## 장면 {scene_idx}(.*)(?=## 장면 |\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        return ["장면 섹션 없음"]
    
    section = match.group(1)
    
    
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        if f"- {field}:" not in section:
            missing.append(field)
    return missing

if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")
    
    if n != 4:
        print(f"[경고] 장면이  4개여야 합니다. 현재: {n}개")
        
    for i in range(1, 5):
        missing = check_fields(draft, i)
        if missing:
            print(f"장면 {i}: 누락 필드-> {missing}")
        else:
            print(f"장면 {i}: OK")
    
    
    print("[완료] 모든 장면 OK이면 self2로 진랭하세요.")