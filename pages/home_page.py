

class HomePage:

    def __init__(self, page):
        self.page = page

    def search_product(self, product):
        # self.page.goto("https://www.amazon.in/?ref_=nav_signin")
        self.page.get_by_role("searchbox", name="Search Amazon.in").fill(product)
        self.page.get_by_role("searchbox", name="Search Amazon.in").press("Enter")