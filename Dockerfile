FROM ubuntu:22
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y python3.9.12
RUN curl -fsSL https://ollama.com/install.sh
RUN pip install -r requirements.txt
RUN sudo systemctl daemon-reload
RUN sudo systemctl enable ollama
ENV OLLAMA_MODELS=/app/models
EXPOSE 3000