# Protein Structure Analysis of Bacteriorhodopsin

Computational analysis of a bacteriorhodopsin protein structure using Python and Biopython.

The project combines sequence and structural analysis with hydrophobicity-based identification of transmembrane regions and validation against experimentally determined α-helices.

---

## Research question

Can sequence-derived hydrophobicity patterns be used to identify candidate transmembrane regions of bacteriorhodopsin and validate them against experimentally determined structural elements?

---

## Protein and structure

- **Protein:** bacteriorhodopsin
- **PDB structure:** 1C3W
- **Structure source:** RCSB Protein Data Bank
- **Primary tool:** Biopython

The structure is downloaded directly from the RCSB PDB and parsed with Biopython's PDB module.

---

## Analysis workflow

```text
PDB structure
      │
      ▼
Sequence & structure analysis
      │
      ├──────────────► Motif search
      │
      ▼
Hydrophobicity profile
      │
      ▼
Hydrophobic peak detection
      │
      ▼
Experimental α-helices
      │
      ▼
Peak–helix validation
      │
      ▼
Visualization
```

The project contains two related workflows. The main entry point performs basic sequence and structural analysis, while the validation workflow evaluates hydrophobicity-derived transmembrane candidates against experimentally defined α-helices.

---

## Main analysis

### 1. Structure and sequence analysis

The main workflow is launched through:

`main.py`

which calls:

`src/analysis/structure_analysis.py`

The script downloads a PDB structure, parses the selected chain, reports basic structural information, extracts the amino-acid sequence from peptide fragments, and optionally searches the sequence for a user-provided motif.

The resulting structural summary is saved to:

`results/report.txt`

### 2. Residue analysis

`src/analysis/residue_analysis.py` extracts standard amino-acid residues and records their residue numbers and three-letter amino-acid codes.

### 3. Motif search

`src/analysis/motif_search.py` converts the extracted residues into a sequence and searches for a user-provided amino-acid motif.

### 4. Secondary-structure reference

`src/analysis/secondary_structure.py` stores the experimentally determined α-helical regions used for structural validation of the hydrophobicity analysis.

For PDB 1C3W, the experimentally defined helices are represented by the following residue ranges:

- 9–31
- 36–63
- 80–101
- 104–128
- 130–155
- 164–192
- 200–226

These structural ranges are used as a reference rather than predicted from the sequence.

---

## Hydrophobicity and transmembrane-region analysis

### 5. Hydrophobicity profile

`src/analysis/hydrophobicity.py` calculates a Kyte–Doolittle hydrophobicity profile using a sliding window.

The default window size is **19 residues**, corresponding approximately to the length of a membrane-spanning α-helix.

### 6. Hydrophobic peak detection

`src/analysis/tm_analysis.py` provides two related approaches for identifying hydrophobic transmembrane candidates:

- detection of continuous hydrophobic regions;
- detection and filtering of local hydrophobicity peaks.

The validation workflow uses the hydrophobic peak approach to identify candidate transmembrane regions from the sequence.

---

## Structural validation

### 7. Peak–helix validation

`src/analysis/validation.py` compares hydrophobic peaks with experimentally determined α-helices.

For each hydrophobic peak, the script calculates its distance from the center of the nearest experimental helix and determines whether the peak lies within the corresponding helix.

The validation reports:

- number of matched peaks;
- mean distance between predicted peaks and experimental helix centers;
- minimum and maximum distances;
- number of peaks located within the assigned experimental helices;
- peak-to-helix accuracy.

For the analyzed 1C3W structure, the current validation produced:

```text
Matched peaks: 7 / 7
Accuracy: 1.00
Mean distance: 3.5 residues
```

These values describe the result for this **single protein structure** and should not be interpreted as a general estimate of the accuracy of hydrophobic transmembrane prediction.

### 8. Validation visualization

`src/analysis/plot_validation.py` combines the hydrophobicity profile, detected peaks, and experimentally defined α-helices in a single visualization.

The resulting figure is saved to:

`results/hydrophobicity_validation.png`

---

## Supporting scripts

- **`src/analysis/residue_analysis.py`** — extracts standard amino-acid residues and residue numbers.
- **`src/analysis/motif_search.py`** — searches the extracted protein sequence for a user-defined motif.
- **`src/analysis/secondary_structure.py`** — defines the experimental α-helical reference regions used for validation.
- **`src/analysis/hydrophobicity.py`** — calculates the Kyte–Doolittle hydrophobicity profile.
- **`src/analysis/tm_analysis.py`** — identifies hydrophobic regions and local hydrophobicity peaks.
- **`src/analysis/validation.py`** — compares hydrophobic peaks with experimental α-helices.
- **`src/analysis/plot_validation.py`** — visualizes the validation results.
- **`src/utils/download_pdb.py`** — downloads PDB structures from the RCSB Protein Data Bank.

---

## Main findings

For the analyzed bacteriorhodopsin structure 1C3W, the hydrophobicity-based workflow identified seven representative hydrophobic peaks corresponding to the seven experimentally defined α-helical regions.

All seven detected peaks were matched to experimental helices, with a mean distance of **3.5 residues** between predicted peak positions and experimental helix centers.

The result demonstrates how a sequence-derived hydrophobicity signal can be connected to experimentally determined three-dimensional structure.

However, because the validation uses a single well-characterized protein, the result demonstrates the **analysis workflow** rather than providing a general estimate of prediction performance.

---

## Repository structure

```text
protein_structure_analysis/
│
├── README.md
├── main.py
│
├── src/
│   ├── analysis/
│   │   ├── structure_analysis.py
│   │   ├── residue_analysis.py
│   │   ├── motif_search.py
│   │   ├── secondary_structure.py
│   │   ├── hydrophobicity.py
│   │   ├── tm_analysis.py
│   │   ├── validation.py
│   │   └── plot_validation.py
│   │
│   └── utils/
│       └── download_pdb.py
│
├── data/
│   └── pdb/
│       └── pdb1c3w.ent
│
└── results/
    └── report.txt
```

---

## Technologies

- Python
- Biopython
- NumPy
- Matplotlib
- PDB / RCSB Protein Data Bank
- Git / GitHub

---

## Installation

Create a Python virtual environment and install the packages used by the analysis scripts:

```bash
python -m venv .venv
source .venv/bin/activate
pip install biopython numpy matplotlib
```

---

## Usage

The main structure-analysis workflow can be launched with:

```bash
python main.py
```

The hydrophobicity validation workflow can be launched with:

```bash
python -m src.analysis.plot_validation
```

The PDB structure used in the current analysis is 1C3W.

---

## Reproducibility

The PDB structure is obtained from the RCSB Protein Data Bank. The downloaded structure is stored locally in `data/pdb/` for analysis.

The hydrophobicity analysis uses the Kyte–Doolittle scale and a default 19-residue sliding window.

Experimental α-helical regions for PDB 1C3W are explicitly defined in `secondary_structure.py` and are used as the reference for validation.

---

## Analysis status

**Analysis completed.**

This project represents the foundation of a broader structural bioinformatics portfolio progressing from protein structure analysis to structure comparison and molecular dynamics analysis.
