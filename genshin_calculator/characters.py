from dataclasses import dataclass
from typing import List, Union

from .artifacts import ArtifactPiece
from .build import Build
from .damages import DmgType, ElementType
from .rotation import Attack
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

    # def __post_init__(self, bar):
    #     self._team = Team(self)

    def __call__(self, *stats: STATS, constellation: int = 1):
        """Add stats to the character build and change its constellation.

        Parameters
        ----------
        *stats : STATS
            Stats to add to the character.
        constellation : int, default 1
            The constellation level to set.

        Returns
        -------
        Character
            The updated character build.
        """
        self._constellation = constellation
        self += Build(*stats)
        return self
    
    @property
    def build(self):
        return (self.default_build + self.weapons + self.flowers + self.feathers
                + self.sands + self.cups + self.helmets + self.team_bonuses)
    
    def attack(self,
               dmg_type: DmgType,
               element_type: ElementType,
               atk_mult: float = 0,
               pv_mult: float = 0,
               def_mult: float = 0):
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
        return Attack(self, dmg_type, element_type, atk_mult, pv_mult, def_mult)
    

    def __getitem__(self, stat_type: STATS):
        if not isinstance(stat_type, STATS):
            raise ValueError("`Build`instance shoud be indexed with `STATS` objects.")

        return self.build.compute(DmgType._ZERO, ElementType._ZERO)[stat_type]


@dataclass
class Fischl(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(9189.3),
                                 STATS.BASE_ATK(244.26),
                                 STATS.BASE_DEF(593.79),
                                 STATS.ATK_PERC(24))

 
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
                                 STATS.CRIT_DMG(38.4),
                                 STATS.DMG(30, DmgType.CHARGED)) # TODO !!!!!!!! (A4 Bonus)


@dataclass
class Wanderer(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(10164.11),
                                 STATS.BASE_ATK(327.67),
                                 STATS.BASE_DEF(607.16),
                                 STATS.CRIT_RATE(19.2))


@dataclass
class Yunjin(Character):
    level: int = 90
    default_build: Build = Build(*_DEFAULT_CHARACTER_STATS,
                                 STATS.BASE_HP(10657.42),
                                 STATS.BASE_ATK(191.16),
                                 STATS.BASE_DEF(734.39),
                                 STATS.ER(26.8))
    
    def BURST(self, lvl):
        self.team.add_party_member_bonus(STATS.FLAT_DMG((0.61 + 0.075) * self[STATS.DEF], DmgType.NORMAL),
                                         duration=12)
    # https://genshin-impact.fandom.com/wiki/Yun_Jin

class Team():

    def __init__(self, *teammates):
        self.teammates = teammates
    
    # def add_party_member_bonus(*stat_bonuses, duration=None, nb_hits=None):
    #     for teammate in 