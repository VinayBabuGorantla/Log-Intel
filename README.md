# Log Intel Application

* Accepts log files (`.log`, `.txt`, `.json`, `.xml`, etc.) and ZIP folders of logs.
* Parses and indexes logs.
* Lets users ask questions (e.g., "What warnings are found?", "Why did the app crash?").
* Provides:

  * **Performance insights**
  * **Warning/Error detection + fixes**
  * **Proactive issue prediction**

---

### 📂 **Updated Folder Structure**

```
log-analyzer-llm/
│
├── src/
│   ├── config/                  # Logging & settings
│   ├── exception/               # Custom error handling
│   ├── ingestion/               # File ingestion & extraction (.log/.zip etc.)
│   ├── indexing/                # Vector DB creation (via LangChain)
│   ├── qa/                      # LLM Q&A logic
│   ├── analysis/                # Log analysis logic (regex-based/error patterns)
│   └── utils/                   # File validation/utilities
│
├── templates/                  # Web pages (Flask or FastAPI + Jinja2)
│   ├── index.html
│   └── home.html
│
├── logs/                       # Application logs
│
├── app.py                      # Entry point (Flask or FastAPI)
├── requirements.txt
├── setup.py
├── .env
└── README.md
