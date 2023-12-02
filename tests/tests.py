import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AdminDashboardTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://localhost:8000/admin-dashboard"  # Update the actual URL
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def login_admin(self):
        self.driver.get("http://localhost:8000/login.html")  # Update the actual URL

        username = self.wait_for_element(By.ID, 'username')
        password = self.wait_for_element(By.ID, 'password')

        username.send_keys("admin")
        password.send_keys("P@ssw0rd")

        login_button = self.wait_for_element(By.ID, 'login-button')
        login_button.click()

    def test_add_staff_and_redirect(self):
        self.login_admin()  # Login as admin first

        # Assuming the "Add Staff" link has the ID 'addStaffLink'
        add_staff_link = self.wait_for_element(By.ID, 'addStaffLink')
        add_staff_link.click()

        # Assuming the fields have the IDs 'first-name', 'username', 'email', 'password', and 'submit-button'
        full_name_input = self.wait_for_element(By.ID, 'first-name')
        username_input = self.wait_for_element(By.ID, 'username')
        email_input = self.wait_for_element(By.ID, 'email')
        password_input = self.wait_for_element(By.ID, 'password')
        submit_button = self.wait_for_element(By.ID, 'submit-button')

        # Fill in the details
        full_name_input.clear()
        full_name_input.send_keys("New Staff")

        username_input.clear()
        username_input.send_keys("newstaff10")

        email_input.clear()
        email_input.send_keys("newstaff@example.com")

        password_input.clear()
        password_input.send_keys("P@ssw0rd")

        # Click the "Add Staff" button
        submit_button.click()

        # Wait for the page to load after form submission
        time.sleep(2)  # You can adjust the sleep time based on your application's actual loading time

        # Print the current URL for debugging
        print("Current URL:", self.driver.current_url)

        # Assert that the page is redirected to 'adminstaff.html'
        self.assertIn("admin-dashboard", self.driver.current_url)

if __name__ == "__main__":
    unittest.main()

print("Login with valid username and password")
print("Add new staff to the laboratory using essential credentials")