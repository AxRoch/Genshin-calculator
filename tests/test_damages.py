import math

from genshin_calculator.build import Build
from genshin_calculator.calculator import Calculator
from genshin_calculator.reactions import OVERLOAD, REVERSE_MELT, REVERSE_VAPORIZE
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
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(146.4),
                                            character_level=81, refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85)[0][0]
    assert math.isclose(results, 3078, rel_tol=3e-4), f'Damages calculated: {results}'


def test_razor_2():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(146.4),
                                            STATS.DMG(10), STATS.DEF_SHRED(15),
                                            character_level=81, refinement=1, constellation=1))

    results = calculator.compute(DmgType.NORMAL(1.52), resistances=70, ennemy_lvl=85)[0][0]
    assert math.isclose(results, 3471, rel_tol=3e-4), f'Damages calculated: {results}'


def test_hu_tao():
    calculator = get_build_calculator(Build(STATS.FLAT_ATK(1069 + 0.0566 * STATS.FLAT_HP),
                                            STATS.DMG(61.6 + 33 + 7.5),
                                            STATS.DMG(48, DmgType.NORMAL),
                                            STATS.FLAT_HP(30830),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(143.64),
                                            character_level=82, refinement=1, constellation=1))
    results = calculator.compute(DmgType.NORMAL(0.741),
                                resistances=10, ennemy_lvl=85)[0][0]

    assert math.isclose(results, 5670, rel_tol=3e-4), f'Damages calculated: {results}'

    results = calculator.compute(DmgType.CHARGED(2.148),
                                resistances=10, ennemy_lvl=85)[0][0]

    assert math.isclose(results, 13282, rel_tol=3e-4), f'Damages calculated: {results}'


def test_rosaria():
    calculator = get_build_calculator(Build(STATS.ATK(1420),
                                            STATS.FLAT_DMG(0.2 * STATS.ATK),
                                            STATS.DMG(86.7),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(107.5),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.NORMAL(0.),
                                resistances=70, ennemy_lvl=85)[0][0]
    
    assert math.isclose(results, 163, rel_tol=5e-3), f'Damages calculated: {results}'


def test_kokomi():
    calculator = get_build_calculator(Build(STATS.ATK(1333),
                                            STATS.HP(30668),
                                            STATS.FLAT_DMG(0.077 * STATS.HP, DmgType.NORMAL),
                                            STATS.FLAT_DMG(0.15 * STATS.HEALING_BONUS * STATS.HP / 100,
                                                           DmgType.NORMAL | DmgType.CHARGED),
                                            STATS.DMG(75.4),
                                            STATS.HEALING_BONUS(75.9),
                                            STATS.CRIT_RATE(0),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.NORMAL(1.094),
                                resistances=10, ennemy_lvl=85)[0][0]
    
    assert math.isclose(results, 5707, rel_tol=5e-3), f'Damages calculated: {results}'


def test_chongyun():
    calculator = get_build_calculator(Build(STATS.ATK(1707),
                                            STATS.EM(54),
                                            STATS.DMG(61.6), STATS.DMG(30),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(163.5),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.NORMAL(3.27), resistances=10, ennemy_lvl=85, reaction=REVERSE_MELT)[0][0]
    assert math.isclose(results, 20752, rel_tol=5e-3), f'Damages calculated: {results}'


def test_chongyun_buffed():
    calculator = get_build_calculator(Build(STATS.ATK(3333),
                                            STATS.EM(223),
                                            STATS.DMG(61.6), STATS.DMG(30),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(163.5),
                                            STATS.FLAT_DMG(0.73 * 3761), STATS.DMG(15, DmgType.SKILL | DmgType.BURST),
                                            STATS.RES_SHRED(40),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.SKILL(3.27), resistances=10, ennemy_lvl=85, reaction=REVERSE_MELT)[0][0]
    assert math.isclose(results, 87361, rel_tol=5e-3), f'Damages calculated: {results}'


def test_yoimiya():
    NB_HITS = 0
    CURIOSITY_STACKS = 0
    YUNJIN_DEF = (1 + CURIOSITY_STACKS * 0.06 + 0.2) * 689 + 1504
    calculator = get_build_calculator(Build(STATS.ATK(2378),
                                            STATS.EM(117),
                                            STATS.DMG(46.6), STATS.DMG(50, DmgType.NORMAL),
                                            STATS.DMG(NB_HITS * 2),
                                            STATS.FLAT_DMG((0.61 + 0.075) * YUNJIN_DEF, DmgType.NORMAL),
                                            STATS.DMG(15, DmgType.NORMAL),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(193.6),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.NORMAL(1.588 * 0.599), resistances=10, ennemy_lvl=85, reaction=REVERSE_VAPORIZE)[0][0]
    assert math.isclose(results, 19438, rel_tol=5e-3), f'Damages calculated: {results}'


def test_diluc_transformative():
    calculator = get_build_calculator(Build(STATS.ATK(0),
                                            STATS.EM(293),
                                            STATS.REACTION_DMG_BONUS(40),
                                            STATS.RES_SHRED(40),
                                            character_level=81, refinement=1, constellation=1))
    
    results = calculator.compute(DmgType.SKILL(3.27), resistances=10, ennemy_lvl=85, reaction=OVERLOAD)[0][0]
    assert math.isclose(results, 8790, rel_tol=5e-3), f'Damages calculated: {results}'