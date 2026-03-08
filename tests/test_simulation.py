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


def test_t_landing_controls_profile_interpolation_endpoint() -> None:
    cfg = load_simulation_config(Path("config/rocket_hopper_config.json"))
    result = run_simulation(cfg)

    assert cfg.t_landing_s == 60.0
    assert cfg.profile_times_s.landing == cfg.t_landing_s

    idx = int(np.argmin(np.abs(result.time_s - cfg.t_landing_s)))
    assert np.isclose(result.time_s[idx], cfg.t_landing_s, atol=cfg.integration.dt_s)
    assert np.isclose(result.mass_kg[idx], cfg.mass_profile_kg.landing, atol=1e-6)
    assert np.isclose(result.cg_m[idx], cfg.cg_profile_m.landing, atol=1e-6)
    assert np.isclose(result.moi_kg_m2[idx], cfg.moi_profile_kg_m2.landing, atol=1e-6)
