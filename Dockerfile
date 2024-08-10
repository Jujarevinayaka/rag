FROM ubuntu:24.04

# Copy project files and change the working directory
COPY . /app
WORKDIR /app

# Install basic requirements
RUN apt-get update && apt-get install -y \
    systemd \
    python3 \
    python3-pip \
    curl

# Install Ollama and set the ENV variables
RUN curl -fsSL https://ollama.com/install.sh | sh
ENV PATH=$PATH:/app/bin
ENV OLLAMA_MODELS=/app/models
ENV FLASK_APP=App
ENV FLASK_DEBUG=1

# Install the requirements to run the app
RUN pip3 install --break-system-packages -r requirements.txt

# Open port for connecting to the app
EXPOSE 5000

# Start ollama service and the app
CMD ./init_app.sh
