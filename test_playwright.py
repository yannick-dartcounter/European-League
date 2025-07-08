from playwright.sync_api import sync_playwright

def test_page():
    url = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # zet headless op False om te zien wat er gebeurt
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # wacht 5 seconden om pagina te laten laden

        html = page.content()

        # Zoek alle knoppen met game ID's (vaak via data-game-id of data-id)
        buttons = page.query_selector_all("button, a, div")

        print("Aantal elementen:", len(buttons))
        for el in buttons:
            attr = el.get_attribute("data-id") or el.get_attribute("data-game-id")
            text = el.inner_text().strip()
            if attr:
                print(f"🔹 Game ID: {attr} | Tekst: {text[:30]}")

        browser.close()

if __name__ == "__main__":
    test_page()
