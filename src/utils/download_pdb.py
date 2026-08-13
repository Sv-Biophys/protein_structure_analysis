import requests
from pathlib import Path


def download_pdb(pdb_id):
    """
    Скачивает PDB-файл по его идентификатору.
    """

    pdb_id = pdb_id.lower()

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    save_dir = Path("data/pdb")
    save_dir.mkdir(parents=True, exist_ok=True)

    save_path = save_dir / f"{pdb_id}.pdb"

    if save_path.exists():
        print("Файл уже существует.")
        return str(save_path)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("PDB не найден.")

    with open(save_path, "w") as f:
        f.write(response.text)

    print("Файл успешно скачан.")

    return str(save_path)