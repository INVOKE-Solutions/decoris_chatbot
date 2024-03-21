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

## File Tree
```
├── README.md
├── main.py                     
├── components.py       
├── pages               
│   ├── feedback.py
│   └── login.py
├── data.py             
├── model.py           
├── model_prefix.py   
├── rename_map.py     
├── requirements.txt
└── tests             
    └── backend_test.py
```
### Files Details
1. `main.py` - top script for Streamlit app
2. `components.py` - Streamlit components (side bar, title, etc)
3. `pages/feedback.py` - Feedback page Streamlit app
4. `pages/login.py` - Login page for Streamlit app
5. `data.py` - Fetching dataset from AWS, cleaning dataset
6. `model.py` - `PandasAgent` class module
7. `model_prefix.py` - Prefix for `PandasAgent`
8. `rename_map.py` - renaming dictionary for data cleaning
9. `tests/backend_test.py` - unit testing for `data.py` and `model.py`

# Testing
## Run all tests
```
# linux
$ python -m pytest tests

# windows
$ python -m pytest /tests
```