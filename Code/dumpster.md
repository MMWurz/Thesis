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

## Objective 3 — EU Supply Autonomy methodology

Use EU JRC CRM supply risk methodology: HHI × WGI per supplier country → weighted supply risk score

Reference: EU EEA supply risk metrics — https://www.eea.europa.eu/en/circularity/thematic-metrics/materialsandwaste/evolution-of-eu-raw-materials-supply-risk

## Enrichment cost data

Public techno-economic data for novel Li-6 enrichment routes is sparse; no industrial cost figures are publicly available.
- Enrichment technology cost is a **scenario variable**: low / medium / high cost assumption per technology
- Model is solved for each scenario; Pareto fronts are compared across scenarios
- Shows policy-relevant insight: how sensitive the cost–risk trade-off is to enrichment cost uncertainty
- Academically defensible: framework and trade-off structure are the contribution, not a single cost estimate

## Thesis novelty framing

> "We extend [ACS 2025 MILP] to Li-6 by adapting the supply chain structure from [Giegerich 2019] and applying it as a bi-criterion MOO for the first time, trading off cost against EU supply risk."

## Solution method

AUGMECON (Mavrotas 2009) — the augmented ε-constraint method. Correct and efficient for bi-criterion MILP; avoids weakly Pareto-optimal solutions via slack variable augmentation; generates a clean 2D Pareto curve.

## Model type: MILP

Almost certainly a Mixed Integer Linear Program (MILP). Two layers of decisions:

1. **Strategic (binary/integer):** Open facility at location X? Use supplier Y? → yes/no = 0/1 integer variables
2. **Operational (continuous):** How much material flows along each arc? → continuous variables

The mix of these two is what makes it "Mixed Integer Linear". Linear holds as long as costs, capacities, and flows scale proportionally — standard assumption in supply chain models and what the ACS 2025 base paper uses.

**Node structure from Giegerich 2019:**

```
Ore mines → Chemical processing → Isotope separation → Li-6 product → Tritium blanket
```

Each arrow = flow variable (continuous). Each node = facility-open decision (binary). Classic multi-echelon MILP.

Both objectives (cost, supply risk) are expressible as linear functions of those same variables — model type does not change. AUGMECON solves the MILP repeatedly with different epsilon bounds to trace the Pareto front.

**Practical implications:**
- Solver: CBC (free, bundled with Pyomo) sufficient for thesis scale; Gurobi (free academic license) faster if problem grows
- Single MILP solve: seconds to minutes; full Pareto front run: still manageable
- Not writing MILP from scratch — adapting ACS 2025 formulation to Li-6 node structure, swapping in the three objectives
- Hardest part: **data** (supplier locations, costs, isotope separation capacity), not the math

## Agreed reading order

1. arXiv:2605.04707 (problem motivation)
2. Giegerich et al. 2019 (supply chain structure)
3. ACS 2025 MILP paper (mathematical formulation to adopt)
4. EU EEA/JRC supply risk methodology (operationalize objective 3)
