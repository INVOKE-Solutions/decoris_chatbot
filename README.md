# Getting Started

- Decoris chatbot (GPT 3.5-Turbo) with Langchain dataframe connector.
- Dataframe is fetched from Facebook Campaign and Ads.

# Development
## Secret Key
- Please ask the developer the following information before start the app development.

1. `Streamlit` - Create `/.streamlit/secrets.toml` file on your local machine and provide the following key and value
```toml
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
OPENAI_API_KEY=""

BUCKET_NAME=""
OBJECT_NAME_1=""
OBJECT_NAME_2=""

USERNAME=""
PASSWORD=""

[connections.gsheets]
spreadsheet = ""
```
2. API Development - Create `.env` file on your local machine and provide
the following key and value
```toml
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
OPENAI_API_KEY=""

BUCKET_NAME=""
OBJECT_NAME_1=""
OBJECT_NAME_2=""
```

## Run Streamlit Locally
```
$ python -m streamlit run main.py
```
## Run API Locally
```
$ uvicorn main:app --reload
```

# Testing
## Run all tests
```
# linux
$ python -m pytest tests

# windows
$ python -m pytest /tests
```