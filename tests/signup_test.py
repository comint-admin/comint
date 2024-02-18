import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SignupPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.get("http://127.0.0.1:8000/accounts/signup/")  

    def tearDown(self):
        self.driver.quit()

    def test_signup_form_elements_present(self):
        driver = self.driver
        # Check  signup form elements are present
        email_field = driver.find_element_by_id('id_email')
        first_name_field = driver.find_element_by_id('id_first_name')
        last_name_field = driver.find_element_by_id('id_last_name')
        password_field = driver.find_element_by_id('passwordField1')
        password_confirm_field = driver.find_element_by_id('passwordField2')
        captcha_field = driver.find_element_by_id('id_captcha')
        terms_checkbox = driver.find_element_by_id('id_tc')

        self.assertTrue(email_field.is_displayed())
        self.assertTrue(first_name_field.is_displayed())
        self.assertTrue(last_name_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(password_confirm_field.is_displayed())
        self.assertTrue(captcha_field.is_displayed())
        self.assertTrue(terms_checkbox.is_displayed())

    def test_signup_form_validation(self):
        driver = self.driver
        # Fill in the form fields
        email_field = driver.find_element_by_id('id_email')
        email_field.send_keys("invalidemail")  # Invalid email format
        first_name_field = driver.find_element_by_id('id_first_name')
        first_name_field.send_keys("John")
        last_name_field = driver.find_element_by_id('id_last_name')
        last_name_field.send_keys("Doe")
        password_field = driver.find_element_by_id('passwordField1')
        password_field.send_keys("password")
        password_confirm_field = driver.find_element_by_id('passwordField2')
        password_confirm_field.send_keys("password")
        #captcha_field = driver.find_element_by_id('id_captcha')
        #captcha_field.send_keys("123456")  # Assuming captcha value
        terms_checkbox = driver.find_element_by_id('id_tc')
        terms_checkbox.click()

        # Submit the form
        signup_button = driver.find_element_by_css_selector('.btn-block[type="submit"]')
        signup_button.click()

        # Wait for error messages to appear
        #error_messages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.alert-danger')))
        
        # Check if error messages are displayed
        #self.assertGreater(len(error_messages), 0)

    def test_successful_signup(self):
        driver = self.driver
        
        email_field = driver.find_element_by_id('id_email')
        email_field.send_keys("validemail@example.com")
        first_name_field = driver.find_element_by_id('id_first_name')
        first_name_field.send_keys("John")
        last_name_field = driver.find_element_by_id('id_last_name')
        last_name_field.send_keys("Doe")
        password_field = driver.find_element_by_id('passwordField1')
        password_field.send_keys("StrongPassword1")
        password_confirm_field = driver.find_element_by_id('passwordField2')
        password_confirm_field.send_keys("StrongPassword1")
       # captcha_field = driver.find_element_by_id('id_captcha')
        #captcha_field.send_keys("123456")  # Assuming captcha value
        terms_checkbox = driver.find_element_by_id('id_tc')
        terms_checkbox.click()

        # Submit the form
        signup_button = driver.find_element_by_css_selector('.btn-block[type="submit"]')
        signup_button.click()

    def test_captcha_displayed(self):
        driver = self.driver
        # Check if captcha field is displayed
        captcha_field = driver.find_element_by_id('id_captcha')
        self.assertTrue(captcha_field.is_displayed())
    
    def test_password_length_validation(self):
        driver = self.driver
        # Fill in the form fields
        email_field = driver.find_element_by_id('id_email')
        email_field.send_keys("validemail@example.com")
        first_name_field = driver.find_element_by_id('id_first_name')
        first_name_field.send_keys("John")
        last_name_field = driver.find_element_by_id('id_last_name')
        last_name_field.send_keys("Doe")
        password_field = driver.find_element_by_id('passwordField1')
        password_field.send_keys("short")  # Password length less than minimum required
        password_confirm_field = driver.find_element_by_id('passwordField2')
        password_confirm_field.send_keys("short")  # Password length less than minimum required
        #captcha_field = driver.find_element_by_id('id_captcha')
        #captcha_field.send_keys("123456")  # Assuming captcha value
        terms_checkbox = driver.find_element_by_id('id_tc')
        terms_checkbox.click()

        signup_button = driver.find_element_by_css_selector('.btn-block[type="submit"]')
        signup_button.click()

        # Wait for error messages to appear
        error_messages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.alert-danger')))
        
        # Check if error message for password length validation is displayed
        password_length_error_message = "Password must be at least 8 characters long."
        self.assertIn(password_length_error_message, [msg.text for msg in error_messages])

if __name__ == "__main__":
    unittest.main()
