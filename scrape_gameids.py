from playwright.sync_api import sync_playwright
import json
import time

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
OUTPUT_FILE = "game_data.json"

def scrape_game_ids_with_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth_session.json")  # gebruik opgeslagen sessie
        page = context.new_page()

        print("🌍 Bezoek de bracketpagina...")
        page.goto(BRACKET_URL)
        page.wait_for_timeout(3000)

        # Wacht tot de bracket zichtbaar is
        try:
            page.wait_for_selector("svg", timeout=10000)
            print("✅ Bracketpagina geladen")
        except:
            print("❌ Kon bracket niet laden")
            return

        # Zoek alle "View details"-links
        print("🔍 Zoek wedstrijdlinks...")
        links = page.query_selector_all("a")
        game_ids = []

        for link in links:
            href = link.get_attribute("href")
            if href and "/statistics/match/details?gameId=" in href:
                game_id = href.split("gameId=")[-1].split("&")[0]
                if game_id not in game_ids:
                    game_ids.append(game_id)
                    print("✅ Gevonden gameId:", game_id)

        browser.close()

        # Opslaan als JSON
        with open(OUTPUT_FILE, "w") as f:
            json.dump(game_ids, f, indent=2)

        print(f"💾 {len(game_ids)} gameIds opgeslagen in '{OUTPUT_FILE}'")

if __name__ == "__main__":
    scrape_game_ids_with_session()
