from genshin_calculator.stats import STATS


def test_basic_resolution():
    assert 10 == STATS.ER(10).resolve({})

def test_addition():
    assert 5 == STATS.ATK(STATS.ER).resolve({STATS.ER: 5})
    assert 15 == STATS.ATK(STATS.ER + 10).resolve({STATS.ER: 5})
    assert 7 == STATS.ATK(STATS.ER + STATS.EM).resolve({STATS.ER: 5, STATS.EM: 2})
    assert 17 == STATS.ATK(STATS.ER + STATS.EM + 10).resolve({STATS.ER: 5, STATS.EM: 2})
    assert 17 == STATS.ATK(10 + STATS.ER + STATS.EM).resolve({STATS.ER: 5, STATS.EM: 2})
    assert 17 == STATS.ATK(STATS.ER + 10 + STATS.EM).resolve({STATS.ER: 5, STATS.EM: 2})

def test_multiplication():
    assert 14 == STATS.ATK(STATS.ER * 2).resolve({STATS.ER: 7})
    assert 24 == STATS.ATK(2 * STATS.ER * STATS.EM).resolve({STATS.ER: 3, STATS.EM: 4})
    assert 14 == STATS.ATK(2 * STATS.ER).resolve({STATS.ER: 7})
    assert 24 == STATS.ATK(STATS.ER * 2 * STATS.EM).resolve({STATS.ER: 3, STATS.EM: 4})
    assert 24 == STATS.ATK(STATS.ER * STATS.EM * 2).resolve({STATS.ER: 3, STATS.EM: 4})

def test_mixed_operations():
    assert 30 == STATS.ATK(18 + 6 * STATS.ER).resolve({STATS.ER: 2})
    assert 9 == STATS.ATK(STATS.EM + STATS.ER * STATS.ER).resolve({STATS.ER: 2, STATS.EM: 5})
    assert 30 == STATS.ATK(6 * STATS.ER + 18).resolve({STATS.ER: 2})
    assert 9 == STATS.ATK(STATS.ER * STATS.ER + STATS.EM).resolve({STATS.ER: 2, STATS.EM: 5})
    assert 14 == STATS.ATK((STATS.EM + STATS.ER) * STATS.ER).resolve({STATS.ER: 2, STATS.EM: 5})
    assert 14 == STATS.ATK(STATS.ER * (STATS.ER + STATS.EM)).resolve({STATS.ER: 2, STATS.EM: 5})

def test_division():
    assert 2 == STATS.ATK(STATS.ER / STATS.EM).resolve({STATS.ER: 4, STATS.EM: 2})