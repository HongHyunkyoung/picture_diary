# agents/video.py — Kling Image-to-Video (Mock 버전)
# 실제 API를 쓰려면 MOCK = False로 바꾸고 fal_client를 활성화한다.

import os
import time
from dotenv import load_dotenv
import fal_client

load_dotenv()

MOCK = True
KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"

def submit_kling(image_url: str, prompt: str, duration: int = 5,) -> str:
    """Kling에 영상 생성 작업을 제출하고 task_id를 반환한다.

    Mock 모드에서는 실제 API를 호출하지 않고
    가짜 task_id를 즉시 반환한다.
    """
    if MOCK:
        print("[MOCK] sumit_kling() 호출됨")
        print(f"    image_url: {image_url[:50]}...")
        print(f"    prompt: {prompt}")
        print(f"    duration: {duration}초")
        fake_task_id = f"mock_task_{int(time.time())}"
        print(f"[Mock] task_id 생성: {fake_task_id}")
        return fake_task_id
    # 실제 API 버전 (MOCK = False일 때 실행됨)
    # handler = fal_client.submit(
    #     KLING_MODEL,
    #     arguments={
    #         "image_url": image_url,
    #         "prompt": prompt,
    #         "duration": duration,
    #     },
    # )
    # return handler.request_id