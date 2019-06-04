import logging

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver

from TestConfig import TestRunConfig
from TestHarness import ScreenshotListener


class WebDriverModule:
    """
      Provides a persistent driver for all tests and modules to access
    """
    driver = None
    screenshot_listener = None

    @staticmethod
    def get_driver():
        """
        Get the driver, creating if it does not exist
        :return: WebDriver object
        """
        if not WebDriverModule.driver:
            WebDriverModule.driver = WebDriverModule.create_driver()
            logging.info("Driver created")
            WebDriverModule.register_screenshot_listener()
        return WebDriverModule.driver

    @staticmethod
    def create_driver():
        """
        Create a WebDriver object
        :return: new WebDriver object
        """
        logging.info("Initialise WebDriver")
        return WebDriverModule.chrome_driver()

    @staticmethod
    def chrome_driver():
        """
        Create a basic chromedriver object
        :return: Chrome driver object
        """
        driver_path = TestRunConfig.TestRunConfig().get("driver_path")
        chrome_options = webdriver.ChromeOptions()
        return webdriver.Chrome(executable_path=driver_path,port=4444,chrome_options=chrome_options)

    @staticmethod
    def register_screenshot_listener():
        """
        Upgrade the driver to an event firing driver, with screenshot listener attached
        :return: EventFiringWebDriver
        """
        WebDriverModule.screenshot_listener = ScreenshotListener.ScreenshotListener()
        WebDriverModule.driver = EventFiringWebDriver(WebDriverModule.driver, WebDriverModule.screenshot_listener)

    @staticmethod
    def reload_driver():
        """
        Clear cookies and reload, for a 'fresh' web page
        :return:
        """
        logging.info("Reloading WebDriver")
        logging.debug("Cookies: %s" % WebDriverModule.driver.get_cookies())
        WebDriverModule.driver.delete_all_cookies()
        WebDriverModule.driver.refresh()
        logging.debug("Cookies/2: %s" % WebDriverModule.driver.get_cookies())

    @staticmethod
    def inject_screenshot(name):
        """
        Notify the screenshot listener to take a screenshot with given name
        :param name: identifier for this screenshot
        :return: None
        """
        WebDriverModule.screenshot_listener.custom_screenshot(WebDriverModule.driver, name)

    @staticmethod
    def inject_annotated_screenshot(details):
        """
        Experimental. Take a screenshot with sections to highlight
        :param details: Dict of
          {'name': name, element: {'location': {'x': x, 'y': y}, 'size': {'width': w, 'height': h}}}
        :return: None
        """
        WebDriverModule.screenshot_listener.annotated_screenshot(WebDriverModule.driver, details)