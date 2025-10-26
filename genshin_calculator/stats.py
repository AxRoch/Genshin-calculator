from enum import Enum, Flag, auto
from functools import reduce
from math import prod
from numbers import Number
from operator import truediv

class _StatsOp():
    
    def __init__(self, *operands):
        self.operands = operands
    
    def __add__(self, operand):
        return _combine_operand(_StatsSum, self, operand)
    
    def __radd__(self, operand):
        return _combine_operand(_StatsSum, operand, self)
    
    def __mul__(self, operand):
        return _combine_operand(_StatsMul, self, operand)
    
    def __rmul__(self, operand):
        return _combine_operand(_StatsMul, operand, self)
    
    def __truediv__(self, operand):
        return _combine_operand(_StatsDiv, self, operand)
    
    def resolve(self, stat_dict):
        return resolve_stat(self, stat_dict)


def _combine_operand(Operation: _StatsOp, operand_1, operand_2):
    if not isinstance(operand_1, (Number, STATS, _StatsOp)):
        return NotImplemented
    if not isinstance(operand_2, (Number, STATS, _StatsOp)):
        return NotImplemented
    
    if isinstance(operand_1, Operation):
        operand_1 = operand_1.operands
    else:
        operand_1 = [operand_1]
    
    if isinstance(operand_2, Operation):
        operand_2 = operand_2.operands
    else:
        operand_2 = [operand_2]
    
    return Operation(*operand_1, *operand_2)


class _StatsMul(_StatsOp):
    _operation = staticmethod(prod)

    def __repr__(self):
        return " * ".join(f"({elem})" if isinstance(elem, _StatsSum) else str(elem)
                          for elem in self.operands)
    

class _StatsSum(_StatsOp):
    _operation = staticmethod(sum)

    def __repr__(self):
        return " + ".join(map(str, self.operands))


class _StatsDiv(_StatsOp):
    _operation = staticmethod(lambda sequence: reduce(truediv, sequence))

    def __repr__(self):
        return " / ".join(f"({elem})" if isinstance(elem, _StatsSum) else str(elem)
                          for elem in self.operands)


def resolve_stat(stat_value, stat_dict):
    if isinstance(stat_value, Number):
        return stat_value
    if isinstance(stat_value, STATS):
        return stat_dict[stat_value]
    if isinstance (stat_value, _StatsOp):
        return stat_value._operation(resolve_stat(term_value, stat_dict) for term_value in stat_value.operands)
    raise NotImplementedError


class ElementType(Flag):
    _ZERO = 0
    PYRO = auto()
    HYDRO = auto()
    ANEMO = auto()
    ELECTRO = auto()
    DENDRO = auto()
    GEO = auto()
    CRYO = auto()
    ELEMENTAL = PYRO | HYDRO | ANEMO | ELECTRO | DENDRO | GEO | CRYO
    PHYSICAL = auto()
    ALL =  ELEMENTAL | PHYSICAL


class DmgType(Flag):
    _ZERO = 0
    NORMAL = auto()
    CHARGED = auto()
    SKILL = auto()
    BURST = auto()
    ALL = NORMAL | CHARGED | SKILL | BURST

    def __init__(self, _value):
        self._atk_mults = None
        self._pv_mults = None
        self._def_mults = None

    def _get_mult(self, mult):
        if mult is None:
            raise ValueError('Mults not initialized. Use `__call__` method in that end.')
        return mult
    
    @property
    def atk_mult(self):
        return self._get_mult(self._atk_mult)
    
    @property
    def pv_mult(self):
        return self._get_mult(self._pv_mult)
    
    @property
    def def_mult(self):
        return self._get_mult(self._def_mult)
        
    def __call__(self, atk_mult=0, pv_mult=0, def_mult=0):
        self._atk_mult = atk_mult
        self._pv_mult = pv_mult
        self._def_mult = def_mult
        return Rotation(self)


class Rotation():

    def __init__(self, *dmg_types):
        self._attacks = list(dmg_types)
    
    def __iter__(self):
        for dmg_type in self._attacks:
            yield dmg_type
    
    def __add__(self, other):
        return Rotation(*self._attacks, *other._attacks)
    
    def __iadd__(self, other):
        self._attacks.extend(other._attacks)


class Stat():

    def __init__(self, stat_type, value, dmg_type=DmgType.ALL):
        self.type = stat_type
        self.value = value
        self.dmg_type = dmg_type
    
    def resolve(self, stat_dict):
        return resolve_stat(self.value, stat_dict)
    
    def __add__(self, other):
        # TODO or remove
        if self.type in (STATS.REFINEMENT,):
            # Constellation
            pass
        if isinstance(other, Stat):
            if other.type == self.type:
                if self.dmg_type == other.dmg_type:
                    return Stat(self.stat_type, self.value + other.value, dmg_type=self.dmg_type)

        return NotImplemented


class STATS(Enum):
    ATK = auto()
    BASE_ATK = auto()
    FLAT_ATK = auto()
    ATK_PERC = auto()

    PV = auto()
    BASE_PV = auto()
    PV_PERC = auto()
    FLAT_PV = auto()

    DEF = auto()
    BASE_DEF = auto()
    DEF_PERC = auto()
    FLAT_DEF = auto()

    EM = auto()
    ER = auto()
    SPEED = auto()
    CRIT_DGT = auto()
    CRIT_RATE = auto()

    DMG = auto()
    FLAT_DMG = auto()
    
    BASE_DMG = auto()
    BASE_DMG_MULT = auto()

    RES_SHRED = auto()
    DEF_SHRED = auto()
    
    CONSTELLATION = auto()
    REFINEMENT = auto()

    def __call__(self, value, *restrictions):
        dmg_type = DmgType._ZERO
        if len(restrictions) == 0:
            dmg_type = DmgType.ALL
        for restriction in restrictions:
            if isinstance(restriction, DmgType):
                dmg_type = dmg_type | restriction

        return Stat(self, value, dmg_type=dmg_type)
    
    def __add__(self, term):
        if isinstance(term, Number) or isinstance(term, STATS):
            return _StatsSum(self, term)
        return NotImplemented

    def __radd__(self, term):
        if isinstance(term, Number) or isinstance(term, STATS):
            return _StatsSum(term, self)
        return NotImplemented
    
    def __mul__(self, factor):
        if isinstance(factor, Number) or isinstance(factor, STATS):
            return _StatsMul(self, factor)
        return NotImplemented
    
    def __rmul__(self, factor):
        if isinstance(factor, Number) or isinstance(factor, STATS):
            return _StatsMul(factor, self)
        return NotImplemented
    
    def __truediv__(self, divisor):
        if isinstance(divisor, Number) or isinstance(divisor, STATS):
            return _StatsDiv(self, divisor)
        return NotImplemented
    
    def __rtruediv__(self, dividend):
        # return self._rop(dividend, _StatsDiv)
        if isinstance(dividend, Number) or isinstance(dividend, STATS):
            return _StatsDiv(dividend, self)
        return NotImplemented