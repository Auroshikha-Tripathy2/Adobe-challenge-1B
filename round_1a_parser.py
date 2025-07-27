import fitz  # PyMuPDF
import json
import re
from collections import Counter

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

def extract_outline_and_text(pdf_path):
    """
    Extracts structured outline (Title, H1, H2, H3 with page numbers)
    and associated text content from a PDF using PyMuPDF (fitz).
    Returns a dict with 'title' and 'outline' (list of sections).
    Each section: {'level', 'text', 'page', 'content_text'}
    """
    outline = []
    title = "Extracted Document Title"
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count == 0:
            return {"title": "", "outline": []}
        body_size, heading_levels = get_font_statistics(doc)
        potential_title = ""
        max_title_size = 0
        current_heading = {"text": "", "level": None, "page": 0, "content_text": ""}
        def commit_current_heading():
            if current_heading["text"]:
                clean_text = re.sub(r'^\d+(\.\d+)*\s*', '', current_heading["text"]).strip()
                outline.append({
                    "level": current_heading["level"],
                    "text": clean_text,
                    "page": current_heading["page"] + 1,  # 0-indexed to 1-indexed
                    "content_text": current_heading["content_text"]
                })
                current_heading["text"] = ""
                current_heading["level"] = None
                current_heading["content_text"] = ""
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
                            current_heading["content_text"] = page.get_text()
                        elif level and current_heading["level"] == level:
                            current_heading["text"] += " " + text
                        else:
                            commit_current_heading()
            # Commit any heading at the end of the page
            commit_current_heading()
        if not outline:
            # Fallback: treat each page as a section with first non-empty line
            for i, page in enumerate(doc):
                page_text = page.get_text()
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                first_line = lines[0] if lines else "Untitled Page"
                outline.append({
                    "level": "H1",
                    "text": first_line,
                    "page": i + 1,
                    "content_text": page_text
                })
        title = potential_title or title
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return {"title": "Unknown Title", "outline": []}
    return {"title": title, "outline": outline}

if __name__ == '__main__':
    sample_pdf_path = "sample.pdf" # Make sure you have a sample.pdf for testing
    try:
        with open("sample.pdf", "w") as f:
            f.write("This is a dummy PDF file content.\nSection 1.\nSubsection 1.1.\nPage 2 content.")
    except Exception:
        pass
    result = extract_outline_and_text("sample.pdf")
    print(json.dumps(result, indent=2)) 