from playwright.sync_api import sync_playwright

BRACKET_URL = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(BRACKET_URL)
    page.wait_for_timeout(2000)

    # Stap 1: klik "Continue without account"
    page.click("text=Continue without account", timeout=5000)
    page.wait_for_timeout(2000)

    # 🔎 Stap 2: zie of er een checkbox is
    checkbox = page.query_selector("input[type=checkbox]")
    print("🧩 Checkbox aanwezig?" , bool(checkbox), "attribuut:", checkbox.get_attribute("type") if checkbox else None)

    if checkbox:
        checkbox.check()
        print("☑️ Checkbox aangevinkt")

    # 🔎 Zoek dan knop met "Continue"
    button = page.query_selector("button:has-text('Continue')")
    print("➡️ Continue-knop gevonden?", bool(button))

    browser.close()
