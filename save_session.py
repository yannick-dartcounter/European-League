from playwright.sync_api import sync_playwright

URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

def save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌍 Ga nu handmatig naar de bracketpagina")
        page.goto(URL)

        input("🔐 Log in en druk op Enter zodra je de bracket ziet...")

        context.storage_state(path="auth_session.json")
        print("💾 Sessie opgeslagen in 'auth_session.json' ✅")

        browser.close()

if __name__ == "__main__":
    save_session()
