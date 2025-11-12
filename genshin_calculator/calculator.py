from dataclasses import dataclass
from itertools import product
from typing import Any, Iterable, List, Union

from .reactions import NO_REACTIONS, Reaction
from .stats import STATS, DmgType, Rotation


def get_res_mult(resistances: Union[float, Iterable[float]], res_loss: float) -> float:
    """Get the multiplier related to resistance applied to the total damages.

    Parameters
    ----------
    resistances : float or Iterable[float]
        If one element, the resistance of the ennemy used to compute the associated damage
        multipliers.
        If an iterable of two elements, it will be considered as an interval of minimum and maximum
        ennemy resistances. The function will compute an interval on this interval.
    res_loss : float
        The resistance shred bonus of the character that will decrease the resistance of the ennemy.
    """
    if isinstance(resistances, (int, float)):
        resistances = [resistances]
    
    if len(resistances) == 1:
        new_res = (resistances[0] - res_loss) / 100
        if new_res < 0:
            new_res /= 2
        res_mult = max(0, 1 - new_res)
        return res_mult
    elif len(resistances) != 2:
        raise ValueError("`resistances` argument should be an int, float, or an iterable with 1 or"
                         " 2 int/float.")
    
    # Compute integral using the given interval
    min_res, max_res = min(resistances) / 100, max(resistances) / 100
    res_loss /= 100

    F_base = lambda a, b: (1 + res_loss) * (b - a) - (b**2 - a**2) / 2
    F_halved = lambda a, b: (1 + res_loss / 2) * (b - a) - (b**2 - a**2) / 4

    if min_res > res_loss:
        return F_base(min_res, max_res)
    elif max_res < res_loss:
        return F_halved(min_res, max_res)
    

    return F_halved(min_res, res_loss) + F_base(res_loss, max_res)


@dataclass
class Calculator():
    character: Any
    weapons: Any
    flowers: Any
    feathers: Any
    sands: Any
    cups: Any
    helmets: Any
    team_bonuses: Any

    def compute(self,
                *actions: List[DmgType],
                resistances: Union[float, Iterable[float]] = 0,
                ennemy_lvl: int = 100,
                reaction: Reaction = NO_REACTIONS):
        """Compute the total damage for all possible combinations of builds.

        Parameters
        ----------
        *actions : List[DmgType]
            List of attack types performed by the character.
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
        assert len(actions) > 0
        char_lvl = self.character.character_level

        SELECTIONS_ORDER = ('team_bonuses', 'weapons', 'helmets',
                            'sands', 'cups', 'feathers', 'flowers')
        enumerate_selections_func = lambda attr_name: enumerate(self.__getattribute__(attr_name))
        results = []
        for indexed_selection in product(*map(enumerate_selections_func, SELECTIONS_ORDER)):
            
            build = self.character
            for i, build_i in indexed_selection:
                build += build_i
                
            # _stats = build.compute() # TODO : a faire en dessous selon le damage type et mettre dmg_type en argument
            total = 0

            for current_dmg_type in sum(actions, start=Rotation()):
                stats = build.compute(current_dmg_type)

                base_dmg_multiplier = 1
                
                res_shred = stats[STATS.DEF_SHRED] / 100
                defense_mult = (100 + char_lvl) / ( (1 - res_shred) * (100 + ennemy_lvl) + (100 + char_lvl) )
                
                base_dmg = current_dmg_type.atk_mult * stats[STATS.ATK]
                base_dmg += current_dmg_type.pv_mult * stats[STATS.HP]
                base_dmg += current_dmg_type.def_mult * stats[STATS.DEF]
                base_dmg = base_dmg * base_dmg_multiplier + stats[STATS.FLAT_DMG]
                
                dmg_bonus = 100 + stats[STATS.DMG]
                dmg = defense_mult * base_dmg * dmg_bonus / 100

                crit_rate = min(100, stats[STATS.CRIT_RATE]) / 100
                final_dmg = (1 + crit_rate * stats[STATS.CRIT_DMG] / 100) * dmg
                
                res_mult = get_res_mult(resistances, stats[STATS.RES_SHRED])
                final_dmg = res_mult * reaction(final_dmg, stats[STATS.EM], stats[STATS.REACTION_DMG_BONUS], char_lvl)

                total += final_dmg
            
            def to_name(attr_name, index):
                selection = self.__getattribute__(attr_name)[index]
                if 'name' in dir(selection):
                    if selection.name is not None:
                        return selection.name
                return f'{attr_name}_{index}'
                
            list_selection_names = [to_name(attr_name, indexed_selection[iattr][0])
                                    for iattr, attr_name in enumerate(SELECTIONS_ORDER)]
            results.append((total, list_selection_names, stats))

        return results