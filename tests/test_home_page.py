from pages.home_page import HomePage
from playwright.sync_api import expect


def test_home_page(auth_page):
    auth_page.goto("https://www.amazon.in/")
    home_page = HomePage(auth_page)
    home_page.search_product("iPhone 17")
    expect(auth_page.get_by_role("searchbox", name="Search Amazon.in")).to_have_value("iPhone 17")