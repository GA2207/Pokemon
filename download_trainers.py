import os
import re
import requests

DIR_URL = "https://play.pokemonshowdown.com/sprites/trainers/?view=dir"
BASE_URL = "https://play.pokemonshowdown.com/sprites/trainers/"
OUT_DIR = "assets/sprites/trainers"

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def get_filenames():
    r = requests.get(DIR_URL, timeout=30)
    r.raise_for_status()
    html = r.text
    # récupère tous les "xxx.png" listés dans la page
    names = sorted(set(re.findall(r'href="([^"]+\.png)"', html)))
    return names

def download_one(name: str) -> bool:
    url = BASE_URL + name
    dest = os.path.join(OUT_DIR, name)

    if os.path.exists(dest):
        return False  # déjà là

    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        print(f"❌ {name} ({r.status_code})")
        return False

    with open(dest, "wb") as f:
        f.write(r.content)

    print(f"✅ {name}")
    return True

def main():
    ensure_out_dir()
    print("📥 Récupération de la liste des trainers…")
    names = get_filenames()
    print(f"🔎 {len(names)} fichiers trouvés")

    downloaded = 0
    for name in names:
        if download_one(name):
            downloaded += 1

    print(f"\n✅ Terminé. Nouveaux fichiers téléchargés : {downloaded}")
    print("👉 Vérifie avec : ls assets/sprites/trainers | head")

if __name__ == "__main__":
    main()