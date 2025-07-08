from playwright.sync_api import sync_playwright
import time
import json

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
OUTPUT_FILE = "game_data.json"

def scrape_game_ids():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth_session.json")
        page = context.new_page()

        print("🌍 Bracketpagina openen...")
        page.goto(BRACKET_URL)
        page.wait_for_selector("svg", timeout=10000)
        page.wait_for_timeout(2000)

        # Zoek alle SVG rects
        rects = page.query_selector_all("svg rect")
        print(f"🔲 Aantal SVG-rects gevonden: {len(rects)}")

        game_ids = []
        clicked = 0

        for i, rect in enumerate(rects):
            try:
                box = rect.bounding_box()
                if not box:
                    continue

                # Filter: klik alleen op brede, platte blokken (typisch voor "View details")
                if not (250 <= box["width"] <= 270 and 30 <= box["height"] <= 34):
                    continue

                print(f"🟧 Klik op rect {i}: breedte={box['width']}, hoogte={box['height']}")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(1500)

                # Check: redirect?
                if "/statistics/match/details?gameId=" in page.url:
                    gid = page.url.split("gameId=")[-1]
                    if gid not in game_ids:
                        game_ids.append(gid)
                        print(f"✅ GameId (redirect): {gid}")
                    page.go_back()
                    page.wait_for_timeout(1500)
                    clicked += 1
                    continue

                # Check: popup geopend?
                popup_links = page.query_selector_all("a[href*='gameId=']")
                found_popup = False
                for link in popup_links:
                    href = link.get_attribute("href")
                    if href:
                        gid = href.split("gameId=")[-1]
                        if gid not in game_ids:
                            game_ids.append(gid)
                            print(f"✅ GameId (popup): {gid}")
                            found_popup = True
                if found_popup:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)
                    clicked += 1

            except Exception as e:
                print(f"⚠️ Fout bij SVG {i}: {e}")
                continue

        # Sla alle gevonden gameIds op
        with open(OUTPUT_FILE, "w") as f:
            json.dump(game_ids, f, indent=2)

        print(f"\n💾 {len(game_ids)} unieke gameIds opgeslagen in '{OUTPUT_FILE}'")
        print(f"🔁 {clicked} 'View details' knoppen verwerkt")

        browser.close()

if __name__ == "__main__":
    scrape_game_ids()
