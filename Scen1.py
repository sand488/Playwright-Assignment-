
from playwright.sync_api import expect
def test_get_by_label(page):
    page.goto("https://demowebshop.tricentis.com/")
    register_link = page.get_by_text("Register")
    register_link.click()
    page.get_by_label("Female").nth(0).check()
    page.get_by_label("First name:").fill("sandhya")
    page.get_by_label("Last name:").fill("Bhaskaran")
    page.get_by_label("Email:").fill("sandyabhaskar1@gmail.com")
    page.get_by_label("Password:").nth(0).fill("san899")
    page.wait_for_timeout(1000)


  