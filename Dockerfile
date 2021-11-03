FROM python

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget

RUN pip install --upgrade pip
RUN pip install flask \
    Flask-Cors \
    pysqlite3 \
    beautifulsoup4

WORKDIR /app
COPY . .

EXPOSE 80

RUN python create_table.py

CMD ["python", "flask_app.py"]
