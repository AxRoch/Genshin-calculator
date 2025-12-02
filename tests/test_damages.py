import math

from genshin_calculator.build import Build
from genshin_calculator.characters import Character
from genshin_calculator.reactions import OVERLOAD, REVERSE_MELT, REVERSE_VAPORIZE
from genshin_calculator.rotation import Rotation
from genshin_calculator.stats import STATS, DmgType, ElementType

# Examples taken from https://www.youtube.com/watch?v=ai1JgPe1ue4&list=WL&index=45


def test_razor_1():
    razor = Character(level=81,
                      default_build=Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3, ElementType.PHYSICAL),
                                          STATS.CRIT_RATE(100), STATS.CRIT_DMG(146.4)))
    rotation = Rotation(razor.attack(DmgType.NORMAL, ElementType.PHYSICAL, 1.52))
    damage = rotation.compute(resistances=70, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 3078, rel_tol=3e-4), f'Damages calculated: {results}'


def test_razor_2():
    razor = Character(level=81,
                      default_build=Build(STATS.FLAT_ATK(2325), STATS.DMG(138.3, ElementType.PHYSICAL),
                                          STATS.CRIT_RATE(100), STATS.CRIT_DMG(146.4),
                                          STATS.DMG(10), STATS.DEF_SHRED(15)))
    rotation = Rotation(razor.attack(DmgType.NORMAL, ElementType.PHYSICAL, 1.52))
    damage = rotation.compute(resistances=70, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 3471, rel_tol=3e-4), f'Damages calculated: {results}'


def test_hu_tao():
    hu_tao = Character(level=82,
                       default_build=Build(STATS.FLAT_ATK(1069 + 0.0566 * STATS.FLAT_HP),
                                           STATS.DMG(61.6 + 33 + 7.5, ElementType.PYRO),
                                           STATS.DMG(48, DmgType.NORMAL),
                                           STATS.FLAT_HP(30830),
                                           STATS.CRIT_RATE(100), STATS.CRIT_DMG(143.64)))
    
    rotation = Rotation(hu_tao.attack(DmgType.NORMAL, ElementType.PYRO, 0.741))
    damage = rotation.compute(resistances=10, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 5670, rel_tol=3e-4), f'Damages calculated: {results}'

    rotation = Rotation(hu_tao.attack(DmgType.CHARGED, ElementType.PYRO, 2.148))
    damage = rotation.compute(resistances=10, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 13282, rel_tol=3e-4), f'Damages calculated: {results}'


def test_rosaria():
    rosaria = Character(level=81,
                      default_build=Build(STATS.ATK(1420),
                                          STATS.FLAT_DMG(0.2 * STATS.ATK),
                                          STATS.DMG(86.7, ElementType.PHYSICAL),
                                          STATS.CRIT_RATE(100), STATS.CRIT_DMG(107.5)))
    
    rotation = Rotation(rosaria.attack(DmgType.NORMAL, ElementType.PHYSICAL, 0.))
    damage = rotation.compute(resistances=70, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 163, rel_tol=5e-3), f'Damages calculated: {results}'


def test_kokomi():
    kokomi = Character(level=81,
                       default_build=Build(STATS.ATK(1333),
                                           STATS.HP(30668),
                                           STATS.FLAT_DMG(0.077 * STATS.HP, DmgType.NORMAL),
                                           STATS.FLAT_DMG(0.15 * STATS.HEALING_BONUS * STATS.HP / 100,
                                                          DmgType.NORMAL | DmgType.CHARGED),
                                           STATS.DMG(75.4, ElementType.HYDRO),
                                           STATS.HEALING_BONUS(75.9),
                                           STATS.CRIT_RATE(0)))
    
    rotation = Rotation(kokomi.attack(DmgType.NORMAL, ElementType.HYDRO, 1.094))
    damage = rotation.compute(resistances=10, ennemy_lvl=85)
    results = sum(damage)
    assert math.isclose(results, 5707, rel_tol=5e-3), f'Damages calculated: {results}'


def test_chongyun():
    chongyun = Character(level=81,
                         default_build=Build(STATS.ATK(1707),
                                             STATS.EM(54),
                                             STATS.DMG(61.6, ElementType.CRYO), STATS.DMG(30),
                                             STATS.CRIT_RATE(100), STATS.CRIT_DMG(163.5)))
    
    rotation = Rotation(chongyun.attack(DmgType.NORMAL, ElementType.CRYO, 3.27))
    damage = rotation.compute(resistances=10, ennemy_lvl=85, reaction=REVERSE_MELT)
    results = sum(damage)
    assert math.isclose(results, 20752, rel_tol=5e-3), f'Damages calculated: {results}'


def test_chongyun():
    chongyun = Character(level=81,
                         default_build=Build(STATS.ATK(3333),
                                             STATS.EM(223),
                                             STATS.DMG(61.6), STATS.DMG(30),
                                             STATS.CRIT_RATE(100), STATS.CRIT_DMG(163.5),
                                             STATS.FLAT_DMG(0.73 * 3761), STATS.DMG(15, DmgType.SKILL | DmgType.BURST),
                                             STATS.RES_SHRED(40)))
    
    rotation = Rotation(chongyun.attack(DmgType.SKILL, ElementType.CRYO, 3.27))
    damage = rotation.compute(resistances=10, ennemy_lvl=85, reaction=REVERSE_MELT)
    results = sum(damage)
    assert math.isclose(results, 87361, rel_tol=5e-3), f'Damages calculated: {results}'


def test_yoimiya():
    NB_HITS = 0
    CURIOSITY_STACKS = 0
    yunjin = Character(level=90, default_build=Build(STATS.DEF((1 + CURIOSITY_STACKS * 0.06 + 0.2) * 689 + 1504)))
    yoimiya = Character(level=81,
                        default_build=Build(STATS.ATK(2378),
                                            STATS.EM(117),
                                            STATS.DMG(46.6, ElementType.PYRO),
                                            STATS.DMG(50, DmgType.NORMAL | DmgType.CHARGED),
                                            STATS.DMG(NB_HITS * 2, ElementType.PYRO),
                                            STATS.FLAT_DMG((0.61 + 0.075) * yunjin[STATS.DEF], DmgType.NORMAL),
                                            STATS.DMG(15, DmgType.NORMAL),
                                            STATS.MULTIPLIER_PERC(58.8, DmgType.NORMAL),
                                            STATS.CRIT_RATE(100), STATS.CRIT_DMG(193.6)))
    
    rotation = Rotation(yoimiya.attack(DmgType.NORMAL, ElementType.PYRO, 0.599))
    damage = rotation.compute(resistances=10, ennemy_lvl=85, reaction=REVERSE_VAPORIZE)
    results = sum(damage)
    assert math.isclose(results, 19438, rel_tol=5e-3), f'Damages calculated: {results}'


def test_diluc_transformative():
    diluc = Character(level=81,
                      default_build=Build(STATS.ATK(0),
                                          STATS.EM(293),
                                          STATS.REACTION_DMG_BONUS(40),
                                          STATS.RES_SHRED(40)))
    
    rotation = Rotation(diluc.attack(DmgType.SKILL, ElementType.PYRO, 3.27))
    damage = rotation.compute(resistances=10, ennemy_lvl=85, reaction=OVERLOAD)
    results = sum(damage)
    assert math.isclose(results, 8790, rel_tol=5e-3), f'Damages calculated: {results}'