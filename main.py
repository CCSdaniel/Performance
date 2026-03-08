from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from sim.config import load_simulation_config
from sim.plotting import create_monitoring_plots
from sim.simulation import run_simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="2D rocket hopper flight trajectory simulation.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/rocket_hopper_config.json"),
        help="Path to simulation input JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory where monitoring plots are saved.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display plots interactively in addition to saving them.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_simulation_config(args.config)
    result = run_simulation(config)

    apogee_idx = int(np.argmax(result.z_m))
    apogee_altitude = float(result.z_m[apogee_idx])
    apogee_time = float(result.time_s[apogee_idx])
    touchdown_time = float(result.time_s[-1])
    touchdown_speed = float(result.vz_m_s[-1])

    fig_path = create_monitoring_plots(result, output_dir=args.output_dir, show=args.show)

    print("Simulation complete")
    print(f"  Config file: {args.config}")
    print(f"  Apogee: {apogee_altitude:.2f} m at t={apogee_time:.2f} s")
    print(f"  Touchdown: t={touchdown_time:.2f} s, vertical speed={touchdown_speed:.2f} m/s")
    print(f"  Monitoring plots saved to: {fig_path}")


if __name__ == "__main__":
    main()
