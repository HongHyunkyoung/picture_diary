import subprocess
from pathlib import Path


def check_env_in_gitignore() -> bool:
    """.gitignore에 .env가 있는지 확인한다."""
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        return False
    text = gitignore_path.read_text(encoding="utf-8")
    return ".env" in text


def check_env_in_staged() -> bool:
    """.env가 git staged 목록에 없으면 False(안전)를 반환한다."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    return ".env" in result.stdout


if __name__ == "__main__":
    gitignore_ok = check_env_in_gitignore()
    env_not_staged = not check_env_in_staged()

    print(f".gitignore에 .env 등록: {'✅' if gitignore_ok else '❌ 누락'}")
    print(f".env staged 안됨:       {'✅' if env_not_staged else '❌ staged 상태 — push 중단'}")

    if gitignore_ok and env_not_staged:
        print("\n✅ 안전 — push 가능합니다.")
    else:
        print("\n❌ push 전에 위 문제를 해결하세요.")