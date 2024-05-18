from pydantic import Field, BaseModel
import mpmath
from fractions import Fraction
import math


def sign(x):
    return int(math.copysign(1, x))


class ArctanParam(BaseModel):
    coeff: int
    numer: int = Field(..., ge=1)  # 分子
    denom: int = Field(..., ge=1)  # 分母

    @property
    def x(self) -> float:
        return mpmath.mpf(self.numer) / self.denom
    
    def composit(self) -> "ArctanParam":
        x = Fraction(self.numer, self.denom)
        ret = x
        
        for _ in range(1, abs(self.coeff)):
            ret = (ret + x) / (1 - ret * x)
        
        return ArctanParam(
            coeff = sign(self.coeff),
            numer = ret.numerator,
            denom = ret.denominator
        )
    
    def add(self, atan_param: "ArctanParam") -> "ArctanParam":
        tmp = self.composit()
        a = Fraction(tmp.coeff * tmp.numer, tmp.denom)
        
        tmp = atan_param.composit()
        b = Fraction(tmp.coeff * tmp.numer, tmp.denom)
        
        ret =  (a + b) / (1 - a * b)
        
        return ArctanParam(
            coeff = sign(ret.numerator),
            numer = abs(ret.numerator),
            denom = ret.denominator
        )
    
    def equal_to(self, atan_param: "ArctanParam") -> bool:
        if self.coeff == atan_param.coeff \
                and self.numer == atan_param.numer \
                and self.denom == atan_param.denom:
            return True
        else:
            return False
    

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
        self._term = self._next_term()
        self._val = self._val + self._term
        self._n = self._n + 1
        return self._val


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


class EulerTransformSeries(Series):
    def __init__(self, p: ArctanParam):
        self._n = 0
        self.param = p
        self.x = self.param.x

        self._term = mpmath.mpf(p.coeff) * (self.x / (1 + self.x ** 2))
        self._val = self._term

    def _next_term(self) -> float:
        # a_{n+1} を返す
        return (
            mpmath.mpf(2 * self.n + 2) / (2 * self.n + 3)
        ) * self._val * (
            self.x ** 2 / (1 + self.x ** 2)
        )
