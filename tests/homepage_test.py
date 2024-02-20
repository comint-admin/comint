import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  
        self.driver.get("http://127.0.0.1:8000/")  

    def tearDown(self):
        self.driver.quit()

    def test_hero_section(self):
        # Test if the hero section exists and contains expected elements
        hero_background = self.driver.find_element(By.ID, "hero-background")
        self.assertTrue(hero_background.is_displayed())

        main_content = hero_background.find_element(By.ID, "main-content")
        self.assertTrue(main_content.is_displayed())

        main_content_words = main_content.find_element(By.ID, "main-content-words")
        self.assertTrue(main_content_words.is_displayed())

        main_content_img = main_content.find_element(By.ID, "main-content-img")
        self.assertTrue(main_content_img.is_displayed())

    def test_bottom_wrapper(self):
        # Test wrapper section exists and contains expected elements
        bottom_wrapper = self.driver.find_element(By.CLASS_NAME, "bottom-wrapper")
        self.assertTrue(bottom_wrapper.is_displayed())

        bottom_content = bottom_wrapper.find_element(By.CLASS_NAME, "bottom-content")
        self.assertTrue(bottom_content.is_displayed())

    def test_how_it_works_section(self):
        # Test if the "How it works" section exists and contains expected elements
        how_it_works = self.driver.find_element(By.ID, "how-it-works")
        self.assertTrue(how_it_works.is_displayed())

        hiw_header = how_it_works.find_element(By.CLASS_NAME, "hiw-header")
        self.assertTrue(hiw_header.is_displayed())

        hiw_upperbody = how_it_works.find_element(By.CLASS_NAME, "hiw-upperbody")
        self.assertTrue(hiw_upperbody.is_displayed())

        step_grid = how_it_works.find_element(By.CLASS_NAME, "step-grid")
        self.assertTrue(step_grid.is_displayed())
    
    def test_modal_input_fields(self):
        # Click the button to open the waitlist modal
        waitlist_button = self.driver.find_element(By.CSS_SELECTOR, ".btn[data-bs-target='#waitlistModal']")
        waitlist_button.click()

        waitlist_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "waitlistModal"))
        )

        # Find  fields in the modal
        firstname_input = waitlist_modal.find_element(By.ID, "waitlist-firstname")
        lastname_input = waitlist_modal.find_element(By.ID, "waitlist-lastname")
        email_input = waitlist_modal.find_element(By.ID, "exampleInputEmail1")
        phone_input = waitlist_modal.find_element(By.ID, "waitlist-lastname") 

        # Check if the input fields are displayed and enabled
        self.assertTrue(firstname_input.is_displayed() and firstname_input.is_enabled())
        self.assertTrue(lastname_input.is_displayed() and lastname_input.is_enabled())
        self.assertTrue(email_input.is_displayed() and email_input.is_enabled())
        self.assertTrue(phone_input.is_displayed() and phone_input.is_enabled()) 



    def test_waitlist_modal(self):
        #  waitlist modal button
        waitlist_button = self.driver.find_element(By.CSS_SELECTOR, ".btn[data-bs-target='#waitlistModal']")
        waitlist_button.click()

        # Wait to be displayed (wait up to 10 seconds)
        waitlist_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "waitlistModal"))
        )
        self.assertTrue(waitlist_modal.is_displayed())

    def test_join_waitlist_button(self):
        # Test  "Join waitlist" button exists and is clickable
        join_waitlist_button = self.driver.find_element(By.CSS_SELECTOR, "[data-bs-target='#waitlistModal']")
        self.assertTrue(join_waitlist_button.is_displayed())
        join_waitlist_button.click()

        # After clicking, verify that the waitlist modal is displayed
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal")))

    def test_learn_more_button(self):
        # Scroll to the "Learn more" button
        learn_more_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Learn more >')]")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", learn_more_button)

        learn_more_button.click()

if __name__ == "__main__":
    unittest.main()
