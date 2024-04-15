FROM python:3.8
WORKDIR /

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV MAIL_USERNAME='test@test.com'
ENV MAIL_PASSWORD='test_password'
ENV MAIL_FROM='test@test.com'
ENV MAIL_PORT=587
ENV MAIL_SERVER=smtp.gmail.com
ENV MAIL_FROM_NAME='FastApi Test'
ENV MAIL_TLS=True

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
