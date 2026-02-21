FROM python:3.9-slim
EXPOSE 5000
WORKDIR /app
COPY . /app
RUN pip install flask
RUN pip install flask-smorest
RUN pip install python-dotenv
CMD [ "flask", "run", "--host=0.0.0.0" ]