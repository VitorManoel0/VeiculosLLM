#!/bin/bash

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
while ! nc -z ollama 11434; do
  sleep 1
done
echo "Ollama is ready!"

# Run the application
python main.py