import logging
import os
import time
from PIL import Image
from PIL import ImageDraw
import io
from selenium.webdriver.support.events import AbstractEventListener

from TestConfig import TestRunConfig


class ScreenshotListener(AbstractEventListener):

    def __init__(self):
        self.basename = TestRunConfig.TestRunConfig().get("screenshot_dir")
        assert(not os.path.isfile(self.basename))
        if not str(self.basename).endswith("/"):
            self.basename += "/"
        if not os.path.isdir(self.basename):
            os.makedirs(self.basename)

    def on_exception(self, exception, driver):
        logging.info("Exception: " + exception.msg)
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
        time.sleep(0.25)
        name = self.basename + str(time.time()) + name + '.png'
        driver.get_screenshot_as_file(name)
        logging.info("Screenshot saved as '%s'" % name)

    @staticmethod
    def custom_screenshot(driver, name):
        instance = ScreenshotListener()
        ScreenshotListener.take_screenshot(instance, driver, name)

    @staticmethod
    def annotated_screenshot(driver, details):
        instance = ScreenshotListener()
        data = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(data))
        draw = ImageDraw.Draw(image)
        x = details.get('element').get('x')
        y = details.get('element').get('y')
        width = details.get('element').get('width')
        height = details.get('element').get('height')
        logging.info('Drawing rectangle: %s %s %s %s' % (x, y, width, height))
        draw.rectangle(((y, x), (height, width)), outline='yellow')
        filename = instance.basename + str(time.time()) + details.get('name') + '.png'
        image.save(filename)
        logging.info("Annotated screenshot saved as '%s'" % filename)