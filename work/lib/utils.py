import mpmath

PI_50 = "3.14159265358979323846264338327950288419716939937510"
PI_100 = PI_50 + "58209749445923078164062862089986280348253421170679"
PI_150 = PI_100 + "82148086513282306647093844609550582231725359408128"

def print_pi(pi: float, pi_true: str, digits: int, _format: str = None):
    """円周率と一致する部分に色をつけてprintする
    
    Args
        pi (float): 計算したあたい
        pi_true (str): 円周率の正しい値
        digits (int): 出力する桁数
        _format (str | None) 出力フォーマット 
            {pi} : 円周率
            {mdigit} : 一致した桁数
    """
    if len(pi_true) < digits:
        raise ValueError(
            f"length of pi_true must be grater than or equal to digits."
            f"given len(pi_true) = {len(pi_true)}, digits = {digits}"
        )
        
    if _format is None:
        _format = "π = {pi} ({mdigit} 桁まで一致)"
    
    pi_str = mpmath.nstr(pi, digits, strip_zeros=False)
    
    def match_nod(pi_str: str) -> int:
        for i in range(0, min(len(pi_str), len(pi_true))):
            if pi_str[i] != pi_true[i]:
                break
        return i 
    
    nod = match_nod(pi_str)
    colored_pi = f"\033[31m{pi_str[0:nod]}\033[0m{pi_str[nod:]}"
    mdigit = max(0, nod -2)
    
    print(_format.format(pi=colored_pi, mdigit=mdigit))