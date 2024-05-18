FROM python:latest
COPY . .
RUN pip install python-telegram-bot==13.3 paramiko psycopg2 six urllib3==1.26.15
CMD ["python", "bot.py"]
