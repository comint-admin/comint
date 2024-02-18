import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class LoginPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome() 
        self.driver.get("http://127.0.0.1:8000/accounts/login/")  

    def tearDown(self):
        self.driver.quit()

    def test_login_form_elements_present(self):
        driver = self.driver
        # Check if the login form elements are present
        email_field = driver.find_element_by_id('id_login')
        password_field = driver.find_element_by_id('id_password')
        remember_checkbox = driver.find_element_by_id('form1Example3')
        captcha_field = driver.find_element_by_id('id_captcha')

        self.assertTrue(email_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        self.assertTrue(remember_checkbox.is_displayed())
        self.assertTrue(captcha_field.is_displayed())

    def test_login_form_validation(self):
        driver = self.driver
        # Fill in the form fields with invalid inputs
        email_field = driver.find_element_by_id('id_login')
        email_field.send_keys("invalidemail")  # Invalid email format
        password_field = driver.find_element_by_id('id_password')
        password_field.send_keys("short")  # Short password
        #captcha_field = driver.find_element_by_id('id_captcha')
        #captcha_field.send_keys("123456")  # Assuming captcha value

        # Submit the form
        login_button = driver.find_element_by_css_selector('.btn.btn-lg.btn-block')
        login_button.click()

        try:
            # Wait for error messages to appear
            error_messages = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.alert.alert-danger')))
            
            # Check if error messages contain the expected text
            expected_error_message = "The email address and/or password you specified are not correct."
            error_texts = [msg.text for msg in error_messages]
            self.assertIn(expected_error_message, error_texts)
        except TimeoutException as e:
            print("Timeout occurred while waiting for error messages to appear:", e)




    def test_successful_login(self):
        driver = self.driver
        # Fill in the form fields with valid inputs
        email_field = driver.find_element_by_id('id_login')
        email_field.send_keys("validemail@example.com")
        password_field = driver.find_element_by_id('id_password')
        password_field.send_keys("StrongPassword1")
        #captcha_field = driver.find_element_by_id('id_captcha')
        #captcha_field.send_keys("123456")  # Assuming captcha value

        # Submit the form
        login_button = driver.find_element_by_css_selector('.btn.btn-lg.btn-block')
        login_button.click()

        # Wait for successful redirection or presence of success message



    def test_successful_login(self):
        # Test to check if user can successfully log in with valid credentials
        driver = self.driver
        # Fill in the login form with valid credentials
        email_field = driver.find_element_by_id('id_login')
        email_field.send_keys("validemail@example.com") #-- > valide email after verifing process
        password_field = driver.find_element_by_id('id_password')
        password_field.send_keys("StrongPassword1") # valid password
        captcha_checkbox = driver.find_element_by_id('id_captcha')
        captcha_checkbox.click()
        # Submit the login form
        login_button = driver.find_element_by_css_selector('.btn[type="submit"]')
        login_button.click()
        ##try:
            #WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/accounts/confirm-email/"))  
       # except TimeoutException:
           # self.fail("Successful login redirection not completed within timeout period")


if __name__ == "__main__":
    unittest.main()
