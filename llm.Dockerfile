FROM ollama/ollama

# Copia modelo e Modelfile
COPY Modelfile ./
COPY mistral-7b-instruct-v0.2.Q4_K_M.gguf ./

# Inicia o servidor Ollama (sem criar o modelo ainda)
CMD ["ollama", "serve"]
