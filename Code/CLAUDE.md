# MOO Model Research — Li-6 Supply Chain

Decided to adopt an existing MILP supply chain model rather than build from scratch, extending it for Li-6 with two objectives: cost and EU supply risk.

Environmental impact was dropped as a third objective. A rigorous ecological assessment requires per-process LCA inventory data that is not yet available for the Li-6 enrichment routes relevant to this thesis. Including it without adequate data would compromise scientific validity. The omission is treated as a limitation and future work direction in the thesis.

## Recommended base model (adopt this)

- **ACS Ind. Eng. Chem. Res. 2025:** "Robust Design and Optimization of Integrated Sustainable Lithium-Ion Battery Supply Chain Network under Demand Uncertainty"
  - https://pubs.acs.org/doi/10.1021/acs.iecr.5c01990
  - Multi-echelon MILP, covers all three objective types, lithium-based chain

## Alternative base model

- **ScienceDirect 2025:** "A multi-objective robust optimization model to sustainable closed-loop lithium-ion battery supply chain network design under uncertainties"
  - https://www.sciencedirect.com/science/article/abs/pii/S0098135425000122

## Li-6-specific domain papers (not base models — use for structure and motivation)

- **Giegerich et al. 2019, Fusion Eng. Design:** "Development of a viable route for lithium-6 supply of DEMO"
  - Defines supply chain nodes: ore mining → chemical processing → isotope separation → Li-6 product → tritium breeding blanket
  - https://www.sciencedirect.com/science/article/pii/S092037961930835X
- **Joule 2025 (arXiv:2605.04707):** "Lithium enrichment threatens to curb fusion deployment"
  - Strongest thesis motivation, high-impact journal
  - https://arxiv.org/abs/2605.04707

## Objective 2 — EU Supply Autonomy methodology

Use EU JRC CRM supply risk methodology: HHI x WGI per supplier country -> weighted supply risk score

Reference: EU EEA supply risk metrics — https://www.eea.europa.eu/en/circularity/thematic-metrics/materialsandwaste/evolution-of-eu-raw-materials-supply-risk

## Enrichment cost data

Public techno-economic data for novel Li-6 enrichment routes is sparse; no industrial cost figures are publicly available.
- Enrichment technology cost is a **scenario variable**: low / medium / high cost assumption per technology
- Model is solved for each scenario; Pareto fronts are compared across scenarios
- Shows policy-relevant insight: how sensitive the cost-risk trade-off is to enrichment cost uncertainty
- Academically defensible: framework and trade-off structure are the contribution, not a single cost estimate

## Thesis novelty framing

"We extend [ACS 2025 MILP] to Li-6 by adapting the supply chain structure from [Giegerich 2019] and applying it as a bi-criterion MOO for the first time, trading off cost against EU supply risk."

## Solution method

AUGMECON (Mavrotas 2009) — the augmented epsilon-constraint method. Correct and efficient for bi-criterion MILP; avoids weakly Pareto-optimal solutions via slack variable augmentation; generates a clean 2D Pareto curve.

## Model type: MILP

Two layers of decisions:

1. **Strategic (binary/integer):** Open facility at location X? Use supplier Y? -> yes/no = 0/1 integer variables
2. **Operational (continuous):** How much material flows along each arc? -> continuous variables

**Node structure from Giegerich 2019:**

```
Ore mines -> Chemical processing -> Isotope separation -> Li-6 product -> Tritium blanket
```

Each arrow = flow variable (continuous). Each node = facility-open decision (binary). Classic multi-echelon MILP.

Both objectives (cost, supply risk) are linear functions of those variables. AUGMECON solves the MILP repeatedly with different epsilon bounds to trace the Pareto front.

**Practical notes:**
- Solver: TBD (CBC bundled with Pyomo / Gurobi academic license)
- Single MILP solve: seconds to minutes; full Pareto front run: manageable
- Hardest part: **data** (supplier locations, costs, isotope separation capacity), not the math

## Agreed reading order

1. arXiv:2605.04707 (problem motivation)
2. Giegerich et al. 2019 (supply chain structure)
3. ACS 2025 MILP paper (mathematical formulation to adopt)
4. EU EEA/JRC supply risk methodology (operationalize objective 2)

---

# MILP Formulation — Li-6 Supply Chain

Adapted from Tsiakis et al. (2001), Ind. Eng. Chem. Res., 40, 3585-3604.

## Sets & Indices

| Symbol | Description | Size |
|--------|-------------|------|
| e in E | Enrichment sites | 3 |
| t in T | Enrichment technologies | 3 |
| l in L | Construction sites | 3 |
| r in R | Reactors (customers) | 1 |

## Decision Variables

### Binary

| Variable | Definition |
|----------|------------|
| Y_et in {0,1} | 1 if enrichment site e is built with technology t |
| X_el in {0,1} | 1 if enrichment site e supplies construction site l (site-level) |
| X_etl in {0,1} | 1 if enrichment site e with technology t supplies construction site l (technology-explicit) |

### Continuous

| Variable | Definition |
|----------|------------|
| Q_el >= 0 | Flow rate from enrichment site e to construction site l (site-level) |
| Q_etl >= 0 | Flow rate from enrichment site e with technology t to construction site l |
| Q_lr >= 0 | Flow rate from construction site l to reactor r |

## Constraints

### 1. Network Structure — link only if facility exists

A supply link e->l can only be active if enrichment facility e is built.
Analogous to Tsiakis eq. (1): X_mk <= Y_m.

9-equation formulation (technology aggregated): X_el <= Y_e for all e, l
27-equation formulation (technology explicit): X_etl <= Y_et for all e, t, l

### 2. Transportation Flow — minimum flow if link is active

If a link is established, a minimum flow must be sent to justify it economically.
Analogous to Tsiakis eq. (9).

9-equation: Q_el >= Q_el_min * X_el for all e, l
27-equation: Q_etl >= Q_etl_min * X_etl for all e, t, l

### 3. Flow Activation — flow only if facility exists

Flow on a link is zero unless the upstream enrichment facility is built.
Analogous to Tsiakis eq. (6).

9-equation: Q_el <= Q_el_max * Y_e for all e, l
27-equation: Q_etl <= Q_etl_max * Y_et for all e, t, l

## Status

| Constraint group | Formulated | Coded |
|-----------------|------------|-------|
| 1. Network structure | done | no |
| 2. Minimum flow | done | no |
| 3. Flow activation | done | no |
| Material balance | no | no |
| Capacity bounds | no | no |
| Objective function | no | no |
