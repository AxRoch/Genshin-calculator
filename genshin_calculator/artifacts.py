from dataclasses import dataclass
from enum import Enum

from .build import Build
from .stats import STATS, DmgType, ElementType


class ArtifactPiece(Build):

    def __init__(self, name, _set, *stats):
        super().__init__(*stats, name=name)
        self._sets_count[_set] = self._sets_count.setdefault(_set, 0) + 1
        self._artifacts_name.append(name)


@dataclass
class Set():
    bonus_2_pcs: set
    bonus_4_pcs: set


class ARTIFACTS(Enum):
    RANDOM_ARTIFACT = Set(bonus_2_pcs={}, bonus_4_pcs={})
    WANDERER_TROUPE = Set(bonus_2_pcs={STATS.EM(80)},
                          bonus_4_pcs={STATS.DMG(35, DmgType.CHARGED)})
    SHIMENAWA = Set(bonus_2_pcs={STATS.ATK_PERC(18), STATS.EM(0)},
                    bonus_4_pcs={STATS.DMG(50, DmgType.CHARGED | DmgType.NORMAL)})
    GOLDEN_TROUP = Set(bonus_2_pcs={STATS.DMG(20, DmgType.SKILL)},
                       bonus_4_pcs={STATS.DMG(50, DmgType.SKILL)})
    DESERT_PAVILION = Set(bonus_2_pcs={STATS.DMG(15, ElementType.ANEMO)},
                          bonus_4_pcs={STATS.SPEED(10),
                                       STATS.DMG(40, DmgType.CHARGED | DmgType.NORMAL)})
    MARECHAUSSE_HUNTER = Set(bonus_2_pcs=STATS.DMG(15, DmgType.CHARGED | DmgType.NORMAL),
                             bonus_4_pcs=STATS.CRIT_RATE(36))
    
    def __call__(self, *stats, name=None):
        return ArtifactPiece(name, self, *stats)