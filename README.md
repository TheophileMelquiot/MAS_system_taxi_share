# TaxiShare: shared-taxi simulation with Mesa

TaxiShare compares individual taxi service with shared rides on a generated
road network. Passengers request a taxi, compare offers and wait for a confirmed
assignment. Taxis plan feasible pickups and drops while respecting seat capacity,
individual detour budgets and previously promised approach distances.

The model uses Mesa agents, `AgentSet` activation, a non-toroidal `MultiGrid`
and `DataCollector`. A common clock advances in 0.2-second intervals.

## Which file should I run?

Run commands from the repository root, using its Python environment.

| Entry point | Purpose | When to use it |
| --- | --- | --- |
| `app.py` | Open the interactive desktop application | Explore the city, watch taxis, change parameters and export a run |
| `run_simulation.py` | Run one simulation without a window | Try a configuration or generate detailed results automatically |
| `run_experiments.py` | Compare capacities 1 and 3 on matched inputs | Reproduce the experiment and collect results for analysis |
| `python -m pytest` | Run the checks in `tests/` | Verify the implementation after a change; optional for normal use |

The files in `taxishare/` are imported library modules. Do not run them
individually. In particular, `scenario.py` generates the inputs used by all
three entry points and is required to run the project.

## Installation

Python 3.11 or later is required; Python 3.12 is the tested version. The desktop
application also requires Tkinter. From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The two direct dependencies, Mesa and Matplotlib, are pinned in
`requirements.txt`. `requirements-lock.txt` records the full environment used
for validation. An existing local `.venv` can be reused without reinstalling.

## Explore one simulation

```powershell
.\.venv\Scripts\python.exe app.py
```

The application opens with the default city and demands. Its controls are:

- **Start / Pause**: start or pause animation.
- **Advance by 0.2 s**: process one model step, including finalizations due at
  the current boundary. A terminal step may finish without advancing time.
- **Replay scenario**: reset agents and counters using the same generated inputs.
- **Generate with these parameters**: create new inputs using the five fields:
  taxis, requests, arrival window, seats per taxi and seed.
- **Export results**: pause and save the current state, even if it is incomplete.

Changing a field does not change the current model until generation is requested.
Other settings, such as map dimensions and detour limits, remain in `Config` and
are preserved when generating from the interface. The animation speed controls
simulation ticks per redraw; it does not change the physical duration of a tick.

Each taxi is a triangle showing its current movement direction or last arrival
heading while parked. Gray means empty and available, orange means empty with
bookings, and green means carrying passengers. Waiting passengers are red dots;
confirmed passengers waiting to board are blue dots. Visual offsets separate
people sharing an access without changing their simulated positions.

The city shows square cell boundaries, white road cells and green land cells.
One cell measures 100 m per side; dark squares mark buildings. A taxi label such
as `T2 (1/3)` identifies taxi 2 with one occupied seat out of three. The same
three taxi colors and two passenger colors are used throughout the dashboard.

The **Map** legend identifies buildings, road-access dots and the solid lines
linking buildings to their fixed pickup/drop cells. Passengers wait at those
road accesses because taxis cannot drive into building cells. They appear
directly at the access; walking from the building is not simulated. Dashed
lines connect visually offset passenger dots to their actual waiting access.
Those offsets prevent overlap and do not move passengers to another cell.

The GUI saves its current inputs to `output/gui/scenario.json`. Replay uses the
scenario already held in memory. Loading a saved scenario file is not supported.

## Generate another map or repeat the same inputs

Change **Seed** (for example, from 2026 to 2027) and click **Generate with these
parameters** to draw another city and demand set. Repeat with other seeds to
explore new inputs. The set of possible cities is finite, so different seeds
are not a mathematical guarantee of unique road layouts.

Using the same seed, parameters and generator version recreates the same inputs.
Clicking Generate again without changing them intentionally reproduces the same
scenario. Use **Replay scenario** to reset the current inputs directly.

Separate random streams control the map, fleet, trips and arrival times. Changing
capacity does not redraw the city or demands; changing taxi count does not redraw
the city or passenger requests. Map dimensions and axis counts can be changed
through `Config` or the single-run command line, not the five-field GUI.

## Export one unattended run

```powershell
.\.venv\Scripts\python.exe run_simulation.py --output output/single-run
.\.venv\Scripts\python.exe run_simulation.py --seed 17 --capacity 4 --output output/seed17
.\.venv\Scripts\python.exe run_simulation.py --help
```

Every `Config` field is available as a command-line option, with hyphens replacing
underscores. For example, `--congestion-threshold` changes the flow threshold.
`--config settings.json` reads generation parameters, not a saved scenario.
Explicit command-line parameters override values from that JSON object.

Use `--no-figure` to omit the final dashboard PNG, or `--trace-messages` to export
the full message log. The script returns exit code 0 when everyone is delivered
and 2 for an incomplete run. Invalid command-line input also produces code 2.
Partial outputs retain missing dates and the reason for stopping.

## Reproduce the capacity comparison

```powershell
.\.venv\Scripts\python.exe run_experiments.py --output output/comparison-uturns
.\.venv\Scripts\python.exe run_experiments.py --seeds 17 18 19 --requests 30 --output output/comparison-30
```

The default experiment uses five seeds, 2026 through 2030, eight taxis and sixty
requests appearing between 0 and 300 seconds. For each seed, the script generates
one city, fleet and demand set, then runs two fresh models whose inputs differ
only in capacity: one seat versus three seats. Both use the same simulation rules.
The runs are sequential and do not require the GUI.

The matched inputs are guaranteed by reusing the generated scenario, not just
by choosing the same seed twice. `compare()` changes only `config.capacity`.
Axes, buildings, accesses, initial taxi positions and headings, trips and
appearance ticks remain identical within each pair. Different seeds supply
different experimental inputs, each with its own matched pair.

`test_compare_generates_once_and_reuses_inputs` checks this by comparing both
exported `scenario.json` files after removing only `config.capacity`. Their full
scenario hashes are expected to differ because capacity is included in the hash.
Small unit tests also use fixed hand-built maps from `tests/conftest.py`; they
test particular rules and do not all need to use the same map.

Options are `--seeds`, `--taxis`, `--requests`, `--appearance-seconds`,
`--max-seconds` and `--output`. Seeds must be distinct nonnegative integers.
Without `--output`, the script writes to `output/comparison/`. Choose a fresh
output directory to preserve previous results. The existing study with U-turns
is in `output/comparison-uturns/`; older local exports in `output/comparison/`
were produced before U-turns were enabled and must not be mixed with that study.

| Experiment output | Contents |
| --- | --- |
| `study.json` | Parameters, seeds, capacities, statistical conventions and excluded pairs |
| `comparison.csv` | Per-seed outcomes for both capacities and their paired differences |
| `summary.csv` | Means by capacity, mean paired difference, sample standard deviation and usable pair count |
| `seed-<seed>/individual/`, `seed-<seed>/shared/` | Detailed exports for each run, without a dashboard or full message log |

Differences are **shared minus individual**, calculated per seed before aggregation.
The four compared measures are fleet distance, mean waiting time, mean total
passenger time and shared-distance rate. Rates remain fractions in [0, 1]; 0.10
means ten percentage points. Standard deviation is calculated across paired
differences and is undefined with fewer than two usable pairs.

Incomplete pairs remain exported but do not enter the comparison statistics.
Undefined measures, such as mean passenger time with no demand, remain absent
and have their own usable pair count. Tables are saved after each completed pair.
Exit code 2 indicates an incomplete pair; code 0 means all pairs completed.

## Read the implementation

| File in `taxishare/` | Responsibility |
| --- | --- |
| `config.py` | Parameters, physical constants, input checks and detour allowance |
| `scenario.py` | Generate and save fixed city, fleet, trip and arrival inputs |
| `city.py` | Road adjacency, service accesses and cached shortest paths between cells |
| `contracts.py` | Immutable trip and offer records, plus mutable physical actions |
| `messaging.py` | Addressed inboxes and message delivery |
| `passenger.py` | Send a request, choose an offer and react to confirmation and transport |
| `taxi.py` | Make offers, revalidate acceptances and execute moves and service operations |
| `planning.py` | Insert pickups and drops while checking capacity, distance budgets and promises |
| `traffic.py` | Calculate loads and speeds independently for each travel direction |
| `model.py` | Coordinate the clock, activation phases, observations and invariants |
| `metrics.py` | Build passenger and taxi tables, summaries and exports |
| `visualization.py` | Draw the current model without affecting its decisions |

A useful reading order is `passenger.py`, `taxi.py`, `model.py`, then `planning.py`.
The main flow is:

1. Generate fixed inputs. Future passengers exist as agents but remain off the
   grid and do not reveal their requests before their appearance tick.
2. At each boundary, finalize due actions and announce newly appearing requests.
3. Passengers send one initial call for proposals (CFP). Taxis retain active
   requests, build offers, and send them to each passenger.
4. Each passenger chooses by estimated boarding start, then worst detour-budget
   fraction among affected passengers, then taxi ID.
5. Each taxi revalidates acceptances in request-age and passenger-ID order.
   Confirmed passengers close their requests; rejected requests remain active.
6. Start new physical actions, compute common traffic speeds, observe the
   boundary and advance one interval. Finish due actions at the next boundary.

Offers last one round and reserve no seats. A concurrent acceptance can therefore
be rejected after another commitment changes feasibility. There is no second
negotiation round at the same instant. Agents decide from their own state and
received messages; the model coordinates their activation.

## Model assumptions

- Roads are finite bidirectional axes joined by an outer frame. Buildings have
  fixed service accesses outside intersections with three or more branches.
- A road portion is 100 m. Free speed is 50 km/h, giving 36 ticks or 7.2 seconds.
  Each boarding or alighting operation takes ten ticks or two seconds.
- U-turns are allowed at every road-cell boundary with no added maneuver time.
  A move or service operation already started must finish before another action
  starts. Heading is not a routing constraint.
- For a fixed stop order, one deterministic shortest path per leg is enough.
  The planner still tries pickup/drop insertion positions and preserves the
  relative order of previously committed stops.
- Each passenger has a fixed direct distance D0 and cumulative extra-distance
  allowance `min(detour_rate * D0, detour_cap_m)`, 25% capped at 400 m by default.
  Replanning never resets travelled distance or a confirmed approach limit.
- A seat is occupied from boarding start until alighting ends. Capacity ranges
  from one to four; sequential future bookings may outnumber physical seats.
- Pickup estimates use free speed and preceding service operations. Actual
  pickup times can grow because of congestion or later inserted operations.
- Congestion is calculated per directed portion: A to B and B to A have separate
  loads. Speed is `free_speed / max(1, vehicle_count / K)`, with K = 2 by default.
  Parked and service taxis are excluded. There are no physical queues or lights.
- Runs end when everyone is delivered, at a configurable time limit, or at a
  defensive frozen-state check. An incomplete run never counts as successful.

## Exported data

| File | Contents |
| --- | --- |
| `scenario.json` | Generation settings and all fixed inputs, including initial headings |
| `summary.json` | Status, stopping reason, outcomes, delivered count and unserved passengers |
| `passengers.csv` | One row per planned passenger, including future or unfinished trips |
| `taxis.csv` | Distance by actual occupancy and vehicle action-time accounts |
| `timeline.csv` | Observations at processed simulation boundaries |
| `provenance.json` | Environment versions, Python source hashes and available source-PDF hashes |
| `dashboard.png` | City and charts, unless disabled |
| `messages.csv` | Detailed addressed messages, only when tracing is enabled |

Times are seconds and distances are metres. Unknown values are JSON `null` or
empty CSV cells. Mean passenger outcomes use delivered trips only, with their
count reported separately. Onboard time excludes the passenger's own boarding
and alighting but includes other stops while they remain aboard.

Shared distance is vehicle distance travelled with at least two passengers,
counted once per metre. It is not passenger-kilometres or an emissions estimate.
Congestion delay is separated from time lost when an arrival uses only part of
a simulation tick. Message counts count deliveries: sixty calls sent to eight
taxis create 480 CFP envelopes, without repeating any passenger's initial call.

Replay requires identical inputs and the same model rules. A scenario hash alone
does not identify the rules; `provenance.json` records source hashes as well.
Changing only comments changes those file hashes but not the simulation logic.

## Optional implementation checks

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Tests check movement and service boundaries, cumulative budgets, offer bounds,
seat reuse, messages, directed congestion, replay and exports. They validate
implementation behavior on selected cases; the paired experiments provide the
outcomes to analyze. Assertions are enabled by default. Do not use Python's `-O`
option if you want to retain them.

## Scope and detailed notes

The model uses a local insertion policy, not a global fleet optimizer. It does
not model transfers between taxis, walking, outside traffic or emissions. Five
seeds under one main configuration support a limited comparison, not a general
claim about real cities. The academic report is a separate deliverable.

Detailed project notes are retained in French. The [documentation index](docs/README.md)
also includes the course and assignment notes imported from the parent folder,
the original slides, decision history and [versioned experiment tables](docs/results/capacity-comparison/README.md).
Historical descriptions are marked separately from the current implementation.

- [Technical decisions](docs/technical-decisions.md)
- [Rules and implementation checks](docs/rules-coverage.md)
- [Executed validation and results](docs/validation.md)
