import os

# Global settings, environment read once here


# Declare this in .env file
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")
LANGUAGETOOL_API = os.getenv("LANGUAGETOOL_API")
#Hugging Face Settings
LLAMA_GGUF_PATH = os.getenv("LLAMA_GGUF_PATH", "/root/.cache/huggingface/hub/models--google--gemma-3-4b-it-qat-q4_0-gguf/blobs/76aed0a8285b83102f18b5d60e53c70d09eb4e9917a20ce8956bd546452b56e2")
# Transformers model (for HuggingFace pipeline)
TRANSFORMERS_MODEL_NAME = os.getenv("TRANSFORMERS_MODEL_NAME", "meta-llama/Llama-3.2-3B-Instruct")
TRANSFORMERS_MAX_LENGTH = int(os.getenv("TRANSFORMERS_MAX_LENGTH", 150))
# Llama context size and thread settings (adjust as needed for your hardware)
LLAMA_N_CTX = int(os.getenv("LLAMA_N_CTX", 2048))
LLAMA_N_THREADS = int(os.getenv("LLAMA_N_THREADS", 4))
# Ollama settings
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
#Keycloak settings
KEYCLOAK_URL_INTERNAL = os.getenv("KEYCLOAK_URL_INTERNAL")
KEYCLOAK_URL_PUBLIC = os.getenv("KEYCLOAK_URL_PUBLIC")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
# KEYCLOAK_ADMIN_CLIENT_SECRET = os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET")
# CALLBACK_URI = os.getenv("CALLBACK_URI") # where keycloak should be redirected
