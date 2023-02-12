import re
import sys
import urllib.request

import modal

stub = modal.Stub(name="link-scraper")

# Create the container in code
# Install Playwright and Chromium for web scrap
playwright_image = modal.Image.debian_slim().run_commands(
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "apt-get update",
    "pip install playwright==1.20.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)


@stub.function(image=playwright_image)
# @stub.function(schedule=modal.Period(days=1))  # This allows us to schedule job in period, run with modal deploy
async def get_links(cur_url: str):
    # We are not running these code locally
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(cur_url)
        links = await page.eval_on_selector_all("a[href]", "elements => elements.map(element => element.href)")
        await browser.close()

    print("Links", links)
    return links


if __name__ == "__main__":
    urls = ["http://modal.com", "http://github.com"]
    with stub.run():
        # Here we use map to run the process in parallel
        for links in get_links.map(urls):
            for link in links:
                print(link)
