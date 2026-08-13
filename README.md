# Protein Structure Analysis

A Python-based bioinformatics project for sequence and structural analysis of protein structures from the Protein Data Bank (PDB).

The current analysis focuses on bacteriorhodopsin (PDB: 1C3W), a well-characterized membrane protein.

## Project goals

The project demonstrates a reproducible workflow for:

- downloading and parsing protein structures from the PDB;
- extracting amino acid sequences from 3D structures;
- analyzing protein sequence and structural properties;
- calculating residue-level hydrophobicity profiles;
- detecting hydrophobic peaks and candidate transmembrane regions;
- comparing computational predictions with experimentally determined secondary structure;
- quantitatively validating the predictions;
- visualizing the results.

## Analysis workflow

### 1. Protein structure analysis

The protein structure is loaded using Biopython.

The following structural and sequence properties are calculated:

- number of models;
- number of chains;
- number of residues;
- number of atoms;
- amino acid sequence;
- sequence length;
- molecular weight;
- amino acid composition.

The analysis report is saved to:

results/report.txt

### 2. Hydrophobicity analysis

A residue-level hydrophobicity profile is calculated from the extracted amino acid sequence.

Hydrophobic regions are relevant for identifying possible membrane-spanning segments in membrane proteins.

The resulting profile is visualized in:

results/hydrophobicity_profile.png

### 3. Hydrophobic peak detection

Local maxima in the hydrophobicity profile are detected as potential membrane-associated regions.

For bacteriorhodopsin (PDB: 1C3W):

- 22 local hydrophobic peaks were initially detected;
- after applying a minimum-distance criterion, 7 representative peaks were selected.

The selected peak positions are:

16, 49, 88, 113, 140, 173, 206

### 4. Structural validation

The selected hydrophobic peaks were compared with experimentally determined alpha-helices reported in the PDB structure.

The seven selected peaks were matched to the seven major alpha-helical regions:

| Hydrophobic peak | Experimental alpha-helix | Distance to helix center |
|---:|:---:|---:|
| 16 | 9-31 | 4.0 residues |
| 49 | 36-63 | 0.5 residues |
| 88 | 80-101 | 2.5 residues |
| 113 | 104-128 | 3.0 residues |
| 140 | 130-155 | 2.5 residues |
| 173 | 164-192 | 5.0 residues |
| 206 | 200-226 | 7.0 residues |

All seven selected hydrophobic peaks were located inside experimentally determined alpha-helices.

Matched peaks: 7 / 7
Accuracy: 1.00
Mean distance: 3.5 residues

This validation was performed on a single well-characterized protein and therefore demonstrates the analysis workflow rather than providing a general estimate of prediction accuracy.

### 5. Validation visualization

The hydrophobicity profile and experimentally determined alpha-helical regions are combined in a single visualization.

The resulting figure is saved to:

results/hydrophobicity_validation.png

## Technologies

- Python 3
- Biopython
- NumPy
- Matplotlib
- PDB
- Git
- GitHub

## Project structure

protein_structure_analysis/

├── data/
│   └── pdb/
│       ├── 1c3w.pdb
│       └── pdb1c3w.ent
│
├── results/
│   ├── hydrophobicity_profile.png
│   ├── hydrophobicity_validation.png
│   └── report.txt
│
├── src/
│   ├── analysis/
│   │   ├── structure_analysis.py
│   │   ├── residue_analysis.py
│   │   ├── motif_search.py
│   │   ├── hydrophobicity.py
│   │   ├── secondary_structure.py
│   │   ├── tm_analysis.py
│   │   ├── validation.py
│   │   └── plot_validation.py
│   │
│   └── utils/
│       └── download_pdb.py
│
├── main.py
├── requirements.txt
└── README.md

## Installation

git clone <repository_url>
cd protein_structure_analysis

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

## Usage

Run the main structural analysis:

python main.py

To generate the hydrophobicity validation plot:

python -m src.analysis.plot_validation

The resulting figure will be saved to:

results/hydrophobicity_validation.png

## Example output

=== Model 0 ===
Chains: 1

Chain A
------------------------
Residues: 260
Atoms: 2073
Sequence length: 222 amino acids
Molecular weight: 24.33 kDa

## Author

Svetlana Knyazeva
