import math

from genshin_calculator.artifacts import ARTIFACTS
from genshin_calculator.build import Build
from genshin_calculator.characters import Neuvilette
from genshin_calculator.rotation import Rotation
from genshin_calculator.stats import STATS, DmgType, ElementType 
from genshin_calculator.weapons import CATALYST



WEAPON = CATALYST.PROTOTYPE_AMBER()

FLOWER = ARTIFACTS.MARECHAUSSE_HUNTER(STATS.FLAT_HP(4780), STATS.CRIT_RATE(6.6), STATS.CRIT_DMG(21.0), STATS.ER(15.5))
FEATHER = ARTIFACTS.MARECHAUSSE_HUNTER(STATS.FLAT_ATK(311), STATS.CRIT_RATE(10.9), STATS.ER(18.1), STATS.CRIT_DMG(7.0))
SAND = ARTIFACTS.RANDOM_ARTIFACT(STATS.HP_PERC(46.6), STATS.ER(5.8), STATS.CRIT_RATE(8.6), STATS.CRIT_DMG(5.4))
CUP = ARTIFACTS.MARECHAUSSE_HUNTER(STATS.DMG(46.6, ElementType.HYDRO), STATS.CRIT_RATE(9.7), STATS.CRIT_DMG(13.2), STATS.EM(42))
HELMET = ARTIFACTS.MARECHAUSSE_HUNTER(STATS.CRIT_DMG(62.2), STATS.CRIT_RATE(7), STATS.ER(20.7))

STUFF = {'weapons': WEAPON,
         'flowers': FLOWER,
         'feathers': FEATHER,
         'sands': SAND,
         'cups': CUP,
         'helmets': HELMET}

def test_solo():
    neuvillette = Neuvilette(**STUFF,
                             team_bonuses=Build(STATS.CRIT_RATE(100)))
    rotation = Rotation(neuvillette.attack(DmgType.CHARGED, ElementType.HYDRO, pv_mult=0.1447))
    results = rotation.compute(resistances=10, ennemy_lvl=103)[0]

    assert math.isclose(results, 11614, rel_tol=3e-4), f'Damages calculated: {results}'


def test_oz():
    neuvillette = Neuvilette(**STUFF,
                             team_bonuses=Build(STATS.CRIT_RATE(100),
                                                STATS.MULTIPLIER_PERC(10)))
    rotation = Rotation(neuvillette.attack(DmgType.CHARGED, ElementType.HYDRO, pv_mult=0.1447))
    results = rotation.compute(resistances=10, ennemy_lvl=103)[0]

    assert math.isclose(results, 12775, rel_tol=3e-4), f'Damages calculated: {results}'


def test_oz_baizhu():
    neuvillette = Neuvilette(**STUFF,
                             team_bonuses=Build(STATS.CRIT_RATE(100),
                                                STATS.MULTIPLIER_PERC(25)))
    rotation = Rotation(neuvillette.attack(DmgType.CHARGED, ElementType.HYDRO, pv_mult=0.1447))
    results = rotation.compute(resistances=10, ennemy_lvl=103)[0]

    assert math.isclose(results, 14517, rel_tol=3e-4), f'Damages calculated: {results}'


def test_sucrose_NA():
    neuvillette = Neuvilette(**STUFF,
                             team_bonuses=Build(STATS.CRIT_RATE(100),
                                                STATS.RES_SHRED(40),
                                                STATS.MULTIPLIER_PERC(10)))
    rotation = Rotation(neuvillette.attack(DmgType.CHARGED, ElementType.HYDRO, pv_mult=0.1447))
    results = rotation.compute(resistances=10, ennemy_lvl=103)[0]

    assert math.isclose(results, 16324, rel_tol=3e-4), f'Damages calculated: {results}'

def test_all():
    neuvillette = Neuvilette(**STUFF,
                             team_bonuses=Build(STATS.CRIT_RATE(100),
                                                STATS.RES_SHRED(40),
                                                STATS.MULTIPLIER_PERC(60)))
    rotation = Rotation(neuvillette.attack(DmgType.CHARGED, ElementType.HYDRO, pv_mult=0.1447))
    results = rotation.compute(resistances=10, ennemy_lvl=103)[0]

    assert math.isclose(results, 23744, rel_tol=3e-4), f'Damages calculated: {results}'