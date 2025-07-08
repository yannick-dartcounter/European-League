from playwright.sync_api import sync_playwright
import requests
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
STORAGE_FILE = "dartcounter_session.json"

def get_game_ids():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=STORAGE_FILE)
        page = context.new_page()

        page.goto(BRACKET_URL)
        print("👀 Pagina geladen:", page.title())
        print("🔗 URL:", page.url)
        page.screenshot(path="screenshot.png")

        page.wait_for_timeout(5000)

        game_ids = set()
        elements = page.query_selector_all("[data-id]")
        for el in elements:
            game_id = el.get_attribute("data-id")
            if game_id and len(game_id) >= 5:
                game_ids.add(game_id)

        browser.close()
        return list(game_ids)

def fetch_game_details(game_id):
    url = f"https://app.dartcounter.net/api/games/{game_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Fout bij game {game_id}: {e}")
        return None

if __name__ == "__main__":
    ids = get_game_ids()
    all_games = []

    for i, gid in enumerate(ids):
        print(f"Ophalen game {i+1}/{len(ids)}: {gid}")
        details = fetch_game_details(gid)
        if details:
            all_games.append(details)
        time.sleep(0.5)

    with open("game_data.json", "w") as f:
        json.dump(all_games, f, indent=2)

    print("💾 Opgeslagen in game_data.json")
