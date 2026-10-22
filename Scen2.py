import pytest
from playwright.async_api import expect

#1.user registration 
@pytest.mark.asyncio
async def test_bank(async_page):
    await async_page.goto("https://parabank.parasoft.com/parabank/index.htm")
    await async_page.wait_for_timeout(5000)
    await async_page.locator("//a[text()='Register']").click()
    await async_page.locator("#customer\\.firstName").fill("Sandhya")
    await async_page.locator("#customer\\.lastName").fill("Bhaskaran")
    await async_page.locator("#customer\\.address\\.street").fill("Austin street")
    await async_page.locator("#customer\\.address\\.city").fill("Bangalore")
    await async_page.locator("#customer\\.address\\.state").fill("karnataka")
    await async_page.locator("#customer\\.address\\.zipCode").fill("560047")
    await async_page.locator("#customer\\.phoneNumber").fill("8848508634")
    await async_page.locator("#customer\\.ssn").fill("12345678")
    await async_page.locator("#customer\\.username").fill("Sandy12390")
    await async_page.locator("#customer\\.password").fill("123456785676")
    await async_page.locator("#repeatedPassword").fill("123456785676")

    await async_page.locator("input[value='Register']").click()
     # Verify registration is successful
    await expect(async_page.locator("text=Your account was created successfully.")).to_be_visible()

    # Verify user is logged in
    await expect(async_page.locator("text=Log Out")).to_be_visible()

    
    
    
     # Logout
    await async_page.locator("a:has-text('Log Out')").click()

    # Verify logout
    await expect(async_page.locator("text=Customer Login")).to_be_visible()

#2.open new account & Verify Account   
@pytest.mark.asyncio
async def test_open_new_account(async_page):

    # Login to ParaBank
    await async_page.goto( "https://parabank.parasoft.com/parabank/index.htm")

    await async_page.locator("//input[@name='username']").fill("Sandy12390")

    await async_page.locator("//input[@name='password']").fill("123456785676")

    await async_page.locator("//input[@value='Log In']").click()

    # Navigate to Open New Account
    await async_page.locator("//a[text()='Open New Account']").click()

    # Select account type
    await async_page.locator("//select[@id='type']").select_option("1")

    # Select existing account
    await async_page.locator("//select[@id='fromAccountId']").select_option(index=0)

    # Click Open New Account
    await async_page.locator("//input[@value='Open New Account']").click()

    # Verify account is successfully created
    await expect(async_page.locator("//h1[text()='Account Opened!']")).to_be_visible()

    # # Capture newly generated account number
    # account_number = async_page.locator("//a[@id='newAccountId']" )

    # await expect(account_number).to_be_visible()

    # new_account_number = await account_number.inner_text()

    # print("New Account Number:", new_account_number)

    # # Navigate to Accounts Overview
    # await async_page.locator("//a[text()='Accounts Overview']").click()

    # # Verify Accounts Overview
    # await expect(async_page.locator("//h1[text()='Accounts Overview']") ).to_be_visible()

    #    # Verify newly created account is displayed
    # await expect(
    #     async_page.locator(f"//a[text()='{new_account_number}']")).to_be_visible()

    # print(f"New account {new_account_number} is displayed successfully.")
