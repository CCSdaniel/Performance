# Rocket Hopper 2D Trajectory Simulator

Python project for simulating a **vertical rocket hopper demonstrator** in 2D (x-z plane) with:

- Vertical launch
- Climb to apogee
- Descent with engine throttled down
- Time-varying mass, center of gravity (CG), and moment of inertia (MoI)

The model includes **gravity + engine thrust** and intentionally excludes aerodynamic forces.

## Key assumptions

- Optimal control keeps the vehicle upright and stabilized at all times.
- No lateral motion command is applied (x stays zero in this baseline model).
- Thrust profile is piecewise:
  - `max_thrust_n` before `throttling_time_s`
  - `throttled_thrust_n` from `throttling_time_s` onward
- CG, MoI, and mass are each defined by 3 points in time:
  - takeoff
  - throttle-down
  - landing
  and interpolated linearly in between.

## Project structure

```text
.
├── config/
│   └── rocket_hopper_config.json
├── sim/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── plotting.py
│   └── simulation.py
├── main.py
└── pyproject.toml
```

## Install

Using pip (recommended):

```bash
python -m pip install -e .
```

Optional dev dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run the simulation

```bash
python main.py
```

Optional arguments:

```bash
python main.py --config config/rocket_hopper_config.json --output-dir outputs --show
```

## Input parameters file

Edit `config/rocket_hopper_config.json`:

- `gravity_m_s2`
- `throttling_time_s`
- `max_thrust_n`
- `throttled_thrust_n`
- `profile_times_s` (`takeoff`, `throttle_down`, `landing`)
- `mass_profile_kg` (`takeoff`, `throttle_down`, `landing`)
- `cg_profile_m` (`takeoff`, `throttle_down`, `landing`)
- `moi_profile_kg_m2` (`takeoff`, `throttle_down`, `landing`)
- `integration.dt_s`
- `integration.max_time_s`

## Monitoring plots generated

At the end of each run, a figure is saved to:

`outputs/rocket_hopper_monitoring.png`

It contains:

1. Vertical position vs time
2. Vertical velocity vs time
3. Mass and CG vs time
4. Thrust vs time
