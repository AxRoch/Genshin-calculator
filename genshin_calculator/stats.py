from enum import Enum, Flag, auto
from functools import reduce
from math import prod
from numbers import Number
from operator import truediv
from typing import Dict, Type, Union


class _StatsOp():
    """Base class for statistical operations.

    This class serves as an abstract operator over Stats and Numbers,
    enabling symbolic composition of stat formulas before resolving them
    into actual numerical values.

    Parameters
    ----------
    *operands : Union[Number, _StatsOp, STATS]
        The operands involved in the operation (numbers, stats, or nested operations).
    """
    
    def __init__(self, *operands: Union[Number, '_StatsOp', 'STATS']):
        self.operands = operands
    
    def __add__(self, operand: Union[Number, '_StatsOp', 'STATS']) -> '_StatsSum':
        return _combine_operand(_StatsSum, self, operand)
    
    def __radd__(self, operand: Union[Number, '_StatsOp', 'STATS']) -> '_StatsSum':
        return _combine_operand(_StatsSum, operand, self)
    
    def __mul__(self, operand: Union[Number, '_StatsOp', 'STATS']) -> '_StatsMul':
        return _combine_operand(_StatsMul, self, operand)
    
    def __rmul__(self, operand: Union[Number, '_StatsOp', 'STATS']) -> '_StatsMul':
        return _combine_operand(_StatsMul, operand, self)
    
    def __truediv__(self, operand: Union[Number, '_StatsOp', 'STATS']) -> '_StatsDiv':
        return _combine_operand(_StatsDiv, self, operand)
    
    def resolve(self, stat_dict: Dict['STATS', Number]) -> Number:
        return resolve_stat(self, stat_dict)


def _combine_operand(Operation: Type,
                     operand_1: Union[Number, _StatsOp, 'STATS'],
                     operand_2: Union[Number, _StatsOp, 'STATS']) -> _StatsOp:
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
    """Represents a multiplication operation among stats."""
    _operation = staticmethod(prod)

    def __repr__(self):
        return " * ".join(f"({elem})" if isinstance(elem, _StatsSum) else str(elem)
                          for elem in self.operands)
    

class _StatsSum(_StatsOp):
    """Represents a summation operation among stats."""
    _operation = staticmethod(sum)

    def __repr__(self):
        return " + ".join(map(str, self.operands))


class _StatsDiv(_StatsOp):
    """Represents a division operation among stats."""
    _operation = staticmethod(lambda sequence: reduce(truediv, sequence))

    def __repr__(self):
        return " / ".join(f"({elem})" if isinstance(elem, _StatsSum) else str(elem)
                          for elem in self.operands)


def resolve_stat(stat_value: Union[Number, _StatsOp, 'STATS'],
                 stat_dict: Dict['STATS', Number]) -> Number:
    """Resolve a stat expression recursively into a numeric value.

    Parameters
    ----------
    stat_value : Union[Number, _StatsOp, STATS]
        The statistical expression.
    stat_dict : dict of STATS to float
        Mapping of stat types to their numeric values or expression.

    Returns
    -------
    float
        The resolved numeric result.
    """
    if isinstance(stat_value, Number):
        return stat_value
    if isinstance(stat_value, STATS):
        return stat_dict[stat_value]
    if isinstance (stat_value, _StatsOp):
        return stat_value._operation(resolve_stat(term_value, stat_dict)
                                     for term_value in stat_value.operands)
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
    """Enumeration of damage types and associated multipliers."""
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

    def _get_mult(self, mult) -> float:
        if mult is None:
            raise ValueError('Multipliers not initialized. Use the `__call__` method in that end.')
        return mult
    
    @property
    def atk_mult(self) -> float:
        return self._get_mult(self._atk_mult)
    
    @property
    def pv_mult(self) -> float:
        return self._get_mult(self._pv_mult)
    
    @property
    def def_mult(self) -> float:
        return self._get_mult(self._def_mult)
        
    def __call__(self, atk_mult: float = 0,
                 pv_mult: float = 0,
                 def_mult: float = 0) -> 'Rotation':
        """Attach multiplier values to this DmgType.

        Parameters
        ----------
        atk_mult, pv_mult, def_mult : float, optional
            Multipliers for attack, HP, and defense scaling respectively.

        Returns
        -------
        Rotation
            A new rotation initialized with this damage type.
        """
        self._atk_mult = atk_mult
        self._pv_mult = pv_mult
        self._def_mult = def_mult
        return Rotation(self)


class Rotation():
    """Represents a sequence of damage types used in a rotation.
    
    Parameters
    ----------
    *dmg_types : DmgType
        The sequence of damages."""

    def __init__(self, *dmg_types: DmgType):
        self._attacks = list(dmg_types)
    
    def __iter__(self):
        for dmg_type in self._attacks:
            yield dmg_type
    
    def __add__(self, other: Union['Rotation', DmgType]) -> 'Rotation':
        return Rotation(*self._attacks, *other._attacks)
    
    def __iadd__(self, other: Union['Rotation', DmgType]) -> 'Rotation':
        self._attacks.extend(other._attacks)


class Stat():
    """Represents a single stat entry with an associated type, value, and damage type.
    
    Parameters
    ----------
    stat_type : STATS
        The type of the statistic.
    value : Union[Number, _StatsOp, STATS]
        The value of the statistic. It can be a numerical value or an expression of other statistics.
    dmg_type : DmgType, default DmgType.ALL
        The type of damage represented.
    """

    def __init__(self, stat_type: 'STATS',
                 value: Union[Number, _StatsOp, 'STATS'],
                 dmg_type: DmgType = DmgType.ALL):
        self.type = stat_type
        self.value = value
        self.dmg_type = dmg_type
    
    def resolve(self, stat_dict: Dict['STATS', Number]) -> Number:
        """Resolve the stat expression recursively into a numeric value.

        Parameters
        ----------
        stat_dict : dict of STATS to float
            Mapping of stat types to their numeric values or expression.

        Returns
        -------
        float
            The resolved numeric result.
        """
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

    def __call__(self, value: Union[Number, _StatsOp, 'STATS'],
                 *restrictions : DmgType):
        """Create a Stat instance associated with this STATS enum member.
        
        Parameters
        ----------
        value : Union[Number, _StatsOp, STATS]
            The numerical value or statistical expression associated with the statistic.
        *restrictions : DmgType
            If given, this statistics will be considered only for the associated damage type in the
            rotation.
        """
        dmg_type = DmgType._ZERO
        if len(restrictions) == 0:
            dmg_type = DmgType.ALL
        for restriction in restrictions:
            if isinstance(restriction, DmgType):
                dmg_type = dmg_type | restriction

        return Stat(self, value, dmg_type=dmg_type)
    
    def __add__(self, term: Union[Number, _StatsOp, 'STATS']) -> _StatsSum:
        if isinstance(term, (Number, STATS)):
            return _StatsSum(self, term)
        return NotImplemented

    def __radd__(self, term: Union[Number, _StatsOp, 'STATS']) -> _StatsSum:
        if isinstance(term, (Number, STATS)):
            return _StatsSum(term, self)
        return NotImplemented
    
    def __mul__(self, factor: Union[Number, _StatsOp, 'STATS']) -> _StatsMul:
        if isinstance(factor, (Number, STATS)):
            return _StatsMul(self, factor)
        return NotImplemented
    
    def __rmul__(self, factor: Union[Number, _StatsOp, 'STATS']) -> _StatsMul:
        if isinstance(factor, (Number, STATS)):
            return _StatsMul(factor, self)
        return NotImplemented
    
    def __truediv__(self, divisor: Union[Number, _StatsOp, 'STATS']) -> _StatsDiv:
        if isinstance(divisor, (Number, STATS)):
            return _StatsDiv(self, divisor)
        return NotImplemented
    
    def __rtruediv__(self, dividend: Union[Number, _StatsOp, 'STATS']) -> _StatsDiv:
        if isinstance(dividend, (Number, STATS)):
            return _StatsDiv(dividend, self)
        return NotImplemented