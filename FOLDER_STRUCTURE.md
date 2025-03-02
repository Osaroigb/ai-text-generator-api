ai-text-generator-api/
│
├── app/
│   │
│   ├── __init__.py
│   │
│   ├── config.py
│   │
│   ├── database.py
│   │
│   ├── routes.py
│   │
│   │
│   ├── controllers/
│   │   │
│   │   ├── auth_controller.py
│   │   │
│   │   └── text_generation_controller.py
│   │
│   │
│   ├── models/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── user.py
│   │   │
│   │   └── generated_text.py
│   │ 
│   │
│   ├── schemas/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── auth_schema.py
│   │   │
│   │   └── text_schema.py
│   │
│   │   
│   ├── services/
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── auth_service.py
│   │   │
│   │   ├── generated_text_service.py
│   │   │
│   │   └── openai_service.py 
│   │
│   │
│   └── utils/
│       │
│       ├── __init__.py
│       │
│       ├── api_responses.py
│       │
│       ├── constants.py
│       │
│       ├── errors.py
│       │
│       └── jwt_handler.py
│
│   
├── tests/
│   ├── __init__.py
│   │
│   ├── test_auth.py
│   │
│   ├── test_generated_text.py
│   │
│   └── conftest.py
│
│
├── venv/
│
├── .dockerignore
│
├── .env
│
├── .env.example
│
├── .gitignore
│
├── docker-compose.yml
│
├── Dockerfile
│
├── FOLDER_STRUCTURE.md
│
├── LICENSE
│
├── README.md
│
├── requirements.txt
│
└── run.py