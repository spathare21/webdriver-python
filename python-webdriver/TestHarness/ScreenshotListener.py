from selenium.webdriver.support.events import AbstractEventListener
import time
import logging
import os

class ScreenshotListener(AbstractEventListener):

    def __init__(self):
        self.basename = "/tmp/screenshots/"
        if "SCREENSHOTDIR" in os.environ:
            self.basename = os.environ.get("SCREENSHOTDIR")
        assert(not os.path.isfile(self.basename))
        if not str(self.basename).endswith("/"):
            self.basename += "/"
        if not os.path.isdir(self.basename):
            os.makedirs(self.basename)

    def on_exception(self, exception, driver):
        self.take_screenshot(driver, '_exception')

    def before_click(self, element, driver):
        self.take_screenshot(driver, '_pre-click')

    def after_click(self, element, driver):
        self.take_screenshot(driver, '_post-click')

    def after_navigate_to(self, url, driver):
        self.take_screenshot(driver, '_nav-to')

    def before_navigate(self, element, driver):
        self.take_screenshot(driver, '_pre-nav')

    def after_navigate(self, element, driver):
        self.take_screenshot(driver, '_post-nav')

    def take_screenshot(self, driver, name):
        time.sleep(1)
        name = self.basename + str(time.time()) + name + '.png'
        driver.get_screenshot_as_file(name)
        logging.info("Screenshot saved as '%s'" % name)
