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

        # ✅ Klik checkbox via <span class='icon-check_mark'>
        try:
            checkbox_span = page.query_selector("span.icon-check_mark")
            if checkbox_span:
                print("☑️ Checkbox <span> aanklikken...")
                checkbox_span.click(force=True)
                page.wait_for_timeout(1000)
            else:
                print("❔ Geen checkbox <span> gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij checkbox: {e}")

        # ✅ Klik juiste 'Continue' knop via klasse
        try:
            correct_button = page.query_selector("button.bg-orange") or \
                             page.get_by_role("button", name="Continue")
            if correct_button:
                print("➡️ Klik juiste 'Continue'-knop...")
                correct_button.click(force=True)
                page.wait_for_timeout(3000)
            else:
                print("❌ Geen geschikte 'Continue'-knop gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij Continue-knop: {e}")

        page.screenshot(path=SCREENSHOT_PATH)
        print("📸 Screenshot opgeslagen als screenshot_guest.png")

        print("🔎 Zoek 'View details' knoppen...")
        view_buttons = page.query_selector_all("button:has-text('View details')")
        game_ids = []

        for i, btn in enumerate(view_buttons):
            try:
                print(f"🔘 Klik View details knop {i+1}/{len(view_buttons)}")
                btn.click(force=True)
                page.wait_for_timeout(1000)
                url = page.url
                if "gameId=" in url:
                    gid = url.split("gameId=")[-1].split("&")[0]
                    if gid not in game_ids:
                        game_ids.append(gid)
                        print("✅ Gevonden gameId:", gid)
                page.go_back()
                page.wait_for_timeout(1000)
            except Exception as e:
                print(f"⚠️ Kon knop {i+1} niet verwerken: {e}")

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
