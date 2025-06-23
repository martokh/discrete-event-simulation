# TU Sofia Canteen Simulation with SimPy

**Author:** Martin Hristov
**Student ID:** 201222041
**Language:** Python 3
**Dependencies:** simpy, matplotlib

## Overview

This project models lunchtime queue dynamics at the TU Sofia canteen (11:00–14:00) using a discrete-event simulation (SimPy). Two scenarios are compared:

1. **2 cash registers**
2. **3 cash registers**

We measure average and maximum waiting times and visualize the distributions with side-by-side histograms.

## Model Assumptions

* **Time horizon:** 180 minutes (0–180) → 11:00–14:00
* **Arrival process:** piecewise-constant Poisson (exponential interarrival times):

  * 0–60 min (11:00–12:00): λ = 0.5 min⁻¹
  * 60–120 min (12:00–13:00): λ = 1.4 min⁻¹
  * 120–180 min (13:00–14:00): λ = 0.333 min⁻¹
* **Service time:** Uniform(1.0, 3.0) min per customer
* **Resources:**

  * Scenario A: `capacity=2`
  * Scenario B: `capacity=3`

## Installation

```bash
git clone https://github.com/your-username/tu-sofia-canteen-simpy.git
cd tu-sofia-canteen-simpy

# (optional) create & activate venv
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install simpy matplotlib
```

## Usage

Run each scenario from the project root:

```bash
python TU_Kantine_2Kassen.py   # 2 registers
python TU_Kantine_3Kassen.py   # 3 registers
```

* Prints **average** and **maximum** waiting times
* Opens a Matplotlib window with the waiting-time histogram(s)

## Example Output

```
=== Scenario with 2 registers ===
Average waiting time: 5.12 min
Maximum waiting time: 20.45 min

=== Scenario with 3 registers ===
Average waiting time: 1.03 min
Maximum waiting time:  8.27 min
```

*(Actual values will vary per run.)*

## Results

| Scenario        | Avg. Wait (min) | Max Wait (min) |
| --------------- | --------------- | -------------- |
| **2 registers** | \~5.00          | \~20.00        |
| **3 registers** | \~1.00          | \~8.00         |

Adding a third register drastically reduces both average and peak wait times.

## License

MIT License © Martin Hristov

