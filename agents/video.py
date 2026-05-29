# agents/video.py — Kling Image-to-Video (Mock 버전)
# 실제 API를 쓰려면 MOCK = False로 바꾸고 fal_client를 활성화한다.

import os
import time
from dotenv import load_dotenv
import fal_client
from pathlib import Path

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

def status_kling(request_id: str) -> str:
    """Kling 작업 상태를 1회 조회하고 상태 문자열을 반환한다.
        Mock 모드에서는 가짜 상태를 반환한다."""
    if MOCK:
        # Mock: 3번 호출 후 completed 반환 시뮬레이션
        # 실제로는 매번 다른 상태가 온다
        call_count_path = Path("mock_call_count.txt")
        count = int(call_count_path.read_text()) if call_count_path.exists() else 0
        count += 1
        call_count_path.write_text(str(count))

        if count >= 3:
            print(f"[Mock] status_kling() → completed (호출 {count}회)")
            return "completed"
        else:
            print(f"[Mock] status_kling() → IN_PROGRESS (호출 {count}회)")
            return "IN_PROGRESS"

    # 실제 버전
    # import fal_client
    # status_obj = fal_client.status(KLING_MODEL, request_id, with_logs=False)
    # return status_obj.status

def result_kling(request_id: str) -> str:
    """
    완료된 Kling 작업의 영상 URL을 반환한다.
    Mock 모드에서는 가짜 URL을 반환한다.
    """
    if MOCK:
        fake_url = f"https://mock.fal.ai/videos/{request_id}.mp4"
        print(f"[Mock] result_kling() → {fake_url}")
        return fake_url

    # 실제 버전
    # import fal_client
    # result = fal_client.result(KLING_MODEL, request_id)
    # return result["video"]["url"]

def generate_video(image_path: str, output_path: str) -> str:
    """
    이미지를 입력받아 영상을 생성하고 저장된 경로를 반환한다.
    Mock 모드에서는 실제 API 호출 없이 가짜 mp4 파일을 생성한다.
    """
    if MOCK:
        print(f"[Mock] generate_video() 호출됨")
        print(f"  image_path: {image_path}")
        print(f"  output_path: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(f"[Mock] video from {image_path}")
        print(f"[Mock] 저장 완료: {output_path}")
        return output_path

    # 실제 버전
    # image_url = fal_client.upload_file(image_path)
    # task_id = submit_kling(image_url, "slow zoom in, gentle motion")
    # ... 폴링 후 저장
    # return output_path