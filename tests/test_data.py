from genshin_calculator.data import TRANSFORMATIVE_REACTION_MULTIPLIERS


def test_increasing_value():
    previous_value = 0
    for lvl in sorted(TRANSFORMATIVE_REACTION_MULTIPLIERS):
        current_value = TRANSFORMATIVE_REACTION_MULTIPLIERS[lvl]
        assert current_value >= previous_value, f"Decreasing value for level {lvl}."
        previous_value = current_value