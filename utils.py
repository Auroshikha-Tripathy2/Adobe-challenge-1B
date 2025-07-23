import json
import os

def load_json(file_path):
    """Loads a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    """Saves data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_input_files(input_dir, extension=".pdf"):
    """Returns a list of PDF files in the input directory."""
    return [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(extension)]

def get_output_path(input_pdf_path, output_dir):
    """Generates the output JSON path for a given input PDF."""
    base_name = os.path.basename(input_pdf_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    return os.path.join(output_dir, f"{file_name_without_ext}.json")

def chunk_text(text, max_length=256, overlap=50):
    """
    Splits text into smaller chunks.
    This is a basic chunking; more advanced methods might use sentence boundaries.
    """
    if not text:
        return []
    chunks = []
    current_pos = 0
    while current_pos < len(text):
        end_pos = min(current_pos + max_length, len(text))
        chunk = text[current_pos:end_pos]
        chunks.append(chunk)
        current_pos += (max_length - overlap) # Move by (chunk size - overlap)
        if current_pos >= len(text) - overlap and end_pos == len(text):
            break # Avoid infinite loop on very small texts
    return chunks