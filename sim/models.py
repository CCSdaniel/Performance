from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ProfileTriplet:
    takeoff: float
    throttle_down: float
    landing: float

    def as_arrays(self, times: "ProfileTriplet") -> tuple[np.ndarray, np.ndarray]:
        x = np.array([times.takeoff, times.throttle_down, times.landing], dtype=float)
        y = np.array([self.takeoff, self.throttle_down, self.landing], dtype=float)
        return x, y


@dataclass(frozen=True)
class IntegrationConfig:
    dt_s: float
    max_time_s: float


@dataclass(frozen=True)
class SimulationConfig:
    gravity_m_s2: float
    throttling_time_s: float
    max_thrust_n: float
    throttled_thrust_n: float
    profile_times_s: ProfileTriplet
    mass_profile_kg: ProfileTriplet
    cg_profile_m: ProfileTriplet
    moi_profile_kg_m2: ProfileTriplet
    integration: IntegrationConfig


@dataclass(frozen=True)
class SimulationResult:
    time_s: np.ndarray
    x_m: np.ndarray
    z_m: np.ndarray
    vx_m_s: np.ndarray
    vz_m_s: np.ndarray
    mass_kg: np.ndarray
    cg_m: np.ndarray
    moi_kg_m2: np.ndarray
    thrust_n: np.ndarray
