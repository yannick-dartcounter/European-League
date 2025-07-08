from playwright.sync_api import sync_playwright
import requests
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
STORAGE_FILE = "dartcounter_session.json"
SCREENSHOT_PATH = "screenshot.png"

def get_game_ids_from_popups():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # zet op True als je het niet visueel wilt
        context = browser.new_context(storage_state=STORAGE_FILE)
        page = context.new_page()

        print("🌍 Pagina laden...")
        page.goto(BRACKET_URL)
        page.wait_for_timeout(5000)
        page.screenshot(path=SCREENSHOT_PATH)

        print("🔍 Zoek 'View details'-knoppen...")
        buttons = page.query_selector_all("button:has-text('View details')")
        print(f"🔘 Aantal knoppen gevonden: {len(buttons)}")

        game_ids = []

        for i, btn in enumerate(buttons):
            print(f"\n👆 Klik op knop {i+1}/{len(buttons)}")
            btn.click()
            page.wait_for_timeout(1000)  # even wachten tot popup verschijnt

            # Zoek gameId binnen de geopende popup
            modal = page.query_selector(".MuiDialog-root")
            if modal:
                html = modal.inner_html()
                if "gameId" in html:
                    # Zoek de daadwerkelijke gameId via JavaScript object
                    matches = page.locator(".MuiDialog-root").locator("script").all()
                    for script in matches:
                        try:
                            content = script.inner_text()
                            if "gameId" in content:
                                # Simpele extractie via tekst (kan beter met regex)
                                start = content.find("gameId") + 9
                                game_id = content[start:start+10].split('"')[0]
                                if game_id not in game_ids:
                                    game_ids.append(game_id)
                                    print(f"✅ Gevonden gameId: {game_id}")
                        except:
                            continue
            else:
                print("⚠️ Geen popup gevonden")

            # Sluit de popup
            close_btn = page.query_selector("button[aria-label='Close']")
            if close_btn:
                close_btn.click()
                page.wait_for_timeout(500)

        browser.close()
        return game_ids

def fetch_game_details(game_id):
    url = f"https://app.dartcounter.net/api/games/{game_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Fout bij {game_id} – status {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Fout bij game {game_id}: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Start scraping...")
    ids = get_game_ids_from_popups()
    print(f"📦 {len(ids)} unieke gameId(s) gevonden.")

    if not ids:
        print("⚠️ Geen gameId’s gevonden. Check screenshot.png en of je bent ingelogd.")
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
