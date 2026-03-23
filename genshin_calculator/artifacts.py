from dataclasses import dataclass
from enum import Enum
from itertools import combinations_with_replacement
from typing import List

from .build import Build
from .damages import DmgType, ElementType
from .data import ARTIFACTS_IMPROVEMENTS, ARTIFACTS_MAIN_STATS
from .stats import STATS


_BEST_IMPROVEMENTS = {stat: stat(max(list_improvements)) for stat, list_improvements in ARTIFACTS_IMPROVEMENTS.items()}

class ArtifactPiece(Build):

    def __init__(self, name, _set, *stats):
        super().__init__(*stats, name=name)
        self._sets_count[_set] = self._sets_count.setdefault(_set, 0) + 1
        self._artifacts_name.append(name)
    
    def improve(self, nb_improvement, stats_to_improve=None):
        """Iterates over several improved version of the current artifact.

        Parameters
        ----------
        nb_improvement : int
            The number of improvements to apply to the artifact.
        stats_to_improve : List[STATS], optional
            If given, the list of statistics to improve. Else, all possible stats of the current artifact are considered.

        Yields
        ------
        ArtifactPiece
            A new artifact with the applied improvements.
        """
        possible_stats = [stat.type for stat in self._stats]
        if stats_to_improve is None:
            stats_to_improve = possible_stats
        else:
            for stat in stats_to_improve:
                if stat not in possible_stats:
                    raise ValueError(f"Can't add the brand new stat {stat}")

        for improvement_paths in combinations_with_replacement(stats_to_improve, nb_improvement):
            improved_artifact = self + Build(*[_BEST_IMPROVEMENTS[stat] for stat in improvement_paths])
            yield improved_artifact


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
    GILDED_DREAM = Set(bonus_2_pcs={STATS.EM(80)},
                       bonus_4_pcs={STATS.EM(150)})
    GOLDEN_TROUP = Set(bonus_2_pcs={STATS.DMG(20, DmgType.SKILL)},
                       bonus_4_pcs={STATS.DMG(50, DmgType.SKILL)})
    DESERT_PAVILION = Set(bonus_2_pcs={STATS.DMG(15, ElementType.ANEMO)},
                          bonus_4_pcs={STATS.SPEED(10),
                                       STATS.DMG(40, DmgType.CHARGED | DmgType.NORMAL)})
    MARECHAUSSE_HUNTER = Set(bonus_2_pcs={STATS.DMG(15, DmgType.CHARGED | DmgType.NORMAL)},
                             bonus_4_pcs={STATS.CRIT_RATE(36)})
    OBSIDIAN_CODEX = Set(bonus_2_pcs={},
                         bonus_4_pcs={})
    
    def __call__(self, *stats, name=None):
        """Set the statistics of the artifact build.

        Parameters
        ----------
        *stats : STATS
            Stats to add to the artifact.
        name : str, optional
            If given, label the artifact with a name.

        Returns
        -------
        ArtifactPiece
            The artifact with its statistics set.
        """
        return ArtifactPiece(name, self, *stats)


def compute_optimal_artifacts(character,
                              rotation,
                              sand_main_stat,
                              cup_main_stat,
                              helmet_main_stat,
                              wanted_substats: List,
                              **rotation_kwargs):
    base_dmg = sum(rotation.compute(**rotation_kwargs))

    nb_possible_improvements = {substat: 30 - 5 * int(substat in (STATS.FLAT_ATK,
                                                                  STATS.FLAT_HP,
                                                                  sand_main_stat,
                                                                  cup_main_stat,
                                                                  helmet_main_stat)) for substat in wanted_substats}

    old_base_stats = {}
    for artifact_piece_type, main_stat in [('flower', STATS.FLAT_HP),
                                           ('feather', STATS.FLAT_ATK),
                                           ('sand', sand_main_stat),
                                           ('cup', cup_main_stat),
                                           ('helmet', helmet_main_stat)]:
        old_base_stats[artifact_piece_type] = getattr(character, artifact_piece_type + 's')
        setattr(character, artifact_piece_type + 's', Build(main_stat(ARTIFACTS_MAIN_STATS[main_stat])))
    
    for i in range(45):
        possible_substat = [substat for substat, remaining_instance in nb_possible_improvements.items()
                            if remaining_instance > 0]
        best_substat = possible_substat[0]
        character.flowers._stats.append(_BEST_IMPROVEMENTS[best_substat])
        best_dmg = sum(rotation.compute(**rotation_kwargs))

        for substat in possible_substat[1:]:
            character.flowers._stats[i+1] = _BEST_IMPROVEMENTS[substat]
            dmg = sum(rotation.compute(**rotation_kwargs))

            if dmg > best_dmg:
                best_dmg = dmg
                best_substat = substat
            
        print(best_substat, best_dmg)
            
        character.flowers._stats[i+1] = _BEST_IMPROVEMENTS[best_substat]
        nb_possible_improvements[best_substat] -= 1
    
    print(best_dmg / base_dmg)

    # Recover old stats
    for artifact_piece_type, artifact_build in old_base_stats.items():
        setattr(character, artifact_piece_type + 's', artifact_build)


