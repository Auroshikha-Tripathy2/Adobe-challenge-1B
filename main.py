import os
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from round_1a_parser import extract_outline_and_text
from query_config import QUERY_KEYWORDS, BOOST_WORDS, PENALTY_WORDS, DOCUMENT_PREFERENCES, QUERY_TEMPLATES, SCORING_WEIGHTS

PDF_DIR = "./input"
INPUT_JSON_PATH = "input/challenge_input.json"
TOP_K = 5

_model_cache = None
_embedding_cache = {}

def load_input_data():
    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        input_data = json.load(f)
    persona = input_data.get("persona", {}).get("role", "Unknown Persona")
    job = input_data.get("job_to_be_done", {}).get("task", "Unknown Task")
    filenames = [doc["filename"] for doc in input_data.get("documents", [])]
    return input_data, persona, job, filenames

def build_intelligent_query(persona, job):
    job_lower = job.lower()
    
    query_parts = []
    
    for template_name, template_content in QUERY_TEMPLATES.items():
        template_lower = template_content.lower()
        if any(keyword in job_lower for keyword in template_lower.split()):
            query_parts.append(template_content)
    
    if not query_parts:
        job_words = job_lower.split()
        for category, keywords in QUERY_KEYWORDS.items():
            if any(keyword in job_lower for keyword in keywords):
                query_parts.extend(keywords[:3])
    
    return " ".join(query_parts)

def should_include_section(section_title, text, job):
    job_lower = job.lower()
    title_lower = section_title.lower()
    text_lower = text.lower()
    
    for category, config in PENALTY_WORDS.items():
        if config["action"] == "exclude":
            if any(keyword in text_lower for keyword in config["keywords"]):
                return False
    
    relevant_keywords = []
    for category, keywords in QUERY_KEYWORDS.items():
        relevant_keywords.extend(keywords)
    
    if not any(keyword in title_lower or keyword in text_lower for keyword in relevant_keywords):
        return False
    
    return True

def calculate_relevance_score(section_title, text, query, job, document_name):
    title_lower = section_title.lower()
    text_lower = text.lower()
    job_lower = job.lower()
    
    score = 0.0
    
    for doc_pattern, preference_score in DOCUMENT_PREFERENCES.items():
        if doc_pattern.lower() in document_name.lower():
            score += preference_score * SCORING_WEIGHTS["document_preference"]
            break
    
    for category, config in BOOST_WORDS.items():
        if any(keyword in text_lower for keyword in config["keywords"]):
            score += config["score"] * SCORING_WEIGHTS["keyword_boost"]
    
    for category, config in PENALTY_WORDS.items():
        if config["action"] == "penalty":
            if any(keyword in text_lower for keyword in config["keywords"]):
                score += config["score"] * SCORING_WEIGHTS["penalty"]
    
    return score

def clean_text(text):
    if not text:
        return ""
    
    text = re.sub(r'[\uf0b7\u2022\u2023\u25e6\u2043\u2219]', '', text)
    
    text = ' '.join(text.split())
    
    text = re.sub(r'\d+\.\s*', '', text)
    
    text = re.sub(r'•\s*', '', text)
    text = re.sub(r'-\s*', '', text)
    text = re.sub(r'\*\s*', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_for_json(text):
    if not text:
        return ""
    
    text = str(text)
    
    text = text.replace('\u0000', '')
    text = text.replace('\u2028', ' ')
    text = text.replace('\u2029', ' ')
    
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    text = clean_text(text)
    
    if len(text) > 2000:
        text = text[:2000] + "..."
    
    return text

def convert_to_json_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    else:
        return obj

def get_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer('all-MiniLM-L12-v2')
    return _model_cache

def process_sections_intelligently(all_sections, query, job):
    model = get_model()
    
    filtered_sections = []
    for section in all_sections:
        if should_include_section(section['section_title'], section['text'], job):
            filtered_sections.append(section)
    
    if not filtered_sections:
        print("Warning: No sections passed the intelligent filter. Using all sections.")
        filtered_sections = all_sections
    
    section_texts = [f"{s['section_title']} {s['text']}" for s in filtered_sections]
    
    section_embeddings = model.encode(section_texts, convert_to_tensor=False, show_progress_bar=False)
    query_embedding = model.encode([query], convert_to_tensor=False, show_progress_bar=False)[0]
    
    semantic_scores = cosine_similarity([query_embedding], section_embeddings)[0]
    
    combined_scores = []
    for i, section in enumerate(filtered_sections):
        semantic_score = float(semantic_scores[i]) * SCORING_WEIGHTS["semantic_similarity"]
        intelligent_score = calculate_relevance_score(
            section['section_title'], 
            section['text'], 
            query, 
            job,
            section['document']
        )
        combined_score = semantic_score + intelligent_score
        combined_scores.append((section, combined_score))
    
    top_sections = sorted(combined_scores, key=lambda x: -x[1])[:TOP_K]
    
    return top_sections

def main():
    print("Starting intelligent document analysis...")
    
    input_data, persona, job, filenames = load_input_data()
    
    print(f"Persona: {persona}")
    print(f"Job: {job}")
    print(f"Documents: {len(filenames)}")
    
    all_sections = []
    for file in filenames:
        pdf_path = os.path.join(PDF_DIR, file)
        if os.path.exists(pdf_path):
            print(f"Processing: {file}")
            try:
                doc_analysis = extract_outline_and_text(pdf_path)
                for section in doc_analysis['outline']:
                    all_sections.append({
                        "document": os.path.basename(pdf_path),
                        "section_title": clean_for_json(section.get("text", "")),
                        "text": clean_for_json(section.get("content_text", "")),
                        "page_number": section.get("page", 1),
                    })
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue
    
    query = build_intelligent_query(persona, job)
    
    top_sections = process_sections_intelligently(all_sections, query, job)
    
    output = {
        "metadata": {
            "input_documents": filenames,
            "persona": persona,
            "job_to_be_done": job,
            "intelligent_query": query,
            "config_used": "query_config.py"
        },
        "extracted_sections": [],
        "subsection_analysis": [],
    }

    for rank, (sec, score) in enumerate(top_sections, start=1):
        refined_text = clean_for_json(sec["text"])[:1000]
        
        output["extracted_sections"].append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page_number"],
        })
        output["subsection_analysis"].append({
            "document": sec["document"],
            "refined_text": refined_text,
            "page_number": sec["page_number"],
        })

    output_path = "output/challenge_output.json"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    output = convert_to_json_serializable(output)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        print(f"Output written to {output_path}")
        print(f"Found {len(top_sections)} relevant sections")
        print("Configuration can be modified in query_config.py")
    except Exception as e:
        print(f"Error writing output: {e}")
        try:
            simplified_output = {
                "metadata": output["metadata"],
                "extracted_sections": output["extracted_sections"],
                "subsection_analysis": [{"document": item["document"], "page_number": item["page_number"]} for item in output["subsection_analysis"]]
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(simplified_output, f, indent=4, ensure_ascii=False)
            print(f"Simplified output written to {output_path}")
        except Exception as e2:
            print(f"Failed to write even simplified output: {e2}")

if __name__ == "__main__":
    main()