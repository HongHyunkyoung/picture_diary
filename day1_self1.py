import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY") or ""
    print(f"[환경 확인] OPENAI_API_KEY 첫 5자: {api_key[:5] if api_key else 'None'}")
    return api_key

def build_scene_prompt() -> str:
    prompt = (
        "a messy kitchen counter, a slightly burnt potato pancake on a plate, "
        "a glass of Korean rice wine makgeolli next to it, "
        "blurry background showing a blender with potato splatters, "
        "cozy but chaotic atmosphere, "
        "watercolor diary illustration style, hand-drawn look, warm tones"
    )
    return prompt

def generate_image(client: OpenAI, prompt:str) -> str:
    response = client.images.generate(
        model ="gpt-image-1",
        prompt = prompt,
        size = "1024x1024",
        quality = "low",
        n=1
    )
    image_base64 = response.data[0].b64_json
    return image_base64

def save_image(image_base64:str, out_path:Path) -> None:
    img_bytes = base64.b64decode(image_base64)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(img_bytes)
    
if __name__ == "__main__":
    load_api_key()
    client = OpenAI()
    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")
    print("[생성 중] 이미지 생성 중 ...")
    image_base64 = generate_image(client, prompt)
    out_path = Path("outputs") / "scene01.png"
    save_image(image_base64, out_path)
    print(f"[저장 완료] {out_path}")
    
