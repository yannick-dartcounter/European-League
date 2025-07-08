from playwright.sync_api import sync_playwright

URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

def save_guest_session():
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

        # Vink checkbox aan
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

        # Jij klikt nu handmatig op 'Continue'
        print("🕹️ Klik nu handmatig op 'Continue'...")
        input("✅ Druk op Enter zodra je de bracket ziet...")

        # Sla sessie op
        context.storage_state(path="guest_state.json")
        print("💾 Sessiestatus opgeslagen in 'guest_state.json' ✅")

        browser.close()

if __name__ == "__main__":
    save_guest_session()
