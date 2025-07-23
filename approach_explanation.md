# Approach Explanation: Persona-Driven Document Intelligence

## Overview
This solution is designed to act as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done. The system is generic and robust, capable of handling diverse document domains, personas, and tasks, as required by the challenge brief.

## Methodology
1. **Input Handling**: The system accepts a collection of 3–10 PDF documents, a persona definition (role, expertise, focus), and a job-to-be-done (concrete task). These are provided via a structured JSON file, ensuring flexibility and ease of integration.

2. **Text Extraction**: Each PDF is parsed to extract its outline and text content. The text is chunked into manageable segments to facilitate efficient embedding and relevance scoring.

3. **Semantic Embedding**: Both the persona/job description and document chunks are converted into dense vector representations using a pre-trained sentence embedding model (`all-MiniLM-L12-v2`). This model is chosen for its balance of speed, accuracy, and compact size (<1GB), making it suitable for CPU-only, offline execution.

4. **Relevance Scoring**: The system computes the cosine similarity between the persona/job embedding and each document chunk embedding. This allows for semantic matching, ensuring that the most contextually relevant sections are identified, regardless of superficial keyword overlap.

5. **Section Ranking and Extraction**: Document sections are ranked based on their maximum relevance scores. The top sections are extracted, and for each, the most relevant sub-section (chunk) is further refined and summarized.

6. **Output Generation**: The results are compiled into a structured JSON output, including metadata (input docs, persona, job, timestamp), extracted sections (document, page, section title, importance rank), and sub-section analysis (document, refined text, page number). The output format strictly follows the provided `challenge1b_output.json` template.

## Model Choice
The `all-MiniLM-L12-v2` model from the Sentence Transformers library is used for semantic embedding. It offers:
- High accuracy for semantic similarity tasks
- Fast inference on CPU
- Small model size (~85MB), well within the 1GB limit
- No internet required at runtime (model is pre-downloaded in the Docker image)

## Compliance with Challenge Requirements
- **CPU-only**: All processing is done on CPU; no GPU is required.
- **Model size**: The model is <1GB.
- **Processing time**: The pipeline is optimized for speed and completes within 60 seconds for 3–5 documents (assuming reasonable document length).
- **Offline execution**: The Docker image is built with all dependencies and the model included, so no internet is required at runtime.
- **Generic solution**: The system is domain-agnostic and can handle a wide variety of documents, personas, and tasks.

## Execution
- The solution is packaged with a Dockerfile and clear instructions for both Docker and offline use.
- A template for the input JSON is provided, and the output strictly matches the required format.

This approach ensures a robust, efficient, and user-friendly solution to the Persona-Driven Document Intelligence challenge. 