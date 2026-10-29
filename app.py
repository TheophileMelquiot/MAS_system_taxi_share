"""Local Tk interface. Rendering and wall-clock cadence never change physics."""

import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from taxishare.config import Config
from taxishare.scenario import generate, Scenario
from taxishare.model import TaxiShareModel
from taxishare.metrics import export_results, summary
from taxishare.visualization import create_figure, draw_model

LABELS = {
    "width": "Largeur (cellules)", "height": "Hauteur (cellules)",
    "horizontal_axes": "Axes horizontaux", "vertical_axes": "Axes verticaux",
    "axis_spacing": "Espacement minimal", "buildings": "Bâtiments", "taxis": "Taxis",
    "requests": "Demandes", "appearance_seconds": "Apparitions jusqu'à (s)",
    "capacity": "Places par taxi", "congestion_threshold": "Seuil de fluidité K",
    "detour_rate": "Taux de détour", "detour_cap_m": "Plafond de détour (m)",
    "seed": "Graine", "max_seconds": "Plafond technique (s)",
}


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("TaxiShare | Simulation multi-agents Mesa")
        self.root.geometry("1400x900")
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
        ttk.Label(panel, text="Un monde · Agents autonomes\nHorloge commune : 0,2 s").pack(anchor="w", pady=(2, 12))
        for label, callback in (("Démarrer / Pause", self.toggle), ("Avancer de 0,2 s", self.single_step),
                                ("Rejouer ce scénario", self.replay), ("Charger un scénario", self.load),
                                ("Exporter les résultats", self.export)):
            ttk.Button(panel, text=label, command=callback).pack(fill="x", pady=2)
        ttk.Label(panel, text="Pas par rafraîchissement").pack(anchor="w", pady=(12, 0))
        ttk.Spinbox(panel, from_=1, to=500, textvariable=self.speed, width=12).pack(fill="x")
        ttk.Separator(panel).pack(fill="x", pady=12)
        form = ttk.Frame(panel)
        form.pack(fill="x")
        for row, (name, field) in enumerate(Config.__dataclass_fields__.items()):
            ttk.Label(form, text=LABELS[name]).grid(row=row, column=0, sticky="w", pady=2)
            variable = tk.StringVar(value=str(getattr(self.model.config, name)))
            self.inputs[name] = variable
            ttk.Entry(form, textvariable=variable, width=10).grid(row=row, column=1, padx=(8, 0))
        ttk.Button(panel, text="Générer avec ces paramètres", command=self.new_scenario).pack(fill="x", pady=10)
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
            messagebox.showerror("Simulation interrompue", f"{type(exc).__name__}: {exc}")
            raise

    def pump(self):
        """Bound GUI work per callback; never sleep to represent simulated time."""
        if self.playing and self.model.running:
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
        state = "En cours" if self.playing and self.model.running else "En pause"
        if not self.model.running:
            state = "Terminé" if self.model.status == "complete" else "Incomplet"
        self.status.set(f"{state} | {self.model.time_seconds:.1f} s\n"
                        f"Livrés : {values['delivered_count']} / {values['planned_count']}\n"
                        f"Distance : {values['distance_total_m'] / 1000:.2f} km\n"
                        f"Cause d'arrêt : {self.model.stop_reason or '-'}")

    def set_scenario(self, scenario):
        self.playing = False
        self.model = TaxiShareModel(scenario)
        scenario.save(Path(__file__).parent / "output/gui/scenario.json")
        for name, variable in self.inputs.items():
            variable.set(str(getattr(scenario.config, name)))
        self.refresh()

    def new_scenario(self):
        try:
            values = {name: type(field.default)(self.inputs[name].get())
                      for name, field in Config.__dataclass_fields__.items()}
            self.set_scenario(generate(Config(**values)))
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Configuration invalide", str(exc))

    def replay(self):
        self.set_scenario(self.model.scenario)

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Scénario JSON", "*.json")])
        if path:
            try:
                self.set_scenario(Scenario.load(path))
            except (ValueError, OSError) as exc:
                messagebox.showerror("Scénario invalide", str(exc))

    def export(self):
        self.playing = False
        directory = filedialog.askdirectory(title="Dossier des exports")
        if directory:
            try:
                export_results(self.model, directory)
                messagebox.showinfo("Export terminé", directory)
            except OSError as exc:
                messagebox.showerror("Export impossible", str(exc))
        self.refresh()


def main():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
