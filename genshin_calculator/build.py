from collections import defaultdict
from numbers import Number
from typing import Dict, Optional

from .stats import DmgType, Stat, STATS

class Build():
    """A class representing an ensemble of statistics for a character given by its own stats and the ones from weapons,
    artifacts, talents...
    
    Parameters
    ----------
    *stats : Stat
        Stats to include in the build.
    refinement : int, default 0
        Refinement level of the weapon.
    constellation : int, default 0
        Constellation level of the character.
    name : Optional[str], optional
        Name of the build.
    """

    def __init__(self,
                 *stats: Stat,
                 character_level: int = 0,
                 refinement: int = 0,
                 constellation: int = 0,
                 name: Optional[str] = None):
        self._stats = list(stats)
        self._sets_count = {}
        self._artifacts_name = []
        self.character_level = character_level
        self._refinement = refinement
        self._constellation = constellation
        self._weapon_name = ""
        self.name = name

    def compute(self, current_dmg_type: DmgType) -> Dict[STATS, Number]:
        """Compute the final statistics for the build, given a damage type.

        Parameters
        ----------
        current_dmg_type : DmgType
            The damage type to compute stats for.

        Returns
        -------
        Dict[STATS, Union[Number, Any]]
            Dictionary of computed stats.

        Raises
        ------
        ValueError
            If more than 5 artifacts are equipped or if refinement/constellation is not set.
        """
        if len(self._artifacts_name) > 5:
            raise ValueError("A character can't have more than 5 artifacts.")
        if self._refinement == 0 or self._constellation == 0 or self.character_level == 0:
            raise ValueError("Character level, refinement and constellation values required"
                             "to compute final statistics.")
        stats_dict = {STATS.REFINEMENT: self._refinement, STATS.CONSTELLATION: self._constellation,
                      STATS.ATK: STATS.FLAT_ATK + STATS.ATK_PERC * STATS.BASE_ATK / 100,
                      STATS.HP: STATS.FLAT_HP + STATS.HP_PERC * STATS.BASE_HP / 100,
                      STATS.DEF: STATS.FLAT_DEF + STATS.DEF_PERC * STATS.BASE_DEF / 100}
        stats_dict = defaultdict(int, stats_dict)
        for stat in self._stats:
            if current_dmg_type in stat.dmg_type:
                stats_dict[stat.type] += stat.value
            # stats_dict[stat.type, stat.dmg_type] = stats_dict.setdefault((stat.type, stat.dmg_type), 0) + stat.value
        
        for _set, count in self._sets_count.items():
            if count >= 2:
                # TODO: function sum dict in utils.py
                for _stat in _set.value.bonus_2_pcs:
                    # TODO: Stat object can be used instead using type and dmg_type for comparaison (__eq__ ??)
                    # stats_dict[(_stat.type, _stat.dmg_type)] = stats_dict.setdefault((_stat.type, _stat.dmg_type), 0.) + _stat.value
                    if current_dmg_type in _stat.dmg_type:
                        stats_dict[_stat.type] += _stat.value
            if count >= 4:
                for _stat in _set.value.bonus_4_pcs:
                    # stats_dict[(_stat.type, _stat.dmg_type)] = stats_dict.setdefault((_stat.type, _stat.dmg_type), 0.) + _stat.value
                    if current_dmg_type in _stat.dmg_type:
                        stats_dict[_stat.type] += _stat.value
        
        to_resolve = [stat for stat in stats_dict if not isinstance(stats_dict[stat], Number)]
        while to_resolve:
            for stat in to_resolve:
                stats_dict[stat] = stats_dict[stat].resolve(stats_dict)
            to_resolve = [stat for stat in stats_dict if not isinstance(stats_dict[stat], Number)]
        return stats_dict
    
    def _sum_constellation(self, other):
        if self._constellation > 0 and other._constellation > 0:
            raise ValueError("Can't set constellation value several times.")
        return self._constellation + other._constellation
    
    def _sum_refinement(self, other):
        if self._refinement > 0 and other._refinement > 0:
            raise ValueError("Can't set refinement value several times.")
        return self._refinement + other._refinement

    def __add__(self, other):
        if isinstance(other, Build):
            new_build = Build(*self._stats, *other._stats,
                              refinement=self._sum_refinement(other),
                              constellation=self._sum_constellation(other))
            if self._weapon_name:
                if other._weapon_name:
                    raise ValueError("Can't add two weapons builds.")
                new_build._weapon_name = self._weapon_name
            elif other._weapon_name:
                new_build._weapon_name = other._weapon_name
            
            if self.character_level:
                if other.character_level:
                    raise ValueError("Can't add two characters.")
                new_build.character_level = self.character_level
            elif other.character_level:
                new_build.character_level = other.character_level
            
            
            new_build._artifacts_name = self._artifacts_name + other._artifacts_name

            for term in (self, other):
                for _set, count in term._sets_count.items():
                    new_build._sets_count[_set] = new_build._sets_count.setdefault(_set, 0) + count
            
            print("TODO: check this method (Build addition)")

            return new_build

    def __iadd__(self, other):
        self._stats += [*other._stats]
        self._refinement = self._sum_refinement(other)
        self._constellation = self._sum_constellation(other)
        self._weapon_name += other._weapon_name
        self._artifacts_name += [*other._artifacts_name]
        for _set, count in other._sets_count.items():
            self._sets_count[_set] = self._sets_count.setdefault(_set, 0) + count
        
        return self