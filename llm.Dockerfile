FROM ollama/ollama

# Copy model and Modelfile
COPY Modelfile ./
COPY mistral-7b-instruct-v0.2.Q4_K_M.gguf ./

# Start Ollama server (without creating the model yet)
CMD ["ollama", "serve"]
