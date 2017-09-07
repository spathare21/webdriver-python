from selenium.webdriver.support.events import AbstractEventListener
import time
import logging


class ScreenshotListener(AbstractEventListener):

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
        name = '/tmp/screenshots/' + str(time.time()) + name + '.png'
        driver.get_screenshot_as_file(name)
        logging.info("Screenshot saved as '%s'" % name)
