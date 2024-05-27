FROM python:3.12-alpine

WORKDIR /soplaya

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./soplaya .
RUN python -c 'import secrets; print(f"SECRET_KEY = \"{secrets.token_hex()}\"")' > config.env

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]