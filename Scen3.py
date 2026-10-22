import pytest
from playwright.async_api import expect


# Scenario 3: Open New Account & Verify Account

@pytest.mark.asyncio
async def test_open_new_account(async_page):

    # Step 1: Open ParaBank
    await async_page.goto(
        "https://parabank.parasoft.com/parabank/index.htm"
    )

    # Step 2: Login
    await async_page.locator(
        "//input[@name='username']"
    ).fill("Sandy1239000")

    await async_page.locator(
        "//input[@name='password']"
    ).fill("123456785676")

    await async_page.locator(
        "//input[@value='Log In']"
    ).click()

    # Step 3: Verify successful login
    open_account_link = async_page.get_by_role(
        "link", name="Open New Account", exact=True
    )

    try:
        await expect(open_account_link).to_be_visible(timeout=15000)
    except AssertionError:
        page_text = await async_page.locator("body").inner_text()
        pytest.fail(
            "Login failed or Open New Account link is unavailable.\n"
            f"Current URL: {async_page.url}\n"
            f"Page content:\n{page_text[:1000]}"
        )

    print("Login successful!")

    # Step 4: Navigate to Open New Account
    await open_account_link.click()

    # Step 5: Select account type (1 = Savings)
    await async_page.locator("#type").select_option("1")

    # Step 6: Wait for existing accounts to load
    from_account = async_page.locator("#fromAccountId")

    await expect(from_account).to_be_visible(timeout=15000)

    account_options = from_account.locator("option")
    await expect(account_options.first).to_be_attached()

    # Select the first available existing account
    await from_account.select_option(index=0)

    # Step 7: Open the new account
    await async_page.locator(
        "//input[@value='Open New Account']"
    ).click()

    # Step 8: Verify account creation
    await expect(
        async_page.get_by_role(
            "heading", name="Account Opened!", exact=True
        )
    ).to_be_visible(timeout=15000)

    # Step 9: Capture the generated account number
    account_number = async_page.locator("#newAccountId")

    await expect(account_number).to_be_visible(timeout=15000)

    new_account_number = (
        await account_number.inner_text()
    ).strip()

    assert new_account_number, "New account number was not generated."

    print("New Account Number:", new_account_number)

    # Step 10: Navigate to Accounts Overview
    await async_page.get_by_role(
        "link", name="Accounts Overview", exact=True
    ).click()

    # Step 11: Verify Accounts Overview
    await expect(
        async_page.get_by_role(
            "heading", name="Accounts Overview", exact=True
        )
    ).to_be_visible(timeout=15000)

    # Step 12: Verify the new account appears in the account list
    new_account_link = async_page.locator(
        f"#accountTable a:text-is('{new_account_number}')"
    )

    await expect(new_account_link).to_be_visible(timeout=15000)

    print(
        f"New account {new_account_number} "
        "is displayed successfully."
    )