import os, requests, json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

COMMON_STYLE = (
    "watercolor diary illustration, "
    "a young woman with black bob haircut, "
    "soft pastel palette, warm tones, cozy mood"
)

def call_dalle(prompt:str, seed: int | None = None) -> str:
    """gpt-image-1로 1장 생성, base64 문자열 반환."""
    client = OpenAI()
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="low",
        n=1
    )
    return response.data[0].b64_json

def call_flux(prompt: str, seed: int | None = None) -> str:
    """FLUX schnell로 1장 생성, URL 반환. seed로 일관성 강화."""
    import fal_client 
    result = fal_client.run(
        "fal-ai/flux/schnell",
        arguments={
            "prompt":prompt,
            "num_images":1,
            "seed": seed,
        }
    )
    return result["images"][0]["url"]

def generate_image(prompt: str, output_path: str, model: str = "dalle", seed: int = 42) -> str:
    """이미지를 생성하고 output_path에 저장한 뒤 경로를 반환한다."""
    model = model.lower()
    is_base64 = model == "dalle"

    if model == "dalle":
        data = call_dalle(prompt)
    elif model == "flux":
        data = call_flux(prompt, seed=seed)
    else:
        raise ValueError(f"지원하지 않는 모델: {model}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    save_image(data, Path(output_path), is_base64=is_base64)
    return output_path

def save_image(data: str, out_path: Path, is_base64: bool = False) -> None:
    """이미지 데이터를 파일로 저장한다."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if is_base64:
        img_bytes = base64.b64decode(data)
    else:
        response = requests.get(data, timeout=30)
        response.raise_for_status()
        img_bytes = response.content
    out_path.write_bytes(img_bytes)
    
def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환. try/except로 한 장 실패 시 격리."""
    saved = []
    is_base64 = model.lower() == "dalle"
    
    for scene in scenes:
        scene_id = scene.get("scene_id", 0)
        prompt_en = scene.get("prompt_en", "")
        
        full_prompt = f"{prompt_en}, {COMMON_STYLE}"
        
        out_path = out_dir / f"scene_{scene_id}.png"
        
        print(f"[생성 중] 장면 {scene_id}: {prompt_en[:40]}...")
        
        try:
            result = generate_image(
                prompt=full_prompt,
                output_path=str(out_path),
                model=model,
            )
            saved.append(Path(result))
            print(f"[저장 완료] {out_path}")
        except Exception as e:
            print(f"[실패] 장면 {scene_id}: {e}")
            continue
    return saved