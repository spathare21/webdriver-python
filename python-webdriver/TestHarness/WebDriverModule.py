import logging
import os

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver

from TestHarness import ScreenshotListener


class WebDriverModule:
    driver = None

    @staticmethod
    def get_driver():
        if not WebDriverModule.driver:
            WebDriverModule.driver = WebDriverModule.create_webdriver()
            logging.warning("Driver created")
        return WebDriverModule.driver

    @staticmethod
    def create_webdriver():
        logging.info("Initialise WebDriver")
        driverpath = "chromedriver"
        if "CHROMEDRIVER" in os.environ:
            driverpath = os.environ.get("CHROMEDRIVER")
        chromeOptions = webdriver.ChromeOptions()
        basedriver = webdriver.Chrome(executable_path=driverpath,port=4444,chrome_options=chromeOptions)
        return EventFiringWebDriver(basedriver, ScreenshotListener.ScreenshotListener())

    @staticmethod
    def reload_webdriver():
        logging.info("Reloading WebDriver")
        logging.info("Cookies: %s" % WebDriverModule.driver.get_cookies())
        WebDriverModule.driver.delete_all_cookies()
        WebDriverModule.driver.refresh()
        logging.info("Cookies/2: %s" % WebDriverModule.driver.get_cookies())

