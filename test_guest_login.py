from playwright.sync_api import sync_playwright

URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

def test_guest_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌍 Open pagina...")
        page.goto(URL)
        page.wait_for_timeout(2000)

        # Klik op 'Continue without account'
        try:
            guest_btn = page.get_by_text("Continue without account")
            guest_btn.click()
            print("👤 Gastoptie geklikt")
            page.wait_for_timeout(2000)
        except:
            print("❌ Gastoptie niet gevonden")

        # Klik op checkbox
        try:
            checkbox = page.query_selector("div.flex.flex-none.items-center.justify-center.rounded-sm")
            checkbox.click(force=True)
            print("☑️ Checkbox aangevinkt")
            page.wait_for_timeout(1000)
        except:
            print("❌ Checkbox niet gevonden")

        # Klik op Continue
        try:
            continue_btn = page.query_selector("button:has-text('Continue')")
            continue_btn.click(force=True)
            print("➡️ Klik op 'Continue'...")
        except:
            print("❌ Continue-knop niet gevonden")

        # Wacht op specifiek element op bracketpagina (bijv. bracket container)
        try:
            page.wait_for_selector("svg", timeout=10000)
            print("✅ Bracketpagina geladen 🎯")
        except:
            print("❌ Bracketpagina niet gevonden")

        page.screenshot(path="guest_flow_test.png")
        print("📸 Screenshot opgeslagen")

        browser.close()

if __name__ == "__main__":
    test_guest_flow()
