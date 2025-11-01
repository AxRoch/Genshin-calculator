from .build import Build
from .stats import STATS


class Character(Build):
    """A class representing a character build, inheriting from `Build`.

    This class initializes a character with default critical damage, critical rate, and energy recharge stats,
    and allows for further customization via additional stats and constellation level.

    Parameters
    ----------
    *stats : STATS
        Additional stats to apply to the character.
    level : int, default 90
        The level of the character.
    """

    def __init__(self, *stats: STATS, level: int = 90):
        super().__init__(STATS.CRIT_DGT(50.), STATS.CRIT_RATE(5.), STATS.ER(100.),
                         *stats, character_level=level, constellation=1)

    def __call__(self, *stats: STATS, constellation: int = 1):
        self._constellation = constellation
        self += Build(*stats)
        return self


FISCHL = Character(STATS.BASE_PV(9189.3),
                   STATS.BASE_ATK(244.26),
                   STATS.BASE_DEF(593.79),
                   STATS.ATK_PERC(24))
GANYU = Character(STATS.BASE_PV(9796.73),
                  STATS.BASE_ATK(334.85),
                  STATS.BASE_DEF(630.21),
                  STATS.CRIT_DGT(38.4),
                  STATS.CRIT_RATE(10))
NEUVILETTE = Character(STATS.BASE_PV(14695.09),
                       STATS.BASE_ATK(208.32),
                       STATS.BASE_DEF(576.42),
                       STATS.CRIT_DGT(38.4))
WANDERER = Character(STATS.BASE_PV(10164.11),
                     STATS.BASE_ATK(327.67),
                     STATS.BASE_DEF(607.16),
                     STATS.CRIT_RATE(19.2))