import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client

def load_keys() -> None:
    """.env에서 FAL_KEY를 로드하고 첫 5자를 출력한다."""
    load_dotenv()
    fal_key = os.getenv("FAL_KEY") or ""
    if not fal_key:
        raise ValueError(".env에서 FAL_KEY가 없습니다.")
    return

def load_first_prompt() -> str:
    """scene_prmpts.json에서 첫 번째 장면의 prompt_en을 반환한다."""
    data = json.loads(
        Path("scene_prompts.json").read_text(encoding="utf-8")
    )
    prompt = data["scenes"][0]["prompt_en"]
    return prompt

def call_flux_schnell(prompt: str) -> str:
    """FLUX-schnell로 이미지 1장 생성, URL을 반환한다."""
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        # ⭕ 오타 수정: atguments -> arguments
        arguments={
            "prompt": prompt,
            "num_images": 1,
        }
    )
    url = result["images"][0]["url"]
    return url

def save_image(url: str, out_path:Path) -> None:
    """URL의 이미지르 내려받아 파일로 저장한다."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(response.content)
    
if __name__ == "__main__":
    load_keys()

    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt[:60]}...")

    print("[생성 중] FLUX-schnell 호출 중...")
    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url[:60]}...")

    out_path = Path("outputs") / "scene01_fal.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")