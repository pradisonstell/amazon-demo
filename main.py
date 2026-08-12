import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage


load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def run(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    home_page = HomePage(page)
    cart_page = CartPage(page)
    payment_page = PaymentPage(page)


    print("USERNAME", USERNAME)
    print("PASSWORD", PASSWORD)

    login_page.login(USERNAME, PASSWORD)
    home_page.search_product("iPhone 17")
    cart_page.add_to_cart()
    cart_page.checkout_cart()
    payment_page.close_payment_page()
    cart_page.clear_cart()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
