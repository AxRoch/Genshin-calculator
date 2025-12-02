from enum import Enum

from .build import Build
from .damages import DmgType, ElementType
from .stats import STATS
    

class _Weapon(Build):

    def __init__(self, *stats):
        super().__init__(*stats)
        self._refinement = 1
        self._weapon_name = None
    
    def __repr__(self):
        return f"{self._weapon_name} ({self._stats})"
        
        
class WEAPONS(Enum):

    def __init__(self, value):
        super().__init__()
        self.value._weapon_name = f'{self.name}'
        self.value._names = [f'{self.name}']
    
    def __call__(self, refinement=1):
        self.value._refinement = refinement
        return self.value


class BOWS(WEAPONS):
    HAMAYUMI_FULL_ER = _Weapon(STATS.BASE_ATK(454),
                               STATS.ATK_PERC(55.1),
                               STATS.DMG(24 + 8 * STATS.REFINEMENT, DmgType.NORMAL),
                               STATS.DMG(18 + 6 * STATS.REFINEMENT, DmgType.CHARGED))
    HAMAYUMI = _Weapon(STATS.BASE_ATK(454),
                       STATS.ATK_PERC(55.1),
                       STATS.DMG(12 + 4 * STATS.REFINEMENT, DmgType.NORMAL),
                       STATS.DMG(9 + 3 * STATS.REFINEMENT, DmgType.CHARGED))
    CHAIN_BREAKER = _Weapon(STATS.BASE_ATK(565),
                            STATS.ATK_PERC(27.6 + 3 * (3.6 + 1.2 * STATS.REFINEMENT)),
                            STATS.EM(18 + 6 * STATS.REFINEMENT))
    BLACKLIFF = _Weapon(STATS.BASE_ATK(565),
                        STATS.CRIT_DMG(36.8))
    ALLEY_HUNTER = _Weapon(STATS.BASE_ATK(565),
                           STATS.ATK_PERC(27.6),
                           STATS.DMG(7.5 + 2.5 * STATS.REFINEMENT) # R1 : 2% per second (max 20) R5 : 4% per second
                            # STATS.DMG(15 + 5 * STATS.REFINEMENT),
                            )
    STRINGLESS = _Weapon(STATS.BASE_ATK(510),
                         STATS.EM(165),
                         STATS.DMG(18 + 6 * STATS.REFINEMENT))


class CATALYST(WEAPONS):
    FOUR_WINDS = _Weapon(STATS.BASE_ATK(608),
                         STATS.CRIT_RATE(33.1),
                         STATS.DMG(6 + 2 * STATS.REFINEMENT, ElementType.ELEMENTAL))
    WIDSITH = _Weapon(STATS.BASE_ATK(510),
                       STATS.CRIT_DMG(55.1),
                       STATS.ATK_PERC(120 / 3),
                       STATS.DMG(96 / 3),
                       STATS.EM(480 / 3))
    PROTOTYPE_AMBER = _Weapon(STATS.BASE_ATK(510),
                              STATS.HP_PERC(41.3))


class SWORD(WEAPONS):
    AUBIER = _Weapon(STATS.BASE_ATK(565),
                     STATS.ER(30.6),
                     STATS.EM(90))