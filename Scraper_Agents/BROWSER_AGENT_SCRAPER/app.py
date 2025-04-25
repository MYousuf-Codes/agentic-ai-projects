from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=True)
page = browser.new_page()
page.goto("https://www.codewithharry.com")

print(page.content())
print(page.title())
page.screenshot(path="screenshot.png")


