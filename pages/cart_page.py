import re

class CartPage:

    def __init__(self, page):
        self.page = page

    def open_cart(self):
        self.page.locator("#a-autoid-3").get_by_role("button", name="Add to cart").click()

    def checkout_cart(self):
        self.page.get_by_role("link", name=re.compile(r"items? in cart")).click()

    def clear_cart(self):
        self.page.get_by_role("link", name=re.compile(r"items? in cart")).click()
        form = self.page.locator("#activeCartViewForm")
        while True:
            delete_buttons = form.get_by_role("button", name="Delete")
            if delete_buttons.count() == 0:
                break
            delete_buttons.first.click()
            self.page.wait_for_timeout(1000)