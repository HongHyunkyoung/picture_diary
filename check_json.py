import json
from pathlib import Path

try:
    data = json.loads(Path('domains/product_prompts.json').read_text(encoding='utf-8'))
    print('JSON 파싱 성공')
    print('도메인:', data['domain'])
    print('장면 수:', len(data['scenes']))
except json.JSONDecodeError as e:
    print('JSON 오류:', e)
except FileNotFoundError:
    print('파일 없음 — domains/product_prompts.json 확인')