import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def build_prompt_variants() -> list[tuple[str, str]]:
    scene = (
        "a young woman, black bob haircut, DO NOT change gender, "
        "female character only, "
        "a person looking baffled but amused in a messy kitchen, "
        "holding a plate with a slightly burnt potato pancake, "
        "a glass of Korean rice wine makgeolli on the counter, "
        "blurry background showing a blender with potato splatters, "
        "watercolor diary illustration style, hand-drawn look, warm tones"
    )
    variants = [
        (
            "scene01_ws.png",
            f"wide shot, eye-level angle, rim light, {scene}",
        ),
        (
            "scene01_cu.png",
            f"close-up shot, eye-level angle, soft front light, {scene}",
        ),
        (
            # "scene01_low.png",
            # f"medium shot, low angle, backlit, {scene}",
            "scene01_low.png",
            f"medium shot, low angle, cinematic backlit, bright funny atmosphere, {scene}"
        ),
    ]
    return variants

def call_dalle(client: OpenAI, prompt: str) -> str:
    response = client.images.generate(
        model="gpt-image-1",
        prompt = prompt,
        size="1024x1024",
        quality="low",
        n=1,
    )
    return response.data[0].b64_json

def save_image(image_base64: str, out_path: Path) -> None:
    image_bytes = base64.b64decode(image_base64)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)
    

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    variants = build_prompt_variants()
    
    for filename, prompt in variants:
        print(f"[호출 시작]{filename} ...")
        print(f"[프롬프트] {prompt[:60]}...")
        try:
            image_base64 = call_dalle(client, prompt)
            save_image(image_base64, output_dir / filename)
            print(f"[저장 완료] outputs/{filename}")
        except Exception as e:
            print(f"[실패] {filename}: {e}")
            continue
        
    print("\n끝. outputs/ 폴더에서 3장을 비교해 보세요.")