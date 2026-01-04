# Algorithmic Immunity: Technical Design Document (v2)
**System:** Thermodynamically Constrained Generative Models (TC-GM)
**Role:** Predictive modeling of viral escape within physical constraints.

## 1. Architectural Philosophy
Standard viral prediction models (EVE, MutaGAN) operate on **Probabilistic Evolution** ("What is likely?").
Our system operates on **First Principles Constraint** ("What is physically allowed at tolerable fitness cost?").
We inject the "Entropic Vise" (high-barrier thermodynamic constraints) as a core axiom in the generative model's conditioning.

**v2 Update:** We are transitioning from GANs to **Diffusion-based architectures** (RFdiffusion, ProteinMPNN) which offer superior handling of structural constraints and avoid mode collapse issues.

## 2. System Architecture

### A. Option 1: TC-GAN (Original Design)
*   **Architecture:** Transformer-based Decoder adapted for protein sequences.
*   **Limitation:** GANs suffer from mode collapse, failing to capture the full diversity of viable escape variants.

### B. Option 2: Diffusion Models (Recommended)
*   **Architecture:** RFdiffusion or similar diffusion-based protein design model.
*   **Mechanism:** Gradual denoising of random 3D coordinates into valid protein backbone structures.
*   **Advantages:**
    - Inherently respects physical and geometric constraints
    - Superior structural fidelity
    - Allows "inpainting" of protein structures or design of binders against specific targets
*   **Integration:** ProteinMPNN can generate sequences thermodynamically optimal for a given backbone.

## 3. Target Definition (v2 Corrected)

| Region | HXB2 Coordinates | Sequence | Role |
| :--- | :--- | :--- | :--- |
| **HR1 (Primary)** | 546–556 | SGIVQQQNNLL | Inner core of 6-helix bundle |
| **MPER (Secondary)** | 678–682 | WLWYI | Membrane-proximal region |

**Critical Note:** The original coordinates (568-576) were incorrect. The corrected target is **546-556**, validated against the standard HXB2 numbering scheme.

## 4. Constraint Enforcement

### The Thermodynamic Penalty ($L_{vise}$)
Instead of treating the HR1 region as "absolutely immutable," we model it as a **high-barrier constraint** with fitness cost:

$$L_{total} = L_{diffusion} + \lambda_{vise} \cdot L_{vise}$$

Where $L_{vise}$ is:
- **Strict mode:** Hamming distance penalty against reference sequence
- **Fitness-aware mode:** Predicted ΔΔG (stability change) for mutations in constrained regions

**Resistance Consideration:** Known escape mutations (V38A, N43D) should be included in training to understand fitness cost landscapes.

## 5. Execution Workflow
1.  **Training:** Condition diffusion model on historical Env evolution + thermodynamic stability data.
2.  **Inference (Attack Simulation):**
    *   Simulate "high antibody pressure" or "drug pressure" scenarios.
    *   Generate diverse escape variant library.
3.  **Filtering:** Retain variants that are bio-plausible AND preserve core structure.
4.  **Result:** A "Future Virus Library" constrained by thermodynamic reality.
5.  **Therapeutic Validation:** Verify that Aptamer-Protease chimeras maintain efficacy against predicted variants.

## 6. Future Directions

- **SELEX Screening:** Generate aptamer libraries against both wild-type (SGIVQQQNNLL) and mutant (V38A) peptides.
- **Binding Kinetics:** Compare Kd values across mutation panels via SPR.
- **Cleavage Assays:** Measure protease cleavage efficiency against wild-type and mutant substrates.

## 7. Summary
We are not just predicting evolution; we are **channeling** it within thermodynamic constraints. The diffusion model approach offers superior protein design capabilities while respecting the physical limits of viral adaptation.

---
**References:**
- RFdiffusion: Baker Lab (2023)
- ProteinMPNN: Dauparas et al. (2022)
- Enfuvirtide resistance data: Greenberg & Cammack (2004) JAC
