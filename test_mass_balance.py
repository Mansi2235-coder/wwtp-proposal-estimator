import pytest
from mass_balance import pollutant_load, removed_load, sludge_production, tank_volume,oxygen_demand

def test_pollutant_load():
    assert pollutant_load(10000, 250) == 2500


def test_removed_load():
    assert removed_load(10000, 250, 20) == 2300

def test_sludge_production():
    result = sludge_production(10000, 250, 20, 0.6, 0.08, 10)
    assert result == pytest.approx(766.7, abs=0.1)


def test_tank_volume():
    result = tank_volume(10000, 250, 20, 0.6, 0.08, 10, 2500)
    assert result == pytest.approx(3066.7, abs=0.1)

def test_oxygen_demand():
    result = oxygen_demand(10000, 250, 20, 0.6, 0.08, 10, 0.68)
    assert result == pytest.approx(2293.7, abs=0.1)