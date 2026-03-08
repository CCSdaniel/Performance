from __future__ import annotations

from math import sqrt

import numpy as np

from sim.models import ProfileTriplet, SimulationConfig, SimulationResult


def _interp_triplet(t_s: float, times: ProfileTriplet, values: ProfileTriplet) -> float:
    x, y = values.as_arrays(times)
    return float(np.interp(t_s, x, y))


def _thrust_command(t_s: float, config: SimulationConfig) -> float:
    if t_s < config.throttling_time_s:
        return config.max_thrust_n
    return config.throttled_thrust_n


def _touchdown_time(z0: float, vz0: float, az: float, dt_s: float) -> float:
    """
    Return time-to-ground in [0, dt_s] for z(t)=z0+vz0*t+0.5*az*t^2.
    Falls back to dt_s if numerical issues appear.
    """
    if abs(az) < 1e-12:
        if abs(vz0) < 1e-12:
            return dt_s
        tau = -z0 / vz0
        return min(max(tau, 0.0), dt_s)

    a = 0.5 * az
    b = vz0
    c = z0
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0:
        return dt_s

    root = sqrt(discriminant)
    tau1 = (-b - root) / (2.0 * a)
    tau2 = (-b + root) / (2.0 * a)
    candidates = [tau for tau in (tau1, tau2) if 0.0 <= tau <= dt_s]
    if not candidates:
        return dt_s
    return min(candidates)


def run_simulation(config: SimulationConfig) -> SimulationResult:
    dt = config.integration.dt_s
    max_time = config.integration.max_time_s
    g = config.gravity_m_s2

    t = 0.0
    x = 0.0
    z = 0.0
    vx = 0.0
    vz = 0.0

    time_s = [t]
    x_m = [x]
    z_m = [z]
    vx_m_s = [vx]
    vz_m_s = [vz]
    mass_kg = [_interp_triplet(t, config.profile_times_s, config.mass_profile_kg)]
    cg_m = [_interp_triplet(t, config.profile_times_s, config.cg_profile_m)]
    moi_kg_m2 = [_interp_triplet(t, config.profile_times_s, config.moi_profile_kg_m2)]
    thrust_n = [_thrust_command(t, config)]

    while t < max_time:
        m = _interp_triplet(t, config.profile_times_s, config.mass_profile_kg)
        thrust = _thrust_command(t, config)
        az = thrust / m - g

        x_next = x + vx * dt
        z_next = z + vz * dt + 0.5 * az * dt * dt
        vx_next = vx
        vz_next = vz + az * dt

        # Stop exactly at first touchdown after liftoff.
        if z_next <= 0.0 and t > 0.0 and vz_next < 0.0:
            tau = _touchdown_time(z, vz, az, dt)
            t_touch = t + tau
            z_touch = 0.0
            vz_touch = vz + az * tau

            time_s.append(t_touch)
            x_m.append(x + vx * tau)
            z_m.append(z_touch)
            vx_m_s.append(vx)
            vz_m_s.append(vz_touch)
            mass_kg.append(_interp_triplet(t_touch, config.profile_times_s, config.mass_profile_kg))
            cg_m.append(_interp_triplet(t_touch, config.profile_times_s, config.cg_profile_m))
            moi_kg_m2.append(_interp_triplet(t_touch, config.profile_times_s, config.moi_profile_kg_m2))
            thrust_n.append(_thrust_command(t_touch, config))
            break

        t += dt
        x, z, vx, vz = x_next, max(0.0, z_next), vx_next, vz_next

        time_s.append(t)
        x_m.append(x)
        z_m.append(z)
        vx_m_s.append(vx)
        vz_m_s.append(vz)
        mass_kg.append(_interp_triplet(t, config.profile_times_s, config.mass_profile_kg))
        cg_m.append(_interp_triplet(t, config.profile_times_s, config.cg_profile_m))
        moi_kg_m2.append(_interp_triplet(t, config.profile_times_s, config.moi_profile_kg_m2))
        thrust_n.append(_thrust_command(t, config))

    return SimulationResult(
        time_s=np.asarray(time_s, dtype=float),
        x_m=np.asarray(x_m, dtype=float),
        z_m=np.asarray(z_m, dtype=float),
        vx_m_s=np.asarray(vx_m_s, dtype=float),
        vz_m_s=np.asarray(vz_m_s, dtype=float),
        mass_kg=np.asarray(mass_kg, dtype=float),
        cg_m=np.asarray(cg_m, dtype=float),
        moi_kg_m2=np.asarray(moi_kg_m2, dtype=float),
        thrust_n=np.asarray(thrust_n, dtype=float),
    )
