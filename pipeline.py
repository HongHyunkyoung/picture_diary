# pipeline.py — 그림일기 통합 파이프라인
import json
import time
from datetime import date
from pathlib import Path

from agents.scene import extract_scenes
from agents.image import batch_generate
from agents.video import submit_kling, status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate

def picture_diary_pipeline(
    diary_text: str,
    model: str = "flux",
    animate_first: bool = False,
) -> dict:
    """
    그림일기 통합 파이프라인.
    diary_text → scenes → images → (선택) 영상 → results.json
    """
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n[1단계] 장면 추출 중...")
    scenes = extract_scenes(diary_text)
    print(f"  → {len(scenes)}개 장면 추출 완료")

    print("\n[2단계] 이미지 생성 중...")
    image_paths = batch_generate(scenes, model=model, out_dir=out_dir)
    print(f"  → {len(image_paths)}장 생성 완료")

    video_path = None
    if animate_first and image_paths:
        print("\n[3단계] 영상 생성 중 (Mock)...")

        image_url = f"https://mock.fal.ai/uploads/{image_paths[0].name}"

        task_id = submit_kling(image_url, "slow zoom in, gentle motion")
        print(f"  → task_id: {task_id}")

        iteration = 0
        start_ts = time.time()
        status = ""
        while True:
            if not (check_max_iter(iteration) and check_timeout(start_ts)):
                break
            status = status_kling(task_id)
            if check_predicate(status):
                break
            iteration += 1
            time.sleep(1)

        if check_predicate(status):
            video_url = result_kling(task_id)
            video_path = out_dir / "scene_1.mp4"
            video_path.write_text(f"[Mock] {video_url}")
            print(f"  → 영상 저장 완료: {video_path}")
    else:
        print("\n[3단계] 영상 생성 건너뜀 (animate_first=False)")

    print("\n[4단계] results.json 저장 중...")
    results = {
        "diary_first_line": diary_text.strip().split("\n")[0],
        "scenes": scenes,
        "images": [str(p) for p in image_paths],
        "video": str(video_path) if video_path else None,
    }
    results_path = Path("results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  → {results_path} 저장 완료")

    return results



if __name__ == "__main__":
    from pathlib import Path

    diary_text = Path("diary.md").read_text(encoding="utf-8") \
        if Path("diary.md").exists() \
        else "오늘 아침 감자전을 만들다가 블렌더가 터졌다."

    result = picture_diary_pipeline(
        diary_text,
        model="flux",
        animate_first=False,   
    )

    print("\n--- 결과 요약 ---")
    print(f"장면 수: {len(result['scenes'])}")
    print(f"이미지 수: {len(result['images'])}")
    print(f"영상: {result['video']}")

 # ─── pipeline 시범 실행 ───────────────────────────────────────
print("\n" + "="*50)
print("pipeline 시범 실행")
print("="*50)

from pipeline import picture_diary_pipeline

diary_text = Path("diary.md").read_text(encoding="utf-8") \
    if Path("diary.md").exists() \
    else "오늘 아침 감자전을 만들다가 블렌더가 터졌다."

result = picture_diary_pipeline(
    diary_text,
    model="flux",
    animate_first=False, 
)

print(f"\n[결과] 장면 {len(result['scenes'])}개, 이미지 {len(result['images'])}장")