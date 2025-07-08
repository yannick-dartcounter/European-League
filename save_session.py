from playwright.sync_api import sync_playwright

def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Open nieuwe pagina en laad de loginpagina
        page = context.new_page()
        page.goto("https://app.dartcounter.net/login")

        print("🔐 Log nu handmatig in. Sluit dit venster pas als je volledig bent ingelogd.")

        # Wacht tot gebruiker op bracketpagina zit
        page.wait_for_url("**/tournaments/**", timeout=300000)  # 5 minuten de tijd

        # Sla login cookies en local storage op
        context.storage_state(path="dartcounter_session.json")
        print("✅ Sessie opgeslagen als dartcounter_session.json")

        browser.close()

if __name__ == "__main__":
    save_login_session()
