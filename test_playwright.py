from playwright.sync_api import sync_playwright

def test_page():
    url = "https://app.dartcounter.net/tournaments/european-league-day-2-2piSdd/bracket"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("table")  # wacht tot een <table> verschijnt
        html = page.content()
        print("✅ HTML geladen, lengte:", len(html))
        if "<table" in html:
            print("✅ Tabellen aanwezig! Eerste 500 karakters:")
            start = html.find("<table")
            print(html[start:start+500])
        else:
            print("❌ Helaas: nog steeds geen <table> gevonden.")
        browser.close()

if __name__ == "__main__":
    test_page()
