import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """
당신은 일기 텍스트를 분석하여 그림 4장면을 추출하는 어시스턴트입니다.
출력은 반드시 JSON 객체여야 하며 다음 스키마를 따르세요:
{
  "scenes": [
    {
      "scene_id": int,
      "scene_kr": "한국어 1줄 장면 설명",
      "prompt_en": "영문 이미지 프롬프트 1줄 (샷·앵글·조명·스타일 포함)"
    }
  ]
}
반드시 4개 장면을 추출하세요.
prompt_en은 반드시 영어로 작성하세요. (prompt_en must be written in English)
wide shot/medium shot/close-up 중 하나,
eye-level/low/high angle 중 하나,
soft/rim/backlit lighting 중 하나를 포함하세요.
watercolor diary illustration, soft pastel palette, warm tones.
Keep the same main character across all scenes.
"""

def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 바아 scenes 리스트를 반환한다."""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text},
        ],
        response_format={"type":"json_object"},
        temperature=0.7,
        max_tokens=1500,
    )
    
    content = response.choices[0].message.content
    scenes = json.loads(content)["scenes"]
    return scenes

def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면 x 필수 3필드를 충족하는지 검증한다."""
    errors = []
    
    if len(scenes) !=4:
        errors.append(f"오류 수 오류: {len(scenes)}개 (4개여야 함)")
        
    required_fileds = ["scene_id", "scene_kr", "prompt_en"]
    for i, scene in enumerate(scenes, 1):
        for field in required_fileds:
            if field not in scene:
                errors.append(f"장면 {i}: '{field}' 필드 누락")
    return errors

def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장한다."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"scenes": scenes}, f, ensure_ascii=False, indent=2)