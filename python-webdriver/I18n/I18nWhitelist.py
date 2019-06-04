

class WhiteList:

    whitelist = {'_global': ['[]', 'PDF', 'Deutsch - Deutschland', 'U.S. English',
                             'español - España', 'français - France', 'italiano - Italia',
                             '日本語 - 日本', '한국어 - 대한민국', 'português do Brasil',
                             '中文（简体） - 中国'],
                 'SignInPage': ['internal']}

    @staticmethod
    def is_in(name, text):
        if text in WhiteList.whitelist.get('_global'):
            return True
        if name not in WhiteList.whitelist:
            return False
        return text in WhiteList.whitelist.get(name)
