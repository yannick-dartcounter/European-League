from playwright.sync_api import sync_playwright

URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

def test_guest_dispatch_event():
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

        # Vind checkbox en activeer met dispatch_event
        try:
            checkbox = page.query_selector("div.flex.flex-none.items-center.justify-center.rounded-sm")
            if checkbox:
                checkbox.dispatch_event("click")
                print("☑️ Checkbox geactiveerd via dispatch_event")
                page.wait_for_timeout(1000)
            else:
                print("❌ Checkbox niet gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij checkbox: {e}")

        # Klik op Continue
        try:
            continue_btn = page.query_selector("button:has-text('Continue')")
            if continue_btn:
                continue_btn.click(force=True)
                print("➡️ Klik op 'Continue'...")
            else:
                print("❌ Continue-knop niet gevonden")
        except Exception as e:
            print(f"⚠️ Fout bij klikken op Continue: {e}")

        # Wacht op de bracketpagina
        try:
            page.wait_for_selector("svg", timeout=10000)
            print("✅ Bracketpagina geladen 🎯")
        except:
            print("❌ Bracketpagina niet gevonden")

        page.screenshot(path="guest_dispatch_test.png")
        print("📸 Screenshot opgeslagen")

        browser.close()

if __name__ == "__main__":
    test_guest_dispatch_event()
