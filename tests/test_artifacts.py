from genshin_calculator.artifacts import ARTIFACTS
from genshin_calculator.stats import DmgType, ElementType, STATS


# def test_max_crit_rate_improvement():
#     artifact = ARTIFACTS.RANDOM_ARTIFACT(STATS.CRIT_RATE(0))
#     improved = next(artifact.improve(1))
#     assert False, str(improved.compute(DmgType.ALL, ElementType.ALL))