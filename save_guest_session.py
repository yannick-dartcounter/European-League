from playwright.sync_api import sync_playwright

URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

def save_guest_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌍 Open de pagina en log handmatig in als gast...")
        page.goto(URL)

        print("🕒 Wacht tot je handmatig op de bracketpagina bent...")
        input("📲 Druk op Enter als je de bracket ziet...")

        print("💾 Sla sessie op in 'guest_state.json'")
        context.storage_state(path="guest_state.json")

        browser.close()

if __name__ == "__main__":
    save_guest_session()
