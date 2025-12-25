from collections import namedtuple
from dataclasses import dataclass
from itertools import product
from typing import Iterable, List, Union

from .build import Build


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
    weapons: List[Build]
    flowers: List[Build]
    feathers: List[Build]
    sands: List[Build]
    cups: List[Build]
    helmets: List[Build]
    team_bonuses: List[Build]

    def __iter__(self):
        """Iterate over all possible build combinations.

        Yields
        ------
        namedtuple
            A named tuple containing the build name, the selected items and the index of the latter.
        """
        SELECTIONS_ORDER = ('team_bonuses', 'weapons', 'helmets',
                            'sands', 'cups', 'feathers', 'flowers')
        enumerate_selections_func = lambda attr_name: enumerate(self.__getattribute__(attr_name))
        for indexed_selection in product(*map(enumerate_selections_func, SELECTIONS_ORDER)):

            Sample = namedtuple('Sample', ['name', *SELECTIONS_ORDER, *map(lambda elem: f"index_{elem}", SELECTIONS_ORDER)])

            names = []
            for i, (j, build) in enumerate(indexed_selection):
                if build.name:
                    names.append(build.name)
                    continue
                attr_name = SELECTIONS_ORDER[i]
                if len(self.__getattribute__(attr_name)) > 1:
                    names.append(f"{SELECTIONS_ORDER[i]}_{j}")

            yield Sample(name="--".join(names),
                         **{SELECTIONS_ORDER[i]: value for i, (_, value) in enumerate(indexed_selection)},
                         **{f"index_{SELECTIONS_ORDER[i]}": j for i, (j, _) in enumerate(indexed_selection)})