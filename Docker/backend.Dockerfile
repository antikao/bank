FROM python:3.11.6-bullseye
WORKDIR /bank
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "gunicorn", "--bind" , "0.0.0.0:3000", "app:create_app()"]
