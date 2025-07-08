from playwright.sync_api import sync_playwright

def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://app.dartcounter.net/login")
        print("🔐 Log nu handmatig in en ga naar een toernooipagina...")

        page.wait_for_url("**/tournaments/**", timeout=300000)
        context.storage_state(path="dartcounter_session.json")
        print("✅ Sessie opgeslagen als dartcounter_session.json")

        browser.close()

if __name__ == "__main__":
    save_login_session()
