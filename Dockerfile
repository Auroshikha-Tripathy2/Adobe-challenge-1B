# Use a slim Python base image for smaller size and faster builds
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies only if needed (uncomment if required)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     poppler-utils \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for input, output, and models
RUN mkdir -p /app/input /app/output /app/nlp_models

# Download the correct NLP model for offline use
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2').save_pretrained('/app/nlp_models/sentence_transformer_model')"

# Copy the rest of your application code
COPY . /app

# .dockerignore recommendations (create this file in your project root):
# __pycache__/
# .git/
# input/
# output/
# *.pdf
# *.md

# Command to run your main script
CMD ["python", "process_docs.py"]