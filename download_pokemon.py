import os
import requests

BASE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
SAVE_DIR = "assets/sprites/pokemon"

os.makedirs(SAVE_DIR, exist_ok=True)

for i in range(1, 152):  # 1 à 151
    url = f"{BASE_URL}{i}.png"
    response = requests.get(url)

    if response.status_code == 200:
        with open(f"{SAVE_DIR}/{i}.png", "wb") as f:
            f.write(response.content)
        print(f"Pokémon {i} téléchargé")
    else:
        print(f"Erreur pour {i}")

print("Téléchargement terminé !")