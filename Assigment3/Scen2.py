#Sceanorio 2
import asyncio
import re
import pytest
from playwright.async_api import Page, async_playwright, expect


async def select_and_interact_with_card(page: Page, target_keyword: str):
    # 1. check all  search result cards 

    product_cards = page.locator("div[data-component-type='s-search-result']")
    await expect(product_cards.first).to_be_visible(timeout=10000)
    # 2. check the specific card matching the product name 
    matching_card = product_cards.filter(has=page.locator("h2", has_text=re.compile(re.escape(target_keyword), re.IGNORECASE)))

    # 3. Handle zero-match 
    if await matching_card.count() == 0:
        matching_card = product_cards.filter(has_text=re.compile(re.escape(target_keyword), re.IGNORECASE))

    matches_count = await matching_card.count()
    if matches_count == 0:
        pytest.fail(
            f"Test Failed: No product card found containing '{target_keyword}' in visible search results."
        )

    # Pick the  matching card
    target_card = matching_card.first
    await expect(target_card).to_be_visible()

    title_element = target_card.locator("h2")
    await expect(title_element).to_be_visible()

    visible_title = (await title_element.inner_text()).strip()
    assert target_keyword.lower() in visible_title.lower(), (
        f"Validation Error: Expected keyword '{target_keyword}' inside matched title '{visible_title}'"
    )
    print(f"Validated Card Title: {visible_title}")

    add_to_cart_btn = target_card.locator(
        "button[name='submit.addToCart'], input[name='submit.addToCart'], button:has-text('Add to cart')"
    ).first
    if await add_to_cart_btn.is_visible():
        print("Clicking 'Add to cart' button inside the matched card...")
        await add_to_cart_btn.click()
    else:
        print("Quick 'Add to cart' not visible on card. Clicking the title link inside the card...")
        title_link = target_card.locator("a:has(h2), h2 a, h2").first
        await title_link.click()


@pytest.mark.asyncio
async def test_select_and_interact_card(async_page):
    await async_page.goto("https://www.amazon.in", wait_until="domcontentloaded")
    search_input = async_page.locator("#twotabsearchtextbox")
    await search_input.fill("wireless mouse")
    await search_input.press("Enter")
    await select_and_interact_with_card(async_page, target_keyword="Logitech")
    await async_page.wait_for_timeout(3000)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()

        await page.goto("https://www.amazon.in", wait_until="domcontentloaded")

        search_input = page.locator("#twotabsearchtextbox")
        await search_input.fill("wireless mouse")
        await search_input.press("Enter")
        await select_and_interact_with_card(page, target_keyword="Logitech")

        await asyncio.sleep(3)
        await browser.close()


        if _name_ == "_main_":
           asyncio.run(main())