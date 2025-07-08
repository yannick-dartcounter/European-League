from playwright.sync_api import sync_playwright
import requests
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
STORAGE_FILE = "dartcounter_session.json"
SCREENSHOT_PATH = "screenshot.png"

def get_game_ids_from_svg_clicks():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STORAGE_FILE)
        page = context.new_page()

        print("🌍 Pagina laden...")
        page.goto(BRACKET_URL)
        page.wait_for_timeout(7000)
        page.screenshot(path=SCREENSHOT_PATH)

        # Zoek SVG-elementen (bijv. <rect>)
        rects = page.query_selector_all("svg rect")
        print(f"🔲 Aantal SVG-rects gevonden: {len(rects)}")

        found_game_ids = []

        for i, rect in enumerate(rects):
            try:
                print(f"🖱 Klik rect {i+1}/{len(rects)}")
                rect.click(force=True)
                page.wait_for_timeout(1000)

                modal = page.query_selector(".MuiDialog-root")
                if not modal:
                    print("⚠️ Geen popup gevonden")
                    continue

                # Zoek in modal naar gameId via tekst of attribuut
                inner = modal.inner_text()
                if 'gameId' in inner:
                    start = inner.find('gameId')
                    snippet = inner[start:start+40]  # stukje tekst erna
                    print("🧩 Ruwe gameId-snippet:", snippet)

                # Zoek gameId als data-attribuut in een button/link
                gid_element = modal.query_selector("[data-id]")
                if gid_element:
                    gid = gid_element.get_attribute("data-id")
                    if gid and gid not in found_game_ids:
                        found_game_ids.append(gid)
                        print("✅ Gevonden gameId:", gid)

                # Alternatief: check op API-url in <a href>
                links = modal.query_selector_all("a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and "/games/" in href:
                        gid = href.split("/games/")[-1]
                        if gid and gid not in found_game_ids:
                            found_game_ids.append(gid)
                            print("✅ Gevonden gameId via href:", gid)

                # Sluit popup
                close_btn = page.query_selector("button[aria-label='Close']")
                if close_btn:
                    close_btn.click()
                    page.wait_for_timeout(500)

            except Exception as e:
                print(f"❌ Fout bij rect {i}: {e}")

        browser.close()
        return found_game_ids

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
    print("🚀 Start scraping via SVG-clicks...")
    ids = get_game_ids_from_svg_clicks()
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
