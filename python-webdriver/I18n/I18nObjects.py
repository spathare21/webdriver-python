import polib
import logging
import difflib
import html2text
from TestHarness import WebDriverModule
import selenium.common
from TestConfig import TestRunConfig
# TODO import shelve for dictionary storage


class I18nObjects:
    """
    Experimental.
    Provide a mechanism for accessing LINK_TEXT or validation strings for non-English pages
    """

    # Pot mode
    pot_translation = {}
    string_cache = {}

    translations = {'HomePage': {'Login': {'en_US': 'Login', 'es_ES': 'Iniciar sesión'}},
                    'SignInPage': {'Unable to log in. Verify your login information or contact the system administrator.':
                                       {'es_ES': 'No logró iniciar sesión. Verifique la información de inicio de sesión o contacte al administrador del sistema.'}}}

    @staticmethod
    def translation_for(page_name, text, language):
        if language == 'en_US':
            return text
        po_string = I18nObjects.get_from_pot_file(text)
        if po_string != '':
            return po_string
        if page_name not in I18nObjects.translations:
            raise Exception('Page not recognised')
        if text not in I18nObjects.translations.get(page_name):
            raise Exception('Text not recognised')
        logging.info('Using fallback for %s', text)
        return I18nObjects.translations.get(page_name).get(text).get(language)

    @staticmethod
    def get_from_pot_file(text):
        # Exact match first
        locale = TestRunConfig.TestRunConfig().get('i18n_locale')
        po = polib.pofile('/tmp/' + locale + '.po')
        for entry in po:
            logging.info("msgid: %s;; str: %s", entry.msgid, text)
            if I18nObjects.sanitise_msgid(entry.msgid) == text:
                return entry.msgstr
        # Try a fuzzy match now
        for entry in po:
            logging.info("Fuzzy match msgid: %s;; str: %s", entry.msgid, text)
            s_entry = I18nObjects.sanitise_msgid(entry.msgid)
            s = difflib.SequenceMatcher(None, text, s_entry)
            if s.ratio() >= 0.8:
                return entry.msgstr
        return ''

    @staticmethod
    def check_for_possible_page_match(text):
        if len(I18nObjects.string_cache) > 0:
            local_cache = I18nObjects.string_cache
        else:
            driver = WebDriverModule.WebDriverModule().get_driver()
            local_cache = I18nObjects.get_all_texts(driver)
        for page_string in local_cache:
            s = difflib.SequenceMatcher(None, page_string, text)
            if s.ratio() >= 0.9:
                return page_string
        return ''

    @staticmethod
    def get_all_texts(driver):
        all_elements = driver.find_elements_by_xpath(".//*")
        bad_tags = ['html', 'head', 'script', 'meta']
        all_strings = {}
        for element in all_elements:
            if not element or str(element.tag_name) in bad_tags:
                logging.debug("Ignoring bad element %s", str(element.tag_name))
                continue
            if element.text.strip() == "":
                logging.debug("Text is empty %s", str(element.tag_name))
                continue
            logging.debug("Proceeding to analyse %s", str(element.tag_name))
            text = I18nObjects.get_top_level_text(driver, element)
            if (text is None):
                logging.debug("Text is empty %s", str(element.tag_name))
                continue
            # Check if the top level key exists
            logging.debug('Considering %s', text.keys())
            if len(text.keys()) > 0 and list(text.keys())[0] not in all_strings.keys():
                all_strings.update(text)
                logging.debug('Added %s', text)
        I18nObjects.string_cache = all_strings
        logging.debug(all_strings)
        return all_strings

    @staticmethod
    def get_top_level_text(driver, element):
        """
        Extract the text from an element, ignoring its children
        :param driver: WebDriver
        :param element: to be analysed
        :return: Extracted text string, or empty if none available
        """
        text = {}
        if not element or element.text.strip() == '':
            return text
        #logging.debug("Full text: %s", element.text)
        #logging.info("Location of %s : %s, %s", element.text, element.location, element.size)
        try:
            el_text = driver.execute_script(
                "var parentpart = window.jQuery(arguments[0]);"
                "if (parentpart === 'undefined') { return ''; }"
                "var cloned = parentpart.clone();"
                "if (cloned.children() != 'undefined' && cloned.children().length > 0) {"
                "  cloned = cloned.children().remove().end();"
                "}"
                "if (cloned.text() === 'undefined'){ return ''; }"
                "return cloned.text();",
                element)
            el_text = el_text.replace('\n', ' ').strip()
            if el_text != '':
                text = {el_text: {'location': element.location, 'size': element.size}}
        except selenium.common.exceptions.WebDriverException as e:
            if not element:
                logging.debug('None element')
            else:
                logging.info('Hit a bad element ' + str(element))
        return text

    @staticmethod
    def sanitise_msgid(text):
        """
        Return the message id as text, without html and surrounding spaces
        :return: sanitised string
        """
        htm = html2text.HTML2Text()
        htm.ignore_links = True
        htm.ignore_emphasis = True
        return htm.handle(text).strip()

    @staticmethod
    def clear_cache():
        I18nObjects.string_cache = []