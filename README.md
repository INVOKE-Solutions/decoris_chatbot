# Getting Started

- Decoris chatbot (GPT 3.5-Turbo) with Langchain dataframe connector.
- Dataframe is fetched from Facebook Campaign and Ads.

# Development
## Secret Key
- Please ask the developer the following information before start the app development.

1. `Streamlit` - Create `/.streamlit/secrets.toml` file on your local machine and provide the following key and value
```toml
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
OPENAI_API_KEY=xxx

BUCKET_NAME=xxx
OBJECT_NAME_1=xx
OBJECT_NAME_2=xxx

USERNAME=xxx
PASSWORD=xxx

[connections.gsheets]
spreadsheet = xxx
```
2. API Development - Create `.env` file on your local machine and provide
the following key and value
```
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
OPENAI_API_KEY=xxx

BUCKET_NAME=xxx
OBJECT_NAME_1=xxx
OBJECT_NAME_2=xxx
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
$ python -m pytest tests
```