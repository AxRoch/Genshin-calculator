from enum import Enum, auto
from functools import reduce
from math import prod
from numbers import Number
from operator import truediv
from typing import Dict, Type, Union

from .damages import DmgType, ElementType


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
    if isinstance(stat_value, _StatsOp):
        return stat_value._operation(resolve_stat(term_value, stat_dict)
                                     for term_value in stat_value.operands)
    raise NotImplementedError


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
    element_type : ElementType, default ElementType.ALL
        The elemental type of damage represented.
    """

    def __init__(self, stat_type: 'STATS',
                 value: Union[Number, _StatsOp, 'STATS'],
                 dmg_type: DmgType = DmgType.ALL,
                 element_type: ElementType = ElementType.ALL):
        self.type = stat_type
        self.value = value
        self.dmg_type = dmg_type
        self.element_type = element_type
    
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

    HP = auto()
    BASE_HP = auto()
    HP_PERC = auto()
    FLAT_HP = auto()

    DEF = auto()
    BASE_DEF = auto()
    DEF_PERC = auto()
    FLAT_DEF = auto()

    EM = auto()
    ER = auto()
    SPEED = auto()
    REACTION_DMG_BONUS = auto()

    CRIT_DMG = auto()
    CRIT_RATE = auto()

    DMG = auto()
    FLAT_DMG = auto()
    BASE_DMG_MULT = auto()

    MULTIPLIER_PERC = auto()

    RES_SHRED = auto()
    DEF_SHRED = auto()

    HEALING_BONUS = auto()
    
    CONSTELLATION = auto()
    REFINEMENT = auto()

    def __call__(self, value: Union[Number, _StatsOp, 'STATS'],
                 *restrictions : Union[DmgType, ElementType]):
        """Create a Stat instance associated with this STATS enum member.
        
        Parameters
        ----------
        value : Union[Number, _StatsOp, STATS]
            The numerical value or statistical expression associated with the statistic.
        *restrictions : Union[DmgType, ElementType]
            If given, this statistics will be considered only for the associated damage type in the
            rotation.
        """
        dmg_type = DmgType._ZERO
        element_type = ElementType._ZERO
        for restriction in restrictions:
            if isinstance(restriction, DmgType):
                dmg_type = dmg_type | restriction
            elif isinstance(restriction, ElementType):
                element_type = element_type | restriction
            else:
                raise ValueError("restrictions should be `DmgType` or `ElementType` objects.")
        
        # No restrictions applied
        if dmg_type is DmgType._ZERO:
            dmg_type = DmgType.ALL
        if element_type is ElementType._ZERO:
            element_type = ElementType.ALL

        return Stat(self, value, dmg_type=dmg_type, element_type=element_type)
    
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