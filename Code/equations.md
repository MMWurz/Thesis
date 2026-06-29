# MILP Formulation — Li-6 Supply Chain (Thesis)

Adapted from Tsiakis et al. (2001), *Ind. Eng. Chem. Res.*, 40, 3585–3604.

---

## Sets & Indices

| Symbol | Description | Size |
|--------|-------------|------|
| $e \in \mathcal{E}$ | Enrichment sites | 3 |
| $t \in \mathcal{T}$ | Enrichment technologies | 3 |
| $l \in \mathcal{L}$ | Construction sites | 3 |
| $r \in \mathcal{R}$ | Reactors (customers) | 1 |

---

## Decision Variables

### Binary

| Variable | Definition |
|----------|------------|
| $Y_{et} \in \{0,1\}$ | 1 if enrichment site $e$ is built with technology $t$ |
| $X_{el} \in \{0,1\}$ | 1 if enrichment site $e$ supplies construction site $l$ (site-level) |
| $X_{etl} \in \{0,1\}$ | 1 if enrichment site $e$ with technology $t$ supplies construction site $l$ (technology-explicit) |

### Continuous

| Variable | Definition |
|----------|------------|
| $Q_{el} \geq 0$ | Flow rate from enrichment site $e$ to construction site $l$ (site-level) |
| $Q_{etl} \geq 0$ | Flow rate from enrichment site $e$ with technology $t$ to construction site $l$ |
| $Q_{lr} \geq 0$ | Flow rate from construction site $l$ to reactor $r$ |

---

## Constraints

### 1. Network Structure — link only if facility exists

> A supply link $e \to l$ can only be active if enrichment facility $e$ is built.
> Analogous to Tsiakis eq. (1): $X_{mk} \leq Y_m$.

**9-equation formulation** (technology aggregated into site-level variable $Y_e$):

$$X_{el} \leq Y_e \quad \forall\, e \in \mathcal{E},\, l \in \mathcal{L}$$

**27-equation formulation** (technology explicit):

$$X_{etl} \leq Y_{et} \quad \forall\, e \in \mathcal{E},\, t \in \mathcal{T},\, l \in \mathcal{L}$$

---

### 2. Transportation Flow — minimum flow if link is active

> If a link is established, a minimum flow must be sent to justify it economically.
> Analogous to Tsiakis eq. (9): $\sum_i Q_{imk} \geq Q_{mk}^{\min} X_{mk}$.

**9-equation formulation:**

$$Q_{el} \geq Q_{el}^{\min} \cdot X_{el} \quad \forall\, e \in \mathcal{E},\, l \in \mathcal{L}$$

**27-equation formulation:**

$$Q_{etl} \geq Q_{etl}^{\min} \cdot X_{etl} \quad \forall\, e \in \mathcal{E},\, t \in \mathcal{T},\, l \in \mathcal{L}$$

---

### 3. Flow Activation — flow only if facility exists

> Flow on a link is zero unless the upstream enrichment facility is built.
> Analogous to Tsiakis eq. (6): $Q_{ijm} \leq Q_{ijm}^{\max} Y_m$.

**9-equation formulation:**

$$Q_{el} \leq Q_{el}^{\max} \cdot Y_e \quad \forall\, e \in \mathcal{E},\, l \in \mathcal{L}$$

**27-equation formulation:**

$$Q_{etl} \leq Q_{etl}^{\max} \cdot Y_{et} \quad \forall\, e \in \mathcal{E},\, t \in \mathcal{T},\, l \in \mathcal{L}$$

---

## Status

| Constraint group | Formulated | Coded |
|-----------------|------------|-------|
| 1. Network structure | ✓ | ☐ |
| 2. Minimum flow | ✓ | ☐ |
| 3. Flow activation | ✓ | ☐ |
| Material balance | ☐ | ☐ |
| Capacity bounds | ☐ | ☐ |
| Objective function | ☐ | ☐ |
