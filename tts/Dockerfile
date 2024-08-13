FROM python:3.12
WORKDIR /tts_app
COPY . /tts_app/
RUN pip install -r requirements.txt
CMD ["python", "server.py"]