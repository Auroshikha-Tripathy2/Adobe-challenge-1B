import fitz  # PyMuPDF
import json
import re
from collections import Counter
import io

try:
    from flask import Flask, request, jsonify
except ImportError:
    raise ImportError("Flask is not installed. Please install it with 'pip install flask'.")

app = Flask(__name__)

def get_font_statistics(doc):
    font_counts = Counter()
    size_counts = Counter()

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for l in b["lines"]:
                    for s in l["spans"]:
                        font_counts[s['font']] += 1
                        size_counts[round(s['size'])] += 1

    body_size = size_counts.most_common(1)[0][0] if size_counts else 12
    potential_heading_sizes = sorted([size for size in size_counts if size > body_size], reverse=True)

    heading_levels = {}
    if len(potential_heading_sizes) > 0:
        heading_levels[potential_heading_sizes[0]] = "H1"
    if len(potential_heading_sizes) > 1:
        heading_levels[potential_heading_sizes[1]] = "H2"
    if len(potential_heading_sizes) > 2:
        heading_levels[potential_heading_sizes[2]] = "H3"
        
    return body_size, heading_levels

def is_bold(font_name):
    return any(x in font_name.lower() for x in ['bold', 'black', 'heavy'])

def extract_outline_from_stream(pdf_stream):
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    if doc.page_count == 0:
        return {"title": "", "outline": []}

    body_size, heading_levels = get_font_statistics(doc)
    
    outline = []
    potential_title = ""
    max_title_size = 0
    current_heading = {"text": "", "level": None, "page": 0}

    def commit_current_heading():
        if current_heading["text"]:
            clean_text = re.sub(r'^\d+(\.\d+)*\s*', '', current_heading["text"]).strip()
            outline.append({
                "level": current_heading["level"],
                "text": clean_text,
                "page": current_heading["page"]
            })
            current_heading["text"] = ""
            current_heading["level"] = None

    for page_num, page in enumerate(doc, 0):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for l in b["lines"]:
                    if len(l['spans']) == 0 or len(l['spans'][0]['text'].strip()) < 3:
                        continue
                    
                    span = l['spans'][0]
                    text = span['text'].strip()
                    size = round(span['size'])
                    font = span['font']

                    if page_num <= 1 and size > max_title_size:
                        max_title_size = size
                        potential_title = text

                    level = heading_levels.get(size)
                    
                    if level and (is_bold(font) or size > body_size + 2):
                        commit_current_heading()
                        current_heading["text"] = text
                        current_heading["level"] = level
                        current_heading["page"] = page_num
                    elif level and current_heading["level"] == level:
                        current_heading["text"] += " " + text
                    else:
                        commit_current_heading()

    commit_current_heading()

    return {
        "title": potential_title,
        "outline": outline
    }

@app.route('/extract-outline', methods=['POST'])
def handle_extract_outline():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "No selected file or file is not a PDF"}), 400
    
    try:
        pdf_stream = io.BytesIO(file.read())
        result = extract_outline_from_stream(pdf_stream)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred during processing: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)