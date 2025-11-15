from dataclasses import dataclass
from typing import Iterable, List, Union

from .artifacts import ArtifactPiece
from .build import Build
from .calculator import get_res_mult
from .damages import DmgType, ElementType
from .reactions import NO_REACTIONS, Reaction
from .stats import STATS
from .weapons import _Weapon


_DEFAULT_CHARACTER_STATS = (STATS.CRIT_DMG(50.), STATS.CRIT_RATE(5.), STATS.ER(100.))

@dataclass
class Attack():
    character: 'Character'
    dmg_type: DmgType
    element_type: ElementType
    atk_mult: float = 0
    pv_mult: float = 0
    def_mult: float = 0


class Rotation():
    """Represents a sequence of damage types used in a rotation.
    
    Parameters
    ----------
    *dmg_types : DmgType
        The sequence of damages."""

    def __init__(self, *attacks: Attack):
        self.team = [] # Should contain maximum 4 characters
        self._attacks = []
        for attack in attacks:
            self._add_attack(attack)
    
    def _add_attack(self, attack: Attack):
        if attack.character not in self.team:
            self.team.append(attack.character)
            if len(self.team) > 4:
                raise ValueError("Teams should contain maximum 4 characters.")
        self._attacks.append(attack)
    
    def __iter__(self):
        for dmg_type in self._attacks:
            yield dmg_type
    
    def __add__(self, other: 'Rotation') -> 'Rotation':
        return Rotation(*self._attacks, *other._attacks)
    
    def __iadd__(self, other: 'Rotation') -> 'Rotation':
        for attack in other._attacks:
            self._add_attack(attack)

    def compute(self,
                resistances: Union[float, Iterable[float]] = 0,
                ennemy_lvl: int = 100,
                reaction: Reaction = NO_REACTIONS):
        """Compute the total damage for all possible combinations of builds.

        Parameters
        ----------
        resistances : Union[float, Iterable[float]], default 0
            Enemy resistance(s).
        ennemy_lvl : int, default 100
            Enemy level.
        reaction : Reaction, optional
            If given, reaction to apply.

        Returns
        -------
        List[Tuple[float, List[str], Dict[STATS, Any]]]
            List of tuples containing total damage, selection names, and stats.
        """
        assert len(self._attacks) > 0
        damages = []

        for attack in self._attacks:
            stats = attack.character.build.compute(attack.dmg_type, attack.element_type)
            char_lvl = attack.character.level

            base_dmg_multiplier = (100 + stats[STATS.MULTIPLIER_PERC]) / 100
            
            res_shred = stats[STATS.DEF_SHRED] / 100
            defense_mult = (100 + char_lvl) / ( (1 - res_shred) * (100 + ennemy_lvl) + (100 + char_lvl) )
            
            base_dmg = attack.atk_mult * stats[STATS.ATK]
            base_dmg += attack.pv_mult * stats[STATS.HP]
            base_dmg += attack.def_mult * stats[STATS.DEF]
            base_dmg = base_dmg * base_dmg_multiplier + stats[STATS.FLAT_DMG]
            
            dmg_bonus = 100 + stats[STATS.DMG]
            dmg = defense_mult * base_dmg * dmg_bonus / 100

            crit_rate = min(100, stats[STATS.CRIT_RATE]) / 100
            final_dmg = (1 + crit_rate * stats[STATS.CRIT_DMG] / 100) * dmg
            
            res_mult = get_res_mult(resistances, stats[STATS.RES_SHRED])
            final_dmg = res_mult * reaction(final_dmg, stats[STATS.EM], stats[STATS.REACTION_DMG_BONUS], char_lvl)

            damages.append(final_dmg)

        return damages

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
        return Attack(self, dmg_type, element_type, atk_mult, pv_mult, def_mult)


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