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
                                            character_level=81, refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85)
    assert math.isclose(results[0][0], 3078, rel_tol=3e-4), f'{results[0][0]}'


def test_razor_2():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(146.4),
                                            STATS.DMG(10), STATS.DEF_SHRED(15),
                                            character_level=81, refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85)
    assert math.isclose(results[0][0], 3471, rel_tol=3e-4)

# Hu Tao
def test_hu_tao():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(1069 + 0.0566 * STATS.FLAT_PV),
                                            STATS.DMG(61.6 + 33 + 7.5),
                                            STATS.DMG(48, DmgType.NORMAL),
                                            STATS.FLAT_PV(30830),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(143.64),
                                            character_level=82, refinement=1, constellation=1))
    results = calculator.compute(DmgType.NORMAL(0.741),
                                resistances=10, ennemy_lvl=85)

    assert math.isclose(results[0][0], 5670, rel_tol=3e-4)

    results = calculator.compute(DmgType.CHARGED(2.148),
                                resistances=10, ennemy_lvl=85)

    assert math.isclose(results[0][0], 13282, rel_tol=3e-4)


def test_rosaria():
    calculator = get_build_calculator(Build(STATS.ATK(1420),
                                            STATS.FLAT_DMG(0.2 * STATS.ATK),
                                            STATS.DMG(86.7),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DGT(107.5),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.NORMAL(0.),
                                resistances=70, ennemy_lvl=85)
    
    print(results[0][0])
    assert math.isclose(results[0][0], 163, rel_tol=5e-3)