import math

from genshin_calculator.artifacts import ARTIFACTS
from genshin_calculator.build import Build
from genshin_calculator.characters import WANDERER
from genshin_calculator.stats import DmgType, ElementType, STATS
from genshin_calculator.weapons import CATALYST



def test_wanderer():
    build = WANDERER
    build += CATALYST.FOUR_WINDS()
    build += ARTIFACTS.DESERT_PAVILION(STATS.FLAT_HP(4780),
                                       STATS.FLAT_ATK(19),
                                       STATS.CRIT_RATE(15.2),
                                       STATS.EM(23),
                                       STATS.ATK_PERC(11.7))
    build += ARTIFACTS.DESERT_PAVILION(STATS.FLAT_ATK(311),
                                       STATS.CRIT_RATE(6.6),
                                       STATS.EM(23),
                                       STATS.ATK_PERC(5.8),
                                       STATS.CRIT_DMG(26.4))
    build += ARTIFACTS.DESERT_PAVILION(STATS.ATK_PERC(46.6),
                                       STATS.FLAT_ATK(35),
                                       STATS.DEF_PERC(21.1),
                                       STATS.CRIT_RATE(2.7),
                                       STATS.CRIT_DMG(19.4))
    build += ARTIFACTS.RANDOM_ARTIFACT(STATS.DMG(46.6, ElementType.ANEMO),
                                       STATS.CRIT_RATE(7.4),
                                       STATS.CRIT_DMG(20.2),
                                       STATS.ATK_PERC(9.9),
                                       STATS.FLAT_HP(209))
    build += ARTIFACTS.DESERT_PAVILION(STATS.CRIT_DMG(62.2),
                                       STATS.DEF_PERC(20.4),
                                       STATS.ATK_PERC(10.5),
                                       STATS.FLAT_HP(239),
                                       STATS.FLAT_ATK(31))
    
    REAL_STATS = {STATS.HP: 15392,
                  STATS.BASE_HP: 10164,
                  STATS.ATK: 2123,
                  STATS.BASE_ATK: 936,
                  STATS.DEF: 859,
                  STATS.BASE_DEF: 607,
                  STATS.EM: 47,
                  STATS.CRIT_RATE: 89.2,
                  STATS.CRIT_DMG: 178.3,
                  STATS.ER: 100}
    
    computed_stats = build.compute(DmgType.ALL)
    for k, v in computed_stats.items():
        print('   -', k, ':', v)
    for stat, real_stat_value in REAL_STATS.items():
        print(stat)
        computed_value = computed_stats[stat]
        assert math.isclose(computed_value, real_stat_value, abs_tol=1), (f'Wrong {stat} value. '
                                                                             f'Given: {computed_value} ; '
                                                                             f'Expected: {real_stat_value}.')
    
