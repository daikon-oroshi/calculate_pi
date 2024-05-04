from typing import Generator, Tuple
from dataclasses import dataclass
import mpmath

@dataclass
class ArctanParam:
    coeff: int
    numer: int  # 分子
    denom: int  # 分母
    
    @property
    def x(self) -> float:
        return mpmath.mpf(self.numer) / self.denom
        
    def __post_init__(self):
        if self.coeff <= 0:
            raise ValueError(f"coeff must be greater than 0. given {self.coeff}")
        if self.numer <= 0:
            raise ValueError(f"numer must be greater than 0. given {self.numer}")
        if self.denom <= 0:
            raise ValueError(f"denom must be greater than 0. given {self.denom}")

            
class Series():
    _n: int
    _term: float
    _val: float  # sum
    x: float
        
    @property
    def n(self) -> int:
        return self.n
    
    @property
    def term(self) -> float:
        return self._term
    
    @property
    def val(self) -> float:
        return self._val
    
    def _next_term(self) -> float:
        raise NotImplementedError()
        
    def __next__(self) -> float:
        raise NotImplementedError()
        
    def __next__(self) -> float:
        self._term = self._next_term()
        self._sum = self._sum + self._term
        self._n = self._n + 1
        return self._sum
        

class ArctanSeries(Series):
    
    def __init__(self, p: ArctanParam):
        self._n = 0
        self.param = p
        self.x = self.param.x
        self._term = p.coeff * self.param.x
        self._val = self._term

    def _next_term(self) -> float:
        # a_{n+1} を返す
        return (-1) * (mpmath.mpf(2 * self._n + 1) / (2 * self._n + 3)) \
                * self._term * (self.x ** 2)
        
        
def EulerTransformSeries(p: ArctanParam):
    def __init__(self, p: ArctanParam):
        self._n = 0
        self.param = p
        x = self.param.x
        
        