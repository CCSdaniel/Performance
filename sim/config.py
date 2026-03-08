from __future__ import annotations

import json
from pathlib import Path

from sim.models import IntegrationConfig, ProfileTriplet, SimulationConfig


def _build_triplet(data: dict[str, float], field_name: str) -> ProfileTriplet:
    required = ("takeoff", "throttle_down", "landing")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing keys in '{field_name}': {missing}")
    return ProfileTriplet(
        takeoff=float(data["takeoff"]),
        throttle_down=float(data["throttle_down"]),
        landing=float(data["landing"]),
    )


def load_simulation_config(path: str | Path) -> SimulationConfig:
    config_path = Path(path)
    raw = json.loads(config_path.read_text(encoding="utf-8"))

    profile_times = _build_triplet(raw["profile_times_s"], "profile_times_s")
    mass_profile = _build_triplet(raw["mass_profile_kg"], "mass_profile_kg")
    cg_profile = _build_triplet(raw["cg_profile_m"], "cg_profile_m")
    moi_profile = _build_triplet(raw["moi_profile_kg_m2"], "moi_profile_kg_m2")

    if not (profile_times.takeoff <= profile_times.throttle_down <= profile_times.landing):
        raise ValueError("profile_times_s must be in ascending order: takeoff <= throttle_down <= landing.")

    integration = IntegrationConfig(
        dt_s=float(raw["integration"]["dt_s"]),
        max_time_s=float(raw["integration"]["max_time_s"]),
    )
    if integration.dt_s <= 0.0:
        raise ValueError("integration.dt_s must be > 0.")
    if integration.max_time_s <= 0.0:
        raise ValueError("integration.max_time_s must be > 0.")

    cfg = SimulationConfig(
        gravity_m_s2=float(raw["gravity_m_s2"]),
        throttling_time_s=float(raw["throttling_time_s"]),
        max_thrust_n=float(raw["max_thrust_n"]),
        throttled_thrust_n=float(raw["throttled_thrust_n"]),
        profile_times_s=profile_times,
        mass_profile_kg=mass_profile,
        cg_profile_m=cg_profile,
        moi_profile_kg_m2=moi_profile,
        integration=integration,
    )

    if cfg.max_thrust_n <= 0.0 or cfg.throttled_thrust_n < 0.0:
        raise ValueError("Thrust values must be non-negative, and max thrust must be > 0.")
    if cfg.throttled_thrust_n > cfg.max_thrust_n:
        raise ValueError("throttled_thrust_n must be <= max_thrust_n.")
    if cfg.gravity_m_s2 <= 0.0:
        raise ValueError("gravity_m_s2 must be > 0.")
    if min(cfg.mass_profile_kg.takeoff, cfg.mass_profile_kg.throttle_down, cfg.mass_profile_kg.landing) <= 0.0:
        raise ValueError("All mass profile values must be > 0.")

    return cfg
