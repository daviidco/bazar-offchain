FROM python:3.8.6
RUN apt-get update && apt-get install -y nginx
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x start.sh
EXPOSE 5000
CMD ["/app/start.sh"]
