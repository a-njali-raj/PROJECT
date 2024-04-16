import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000/login.html"
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def test_successful_navigation_to_product(self):
        self.driver.get(self.base_url)

        username = self.wait_for_element(By.ID, 'username')
        password = self.wait_for_element(By.ID, 'password')

        username.send_keys("anu")
        password.send_keys("Anu@12345")

        login_button = self.wait_for_element(By.ID, 'login-button')
        login_button.click()

        # Introduce a delay of 2 seconds before clicking the "Buy now" button
        time.sleep(2)

        buy_now_button = self.wait_for_element(By.ID, 'buynow')
        buy_now_button.click()

        # Introduce another delay of 2 seconds before asserting the URL
        time.sleep(2)

        # Assert that the current URL is the product.html page
        self.assertIn("product.html", self.driver.current_url)

        # Find the "Add to Cart" button and click on it
        add_to_cart_button = self.wait_for_element(By.CSS_SELECTOR, ".btn-add-to-cart")
        add_to_cart_button.click()

        # Wait for some time for the cart to be updated (You might need to adjust this time)
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
print(" Product add to cart")
