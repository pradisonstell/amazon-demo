

class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.goto("https://www.amazon.in/")
        if self.page.get_by_role("button", name="Continue shopping").is_visible():
            self.page.get_by_role("button", name="Continue shopping").click()
        self.page.get_by_role("link", name="Hello, sign in Account & Lists").click()


        self.page.get_by_role("textbox", name="Enter mobile number or email").fill(username)
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Sign in", exact=True).click()
