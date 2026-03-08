from __future__ import annotations

from pathlib import Path

import numpy as np

from sim.config import load_simulation_config
from sim.simulation import run_simulation


def test_simulation_reaches_apogee_and_touchdown() -> None:
    cfg = load_simulation_config(Path("config/rocket_hopper_config.json"))
    result = run_simulation(cfg)

    assert result.time_s.size > 10
    assert np.all(np.diff(result.time_s) > 0)
    assert np.max(result.z_m) > 0.0
    assert result.z_m[-1] == 0.0
    assert result.vz_m_s[-1] < 0.0
