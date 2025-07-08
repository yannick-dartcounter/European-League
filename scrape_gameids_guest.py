from playwright.sync_api import sync_playwright
import requests
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
SCREENSHOT_PATH = "screenshot_guest.png"


def get_game_ids_as_guest():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Pagina openen als gast...")
        page.goto(BRACKET_URL)
        page.wait_for_timeout(3000)

        # ✅ Klik op 'Continue without account'
        try:
            continue_guest = page.get_by_text("Continue without account")
            if continue_guest.is_visible():
                print("👤 Gastmodus activeren...")
                continue_guest.click()
                page.wait_for_timeout(2000)
        except:
            print("❔ Geen gastoptie zichtbaar")

        # ✅ Klik checkbox visueel indien aanwezig
        try:
            checkbox_visual = (
                page.query_selector("input[type='checkbox']") or
                page.query_selector("div[role='checkbox']") or
                page.query_selector("div[class*='check']") or
                page.query_selector("svg")
            )
            if checkbox_visual:
                print("☑️ Checkbox aanklikken...")
                checkbox_visual.click(force=True)
                page.wait_for_timeout(1000)
            else:
                print("❔ Geen checkbox gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij checkbox: {e}")

        # ✅ Klik juiste 'Continue' knop via unieke klasse
        try:
            correct_button = page.query_selector("button.bg-orange") or \
                             page.get_by_role("button", name="Continue")
            if correct_button:
                print("➡️ Klik juiste 'Continue'-knop...")
                correct_button.click(force=True)
                page.wait_for_timeout(2000)
            else:
                print("❌ Geen geschikte 'Continue'-knop gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij Continue-knop: {e}")

        page.screenshot(path=SCREENSHOT_PATH)
        print("📸 Screenshot opgeslagen als screenshot_guest.png")

        print("🔍 Zoek links naar wedstrijdstatistieken...")
        links = page.query_selector_all("a")
        game_ids = []

        for link in links:
            href = link.get_attribute("href")
            if href and "/statistics/match/details?gameId=" in href:
                gid = href.split("gameId=")[-1].split("&")[0]
                if gid not in game_ids:
                    game_ids.append(gid)
                    print("✅ Gevonden gameId:", gid)

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
    print("🚀 Scraping starten als gast...")
    ids = get_game_ids_as_guest()
    print(f"📦 {len(ids)} gameId(s) gevonden.")

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
