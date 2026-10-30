"""Local Tk interface. Rendering and wall-clock cadence never change physics."""

from dataclasses import replace
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from taxishare.config import Config
from taxishare.scenario import generate
from taxishare.model import TaxiShareModel
from taxishare.metrics import export_results, summary
from taxishare.visualization import create_figure, draw_model

LABELS = {
    "taxis": "Taxis",
    "requests": "Requests", "appearance_seconds": "Arrivals until (s)",
    "capacity": "Seats per taxi", "seed": "Seed",
}


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("TaxiShare | Mesa multi-agent simulation")
        # Tk reports logical pixels under Windows display scaling. A fixed
        # 1400x900 window can extend off-screen and hide the bottom legends.
        width = min(1400, self.root.winfo_screenwidth() - 60)
        height = min(900, self.root.winfo_screenheight() - 100)
        self.root.geometry(f"{width}x{height}")
        self.playing = False
        self.model = TaxiShareModel(generate(Config()))
        self.model.scenario.save(Path(__file__).parent / "output/gui/scenario.json")
        self.inputs = {}
        self.speed = tk.IntVar(value=10)
        self.status = tk.StringVar()
        self._build_controls()
        self.figure = create_figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        self.refresh()
        self.root.after(40, self.pump)

    def _build_controls(self):
        panel = ttk.Frame(self.root, padding=14)
        panel.pack(side="left", fill="y")
        ttk.Label(panel, text="TAXISHARE", font=("Segoe UI", 19, "bold")).pack(anchor="w")
        ttk.Label(panel, text="Shared taxis in a generated city").pack(anchor="w", pady=(2, 12))
        for label, callback in (("Start / Pause", self.toggle), ("Advance by 0.2 s", self.single_step),
                                ("Replay scenario", self.replay),
                                ("Export results", self.export)):
            ttk.Button(panel, text=label, command=callback).pack(fill="x", pady=2)
        ttk.Label(panel, text="Animation speed").pack(anchor="w", pady=(12, 0))
        ttk.Spinbox(panel, from_=1, to=500, textvariable=self.speed, width=12).pack(fill="x")
        ttk.Separator(panel).pack(fill="x", pady=12)
        form = ttk.Frame(panel)
        form.pack(fill="x")
        for row, (name, label) in enumerate(LABELS.items()):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=2)
            variable = tk.StringVar(value=str(getattr(self.model.config, name)))
            self.inputs[name] = variable
            ttk.Entry(form, textvariable=variable, width=10).grid(row=row, column=1, padx=(8, 0))
        ttk.Button(panel, text="Generate with these parameters", command=self.new_scenario).pack(fill="x", pady=10)
        ttk.Label(panel, textvariable=self.status, wraplength=260, justify="left").pack(anchor="w", pady=8)

    def toggle(self):
        if self.model.running:
            self.playing = not self.playing
        self.refresh()

    def single_step(self):
        self.playing = False
        self._advance_safely()
        self.refresh()

    def _advance_safely(self):
        try:
            self.model.step()
        except Exception as exc:
            self.playing = False
            messagebox.showerror("Simulation interrupted", f"{type(exc).__name__}: {exc}")
            raise

    def pump(self):
        """Bound GUI work per callback; never sleep to represent simulated time."""
        if self.playing and self.model.running:
            # Check the wall-clock budget BETWEEN complete simulation ticks.
            # A costly planning tick can exceed it; interrupting half a tick
            # would leave negotiations and physical updates inconsistent.
            deadline = time.perf_counter() + 0.035
            try:
                steps = max(1, min(500, self.speed.get()))
            except (ValueError, tk.TclError):
                steps = 1
            for _ in range(steps):
                self._advance_safely()
                if not self.model.running or time.perf_counter() >= deadline:
                    break
            self.refresh()
        self.root.after(40, self.pump)

    def refresh(self):
        draw_model(self.figure, self.model)
        self.canvas.draw_idle()
        values = summary(self.model)
        state = "Running" if self.playing and self.model.running else "Paused"
        if not self.model.running:
            state = "Complete" if self.model.status == "complete" else "Incomplete"
        self.status.set(f"{state} | {self.model.time_seconds:.1f} s\n"
                        f"Delivered: {values['delivered_count']} / {values['planned_count']}\n"
                        f"Distance: {values['distance_total_m'] / 1000:.2f} km\n"
                        f"Stop reason: {self.model.stop_reason or '-'}")

    def set_scenario(self, scenario):
        # Rebuild every agent and counter from saved exogenous inputs. Replaying
        # must not reuse current commitments or draw a different random city.
        self.playing = False
        self.model = TaxiShareModel(scenario)
        scenario.save(Path(__file__).parent / "output/gui/scenario.json")
        for name, variable in self.inputs.items():
            variable.set(str(getattr(scenario.config, name)))
        self.refresh()

    def new_scenario(self):
        try:
            values = {name: type(Config.__dataclass_fields__[name].default)(variable.get())
                      for name, variable in self.inputs.items()}
            # Editing the main controls must preserve the current map settings,
            # detour limits and other parameters that are not shown in the form.
            self.set_scenario(generate(replace(self.model.config, **values)))
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Invalid configuration", str(exc))

    def replay(self):
        self.set_scenario(self.model.scenario)

    def export(self):
        self.playing = False
        directory = filedialog.askdirectory(title="Export directory")
        if directory:
            try:
                export_results(self.model, directory)
                messagebox.showinfo("Export complete", directory)
            except OSError as exc:
                messagebox.showerror("Export failed", str(exc))
        self.refresh()


def main():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
