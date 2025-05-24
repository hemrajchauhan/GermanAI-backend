# app/config.py

import os

LANGUAGETOOL_API = os.getenv("LANGUAGETOOL_API", "http://languagetool:8010/v2/check")
TRANSLATE_API = os.getenv("TRANSLATE_API", "http://libretranslate:5000/translate")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8082")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "GermanAI")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "vokabelmeister-app")
# KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
