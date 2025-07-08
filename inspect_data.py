import json

# 📥 Laad lokaal JSON-bestand
with open("game_data.json") as f:
    data = json.load(f)

# 🔍 Toon aantal games
print(f"Aantal wedstrijden: {len(data)}")

# 🔍 Bekijk eerste 1-2 games (ruwe structuur)
for i, game in enumerate(data[:2]):
    print(f"\n🎯 Game {i+1} -------------------------")
    print(json.dumps(game, indent=2))
