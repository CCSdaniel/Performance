from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from sim.models import SimulationResult


def create_monitoring_plots(result: SimulationResult, output_dir: str | Path, show: bool = False) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(4, 1, figsize=(10, 14), sharex=True, constrained_layout=True)

    # 1) Vertical position vs time
    axes[0].plot(result.time_s, result.z_m, color="tab:blue")
    axes[0].set_ylabel("Position z [m]")
    axes[0].set_title("Vertical Position vs Time")
    axes[0].grid(True, alpha=0.3)

    # 2) Vertical velocity vs time
    axes[1].plot(result.time_s, result.vz_m_s, color="tab:orange")
    axes[1].set_ylabel("Velocity vz [m/s]")
    axes[1].set_title("Vertical Velocity vs Time")
    axes[1].grid(True, alpha=0.3)

    # 3) Mass and CG vs time
    ax_mass = axes[2]
    ax_cg = ax_mass.twinx()
    line_mass = ax_mass.plot(result.time_s, result.mass_kg, color="tab:green", label="Mass [kg]")
    line_cg = ax_cg.plot(result.time_s, result.cg_m, color="tab:red", label="CG [m]")

    ax_mass.set_ylabel("Mass [kg]")
    ax_cg.set_ylabel("CG from engine pivot [m]")
    ax_mass.set_title("Mass and CG vs Time")
    ax_mass.grid(True, alpha=0.3)

    handles = line_mass + line_cg
    labels = [h.get_label() for h in handles]
    ax_mass.legend(handles, labels, loc="best")

    # 4) Thrust vs time
    axes[3].plot(result.time_s, result.thrust_n, color="tab:purple")
    axes[3].set_ylabel("Thrust [N]")
    axes[3].set_xlabel("Time [s]")
    axes[3].set_title("Thrust vs Time")
    axes[3].grid(True, alpha=0.3)

    figure_path = output_path / "rocket_hopper_monitoring.png"
    fig.savefig(figure_path, dpi=150)

    if show:
        plt.show()
    plt.close(fig)
    return figure_path
