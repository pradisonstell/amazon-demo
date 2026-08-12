


class PaymentPage:

    def __init__(self, page):
        self.page = page

    def close_payment_page(self):
        self.page.locator('input[name="proceedToRetailCheckout"]').click()
        self.page.get_by_role("link", name="Back to cart").click()
        print("Closing Payment Page")