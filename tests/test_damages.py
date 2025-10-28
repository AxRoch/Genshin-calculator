import math

from genshin_calculator.build import Build
from genshin_calculator.calculator import Calculator
from genshin_calculator.stats import STATS, DmgType

# Examples taken from https://www.youtube.com/watch?v=ai1JgPe1ue4&list=WL&index=45

def get_build_calculator(build):
    return Calculator(character=build,
                      # No other build
                      weapons = [Build()],
                      flowers=[Build()],
                      feathers=[Build()],
                      sands=[Build()],
                      cups=[Build()],
                      helmets=[Build()],
                      team_bonuses=[Build()])


def test_razor_1():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(146.4),
                                            refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85, char_lvl=81)
    assert math.isclose(results[0][0], 3078, abs_tol=1), f'{results[0][0]}'


def test_razor_2():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(146.4),
                                            STATS.DMG(10), STATS.DEF_SHRED(15),
                                            refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85, char_lvl=81)
    assert math.isclose(results[0][0], 3471, abs_tol=1)

# Hu Tao
def test_hu_tao():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(1069 + 0.0566 * STATS.FLAT_PV),
                                            STATS.DMG(61.6 + 33 + 7.5),
                                            STATS.DMG(48, DmgType.NORMAL),
                                            STATS.FLAT_PV(30830),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(143.64),
                                            refinement=1, constellation=1))
    results = calculator.compute(DmgType.NORMAL(0.741),
                                resistances=10, ennemy_lvl=85, char_lvl=82)

    assert math.isclose(results[0][0], 5670, abs_tol=1)

    results = calculator.compute(DmgType.CHARGED(2.148),
                                resistances=10, ennemy_lvl=85, char_lvl=82)

    assert math.isclose(results[0][0], 13282, abs_tol=2)