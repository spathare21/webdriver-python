import io
import logging
import os

from I18n import I18nObjects
from I18n import I18nWhitelist
from TestConfig import TestRunConfig
from TestHarness import WebDriverModule


class I18nAuditor:
    """
      Various tests for translations, through character recognition and
      record/playback of strings
      Requires JQuery on the page. An attempt to insert it will occur if not detected.
    """

    audit_mode = TestRunConfig.TestRunConfig().get("i18n_audit")
    ready = False

    @staticmethod
    def ready_state(is_ready):
        """
        Do not start recording or verifying until the test is ready
        :param is_ready: test is ready True/False
        :return: None
        """
        I18nAuditor.ready = is_ready

    @staticmethod
    def is_rendered_correctly(by, driver):
        """
        Checks for the standard browser placeholder characters
        :param by: locator for the element
        :param driver: WebDriver object
        :return: is a placeholder character in the element text
        """
        rendered = True
        character = str.encode('U+FFFD')
        if driver.findElement(by).get_text().contains(character):
            rendered = False
        return rendered

    @staticmethod
    def is_in_english(by, driver):
        """
        Magic function to guess if the string is in english (TODO)
        :param by: locator of element
        :param driver: WebDriver object
        :return: is string likely in english
        """
        pass

    @staticmethod
    def perform(driver, name):
        """
        Redirector for the I18n function
        :param driver: WebDriver
        :param name: Page name
        :return: None
        """
        if not I18nAuditor.ready:
            logging.warning('I18n Auditor not ready!')
            return
        if I18nAuditor.audit_mode == "off":
            logging.info("I18n audit mode off")
            return
        if I18nAuditor.audit_mode == "record":
            I18nAuditor.record_all(driver, name)
        elif I18nAuditor.audit_mode == "compare":
            I18nAuditor.compare_all(driver, name)

    @staticmethod
    def record_all(driver, name):
        """
        Record the text elements of a page to file for later comparison.
        Requires JQuery. If not detected on the page, it will be inserted.
        :param driver: WebDriver
        :param name: page name, file name to store data
        :return: None
        """
        logging.info('Recording all elements on %s', name)
        texts = I18nAuditor.playback_all(name)
        if not I18nAuditor.inject_jquery(driver):
            logging.warning("Failed to detect JQuery on page %s", name)
        found_new = False
        for text in I18nObjects.I18nObjects().get_all_texts(driver):
            if I18nAuditor.is_good_chunk(text, texts):
                found_new = True
                texts.append(text)
                logging.debug('Added: ' + text)
        if found_new:
            with io.open(I18nAuditor.get_file_name(name), 'w+') as file:
                # file.write('{ texts: ')
                for wrt_string in texts:
                    if '\n' in wrt_string:
                        logging.warning("Rogue newline")
                        wrt_string = wrt_string.replace('\n', '')
                    if wrt_string == '':
                        logging.warning("Empty string")
                        continue
                    logging.debug('Writing to file %s', wrt_string)
                    file.write(wrt_string+'\n')
                file.close()

    @staticmethod
    def playback_all(name):
        """
        If the page has been previously recorded, return the strings
        :param name: of the page class
        :return: strings that have been seen previously
        """
        logging.info('Read dictionary for %s', name)
        texts = []
        output = I18nAuditor.get_file_name(name)
        if os.path.isfile(output):
            with io.open(output, 'r') as infile:
                texts = infile.read().splitlines()
        else:
            logging.info("Unable to open %s", output)
        logging.debug("Found: %s", texts)
        return texts

    @staticmethod
    def compare_all(driver, name):
        """
        Compare all texts (best effort) on current page to that stored on file.
        Log a warning for every instance that appears to be untranslated.
        :param driver: WebDriver
        :param name: Page name
        :return: None
        """
        logging.info('Comparing all elements on %s', name)
        base_texts = I18nAuditor.playback_all(name)
        if len(base_texts) == 0:
            logging.warning("Error: no such file %s", name)
            pass
        if not I18nAuditor.inject_jquery(driver):
            logging.warning("Failed to detect JQuery on page %s", name)
            pass
        # Use a dictionary here!
        page_items = I18nObjects.I18nObjects().get_all_texts(driver)
        logging.info(page_items)
        for text in page_items:
            if text in base_texts and not I18nWhitelist.WhiteList().is_in(name, text):
                logging.warning("I18N:%s:%s seems unchanged", name, text)
                entity = page_items.get(text)
                logging.info('What: %s', entity)
                x = entity.get('location').get('x')
                y = entity.get('location').get('y')
                width = entity.get('size').get('width')
                height = entity.get('size').get('height')
                logging.info('Request draw at: %s %s %s %s' % (x, y, width, height))
                WebDriverModule.WebDriverModule().inject_annotated_screenshot(
                    {'name': 'i18n_' + name,
                     'element': {'x': x, 'y': y, 'width': width, 'height': height}})

    @staticmethod
    def inject_jquery(driver):
        """
        Inject a minified JQuery if the page does not include one
        :param driver: WebDriver
        :return: JQuery exists
        """
        existing_jquery = driver.execute_script("return !!window.jQuery;")
        if not existing_jquery:
            logging.debug("JQuery insertion required")
            with open(os.path.dirname(__file__) + '/jquery-3.2.1.min.js', 'r') as jquery_js:
                jquery = jquery_js.read() #read the jquery from a file
                driver.execute_script(jquery) #active the jquery lib
        existing_jquery = driver.execute_script("return !!window.jQuery;")
        return existing_jquery

    @staticmethod
    def is_good_chunk(chunk, chunks):
        logging.debug('Found "%s" chunk', chunk)
        if not chunk:
            logging.debug('%s is not chunk', chunk)
        if chunk == '':
            logging.debug('Chunk is empty')
        if chunk in chunks:
            logging.debug('%s already seen', chunk)
        return chunk and chunk != '' and chunk != '\n' and (chunk not in chunks)

    @staticmethod
    def get_file_name(name):
        output_entity = str(TestRunConfig.TestRunConfig().get("i18n_audit_dir")) + name + '.i18n'
        logging.info("File: %s", output_entity)
        return output_entity

    @staticmethod
    def get_element_identifier(element):
        if element.id != '':
            return element.id
        elif element.name != '':
            return element.name
        elif element.class_name != '':
            return element.class_name
        else:
            return element.tag_name