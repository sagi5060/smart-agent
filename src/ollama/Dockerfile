FROM ollama/ollama:latest
ENV OLLAMA_MODELS_LIST="llama3.1:8b"

RUN apt-get update && apt-get install -y curl

# Start ollama serve in the background, pull the model, then stop ollama
RUN ollama serve & \
    PID=$! && \
    for i in $(seq 1 60); do \
      if curl -sf http://localhost:11434/api/tags >/dev/null; then break; fi; \
      sleep 1; \
    done && \
    for m in $OLLAMA_MODELS_LIST; do \
      echo "Pulling $m"; ollama pull "$m" || exit 1; \
    done && \
    kill $PID

ENTRYPOINT ["ollama", "serve"]