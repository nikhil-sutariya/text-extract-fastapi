# Simple text extraction from pdf, doc or docx file FastApi App

For simple todo apis with database checkout branch to todos-with-db

### Install all the requirements

```
pip install -r requirements.txt
```

### To start the app
```
cd app
uvicorn main:app --reload
```

### To start app with docker
```
docker build -t text-extraction-api .
docker run -d --name text_extraction_api_container -p 80:80 text-extraction-api
```