

class HomePage:

    def __init__(self, page):
        self.page = page

    def search_product(self, product):
        # self.page.goto("https://www.amazon.in/?ref_=nav_signin")
        search_box = self.page.get_by_role("searchbox", name="Search Amazon.in")
        search_box.fill("")
        search_box.press_sequentially(product, delay=100)
        search_box.press("Enter")

    def find_with_spec(self, product, specs):
        checked = 0
        while checked < 20:
            products = (self.page.locator(".s-result-list").get_by_role("listitem").filter(has_text=product))
            count = products.count()
            for i in range(count):
                if checked >= 20:
                    break
                product = products.nth(i)
                class_name = product.get_attribute("class") or ""
                # Go to next page
                if any(cls.startswith("textref") for cls in class_name.split()):
                    next_page = self.page.get_by_role("button", name="Go to next page, page")
                    if next_page.count() == 0:
                        return False
                    next_page.click()
                    self.page.wait_for_load_state("domcontentloaded")
                    break

                if not product.is_visible():
                    continue

                product.scroll_into_view_if_needed()
                text = product.inner_text().lower()

                if all(spec.lower() in text for spec in specs):
                    product.click()
                    return True
                    # add_to_cart = product.get_by_role("button", name="Add to cart")
                    # if add_to_cart.count() > 0:
                    #     add_to_cart.first.click()
                    #     return True
                checked += 1
            else:
                self.page.mouse.wheel(0, 800)
                self.page.wait_for_timeout(1000)
        return False
