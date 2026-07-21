# Protein Structure Analysis

A Python project for downloading and analyzing protein structures from the Protein Data Bank (PDB).

## Features

- downloads a protein structure by its PDB ID;
- loads the structure using Biopython;
- analyzes:
  - number of models;
  - number of chains;
  - number of residues;
  - number of atoms;
  - amino acid sequence;
  - sequence length;
  - molecular weight;
  - amino acid composition;
- saves the analysis to `results/report.txt`.

## Technologies

- Python 3
- Biopython

## Project structure

```
protein_structure_analysis/
│
├── data/
│   └── pdb/
│
├── results/
│   └── report.txt
│
├── src/
│   ├── analysis/
│   │   └── structure_analysis.py
│   └── utils/
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repository_url>
cd protein_structure_analysis

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Run

```bash
python main.py
```

The analysis report will be saved to

```
results/report.txt
```

## Example output

```
=== Model 0 ===
Chains: 1

Chain A
------------------------
Residues: 260
Atoms: 2073
Sequence length: 222 amino acids
Molecular weight: 24.33 kDa
```

## Author

Svetlana Knyazeva