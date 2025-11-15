from enum import Flag, auto
from typing import Union


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