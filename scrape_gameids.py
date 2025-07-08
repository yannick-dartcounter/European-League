from playwright.sync_api import sync_playwright
import requests
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
STORAGE_FILE = "dartcounter_session.json"
SCREENSHOT_PATH = "screenshot.png"

def get_game_ids():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # zet op True als je het niet visueel wilt
        context = browser.new_context(storage_state=STORAGE_FILE)
        page = context.new_page()

        print("🌍 Pagina laden...")
        page.goto(BRACKET_URL)

        page.wait_for_timeout(5000)
        print("📸 Screenshot maken...")
        page.screenshot(path=SCREENSHOT_PATH)

        print("🔍 Probeer game-IDs te vinden...")
        elements = page.query_selector_all("[data-id]")
        print(f"📦 Aantal elementen gevonden met [data-id]: {len(elements)}")

        game_ids = set()
        for el in elements:
            game_id = el.get_attribute("data-id")
            if game_id and len(game_id) >= 5:
                game_ids.add(game_id)
                print("🆔 Gevonden game ID:", game_id)

        browser.close()
        return list(game_ids)

def fetch_game_details(game_id):
    url = f"https://app.dartcounter.net/api/games/{game_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Geen succes voor {game_id} - status {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Fout bij ophalen van game {game_id}: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Start scraping...")
    ids = get_game_ids()
    print(f"✅ {len(ids)} game ID(s) gevonden.")

    if not ids:
        print("⚠️ Geen game ID's gevonden. Check screenshot.png en of je bent ingelogd.")
    else:
        all_games = []
        for i, gid in enumerate(ids):
            print(f"⬇️ Ophalen game {i+1}/{len(ids)}: {gid}")
            details = fetch_game_details(gid)
            if details:
                all_games.append(details)
            time.sleep(0.5)

        with open("game_data.json", "w") as f:
            json.dump(all_games, f, indent=2)

        print(f"💾 {len(all_games)} games opgeslagen in game_data.json")
