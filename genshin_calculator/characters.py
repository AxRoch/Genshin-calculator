from dataclasses import dataclass
from typing import List, Union

from .artifacts import ArtifactPiece
from .build import Build
from .stats import STATS
from .weapons import _Weapon


_DEFAULT_CHARACTER_STATS = (STATS.CRIT_DMG(50.), STATS.CRIT_RATE(5.), STATS.ER(100.))

@dataclass
class Character():
    """A class representing a character build.

    Parameters
    ----------
    level : int, default 90
        The level of the character.
    """
    level: int
    default_build: Build
    constellation: int = 1
    weapons: Union[_Weapon, List[_Weapon]] = _Weapon()
    flowers: Union[ArtifactPiece, List[ArtifactPiece]] = Build()
    feathers: Union[ArtifactPiece, List[ArtifactPiece]] = Build()
    sands: Union[ArtifactPiece, List[ArtifactPiece]] = Build()
    cups: Union[ArtifactPiece, List[ArtifactPiece]] = Build()
    helmets: Union[ArtifactPiece, List[ArtifactPiece]] = Build()
    team_bonuses: Union[Build, List[Build]] = Build()

    def __call__(self, *stats: STATS, constellation: int = 1):
        self._constellation = constellation
        self += Build(*stats)
        return self

@dataclass
class Fischl(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(9189.3),
                                 STATS.BASE_ATK(244.26),
                                 STATS.BASE_DEF(593.79),
                                 STATS.ATK_PERC(24))

@dataclass
class Wanderer(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(10164.11),
                                 STATS.BASE_ATK(327.67),
                                 STATS.BASE_DEF(607.16),
                                 STATS.CRIT_RATE(19.2))
    
@dataclass
class Ganyu(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(9796.73),
                                 STATS.BASE_ATK(334.85),
                                 STATS.BASE_DEF(630.21),
                                 STATS.CRIT_DMG(38.4),
                                 STATS.CRIT_RATE(10))

@dataclass
class Neuvilette(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(14695.09),
                                 STATS.BASE_ATK(208.32),
                                 STATS.BASE_DEF(576.42),
                                 STATS.CRIT_DMG(38.4))
