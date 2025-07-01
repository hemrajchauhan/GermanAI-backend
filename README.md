# GermanAI-backend

**GermanAI-backend** is a modern, AI-powered backend for German language learning.
It provides grammar checking, smart translation, verb conjugation, example sentences, and quiz generation via a clean REST API—**all powered by open source AI models** and robust microservices.

---

## Features

- **Grammar Checking:** Uses [LanguageTool](https://languagetool.org/) for comprehensive German grammar, spelling, and style suggestions.
- **LLM-Powered Translation:** All translations are handled by your self-hosted LLM (Ollama + Llama 3). No external API costs or data sharing.
- **AI Example Sentences:** On-demand, AI-generated sentences for any word, tailored for learners.
- **Smart Verb Conjugation:** Get all forms of any German verb for any person/tense, using a simple API and enums for clarity.
- **Multiple Choice Quiz Generation:** Get four English options (one correct, three distractors) for any German word—great for learning and flashcards!
- **API-First Design:** All endpoints have strict typing, enums, and auto-validated requests—works beautifully with Swagger UI and frontend codegen.
- **Secure Authentication (optional):** Supports Keycloak + JWT for secure APIs and future user features.
- **Easy Deployment:** One command with Docker Compose spins up the whole stack (API, LLM, grammar, translation, auth).
- **Extensible:** Easily add new endpoints or swap in your own LLM.

---

## Quick Start

1. **Clone the repository**

    ```bash
    git clone git@github.com:hemrajchauhan/GermanAI-backend.git
    cd GermanAI-backend
    ```
2. **Create a .env file**

   Create a file named `.env` in the project root (next to `docker-compose.yml`).  
   Fill in your Keycloak and other variables as shown below (replace with your own values):

    ```bash
    # .env (example values, replace with your own for production!)
    KEYCLOAK_URL_INTERNAL=http://keycloak:8080
    KEYCLOAK_URL_PUBLIC=http://localhost:8082
    KEYCLOAK_REALM=GermanAI
    KEYCLOAK_CLIENT_ID=germanai-backend
    KEYCLOAK_CLIENT_SECRET=supersecretkeycloakclientsecret
    
    KEYCLOAK_ADMIN=admin
    KEYCLOAK_ADMIN_PASSWORD=adminpassword123
    
    # Ollama LLM endpoint (internal Docker address)
    OLLAMA_URL=http://ollama:11434/api/generate
    
    # LanguageTool API (internal Docker address)
    LANGUAGETOOL_API=http://languagetool:8010/v2/check
    
    # LibreTranslate API (internal Docker address)
    TRANSLATE_API=http://libretranslate:5000/translate
    
    # CORS
    ALLOWED_ORIGINS=http://localhost:8080
    ```

4. **Build and run with Docker Compose**

    ```bash
    docker compose up --build
    ```
    
5. **Pull the Llama 3 model for Ollama (first time only)**

    ```bash
    docker exec -it ollama ollama pull llama3
    ```
       
6. **Access the API documentation**

    Visit [http://localhost:8080/docs](http://localhost:8080/docs) in your browser to see interactive Swagger UI for all endpoints.

## API Endpoints
### POST `/check-grammar`
Checks the grammar of German sentences using LanguageTool.
- **Request Body:** JSON
  ```json
  { "text": "Ich habe ein Hund." }

- **Response:**
JSON object containing grammar issues and suggestions.

### GET `/example-sentence`
AI-generated German sentence for a given word.
- **Request Body:** String
  ```str
  GET /example-sentence?word=Hausaufgaben
  
- **Response:** JSON
  ```json
  {
      "word": "Hausaufgaben",
      "sentence": "Hier ist ein Beispiel:\n\n\"Meine Tochter muss jeden Abend ihre Hausaufgaben erledigen, bevor sie sich ins Bett legen kann.\"\n\n(Das bedeutet: Meine Tochter muss jeden Abend ihre Homeworks erledigen, bevor sie sich ins Bett legen kann.)"
  }

### GET `/verb-form`
Get any German verb form for a given person and tense.
- **Request Body:** String
  ```str
  GET /verb-form?verb=laufen&form=perfekt&person=er%2Fsie%2Fes
  
- **Response:** JSON
  ```json
  {
      "verb": "laufen",
      "form": "perfekt",
      "person": "er/sie/es",
      "result": "Das Verb \"laufen\" im Perfekt wird wie folgt konjugiert:\n\n* Er: ist gelaufen\n* Sie: ist gelaufen\n* Es: ist gelaufen"
  }

### GET `/mcq-meaning`
Multiple-choice quiz for any German word.
- **Request Body:** String
  ```str
  GET /mcq-meaning?word=verlieren
  
- **Response:** JSON
  ```json
  {
      "word": "verlieren",
      "options": [
        "lose",
        "understand",
        "delay",
        "win"
      ],
      "answer": 0
  }
  ```
  **Note:** `"answer"` is a zero-based index (first option is 0).

### GET `/translate-word`
Get all possible English meanings of a German word.

- **Request Body:** String
  ```str
  GET /translate-word?word=entsprechen

- **Response:** JSON
  ```json
  {
      "word": "entsprechen",
      "meanings": [
        "correspond",
        "match",
        "suit",
        "fit",
        "agree",
        "coincide",
        "comply",
        "meet",
        "answer to",
        "be equivalent to"
      ]
  }

### POST `/translate-sentence`
Translate a German sentence to English (with a word limit for resource control).
- **Request Body:** JSON
  ```json
  { "sentence": "Ich gehe jeden Tag zur Schule." }

- **Response:** JSON
  ```json
  {
      "sentence": "Ich gehe jeden Tag zur Schule.",
      "translation": "I go to school every day."
  }

## Technology Stack
- **FastAPI** — Modern, high-performance Python web API framework.
- **Ollama** — Self-hosted open-source LLM (Large Language Model) server (e.g., Llama 3 and more) for AI-powered sentence generation and quizzes.
- **LanguageTool** — Self-hosted open-source grammar, spelling, and style checker.
- **Keycloak** — Self-hosted identity and access management (IAM) platform for authentication and JWT-based API security (optional).
- **Docker Compose** — Multi-container orchestration; makes it easy to run and manage all services locally or in production.
- **Pydantic** — Python data validation and settings management, including powerful type-safe enums for request/response models.

## Extending
- **Tune LLM prompts:** See app/services/llm_service.py to change AI behavior or add more features.
- **Plug in your own models:** Swap in any Ollama-supported LLMs as desired.

## License
This project is licensed under the Apache License 2.0.
See [LICENSE](https://github.com/hemrajchauhan/GermanAI-backend/blob/main/LICENSE) for details.

## Contributing
Pull requests and issues are welcome!
Open an issue to get started.

## Author
Hemraj Chauhan

## Acknowledgements
- [LanguageTool](https://languagetool.org/)
- [Ollama](https://ollama.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Keycloak](https://www.keycloak.org/)
- The open-source community!

## Happy coding and viel Erfolg beim Deutschlernen! 🇩🇪

