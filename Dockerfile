# Use a slim Python base image compatible with AMD64
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for input, output, and models
RUN mkdir -p /app/input /app/output /app/nlp_models

# --- Download NLP Models (CRUCIAL for offline operation) ---
# Ensure these commands download the models to /app/nlp_models
# Example for sentence-transformers:
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save_pretrained('/app/nlp_models/sentence_transformer_model')"
# Example for spaCy:
# RUN python -m spacy download en_core_web_sm --target /app/nlp_models/spacy_model
# If spacy download doesn't work directly to target, download it, then copy it.
# e.g., RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz --target /app/nlp_models/spacy_model


# Copy the rest of your application code
COPY . /app

# Command to run your main script
# The script will automatically look for PDFs in /app/input and write to /app/output
CMD ["python", "process_docs.py"]