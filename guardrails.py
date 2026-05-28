import time
from typing import Callable

MAX_ITER = 60
TIMEOUT_SEC = 300
BUDGET_CAP_USD = 0.50

def check_max_iter(iteration: int) -> bool:
    """반복 횟수가 최대치 미만이면 True를 반환한다."""
    return iteration < MAX_ITER
    
def check_timeout(start_ts:float) -> bool:
    """시작 시각으로부터 제한 시간 이내이면 True를 반환한다."""
    return time.time() - start_ts < TIMEOUT_SEC 
    
def check_predicate(status:str, accept:tuple = ("completed", "succeeded")) -> bool:
    """status가 완료 상태이면 True를 반환한다."""
    return status.lower() in accept
    
def check_budget(used_usd:float) -> bool:
    """사용 금액이 상한 이하이면 True를 반환한다."""
    return used_usd < BUDGET_CAP_USD
    