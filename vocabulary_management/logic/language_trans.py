from translate import Translator

# 封装好的翻译模块
"""
    输入参数：
        “E2C”:英译中
        "C2E":中译英
"""


class LanguageTrans:
    def __init__(self, mode):
        self.mode = mode
        if self.mode == "E2C":
            self.translator = Translator(from_lang="english", to_lang="chinese")
        if self.mode == "C2E":
            self.translator = Translator(from_lang="chinese", to_lang="english")

    def trans(self, word):
        translation = self.translator.translate(word)
        return translation
