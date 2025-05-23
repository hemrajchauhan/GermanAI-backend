# app/config.py

import os

LANGUAGETOOL_API = os.getenv("LANGUAGETOOL_API", "http://languagetool:8010/v2/check")
TRANSLATE_API = os.getenv("TRANSLATE_API", "http://libretranslate:5000/translate")
