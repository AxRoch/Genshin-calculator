from enum import Flag, auto


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