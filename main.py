import os
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from round_1a_parser import extract_outline_and_text
from query_config import QUERY_KEYWORDS, BOOST_WORDS, PENALTY_WORDS, DOCUMENT_PREFERENCES, QUERY_TEMPLATES, SCORING_WEIGHTS

# Configuration
PDF_DIR = "./input"
INPUT_JSON_PATH = "input/challenge_input.json"
TOP_K = 5  # Keep at top 5 as requested

# Global cache for model and embeddings
_model_cache = None
_embedding_cache = {}

def load_input_data():
    """Loads and validates the input JSON data."""
    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        input_data = json.load(f)
    persona = input_data.get("persona", {}).get("role", "Unknown Persona")
    job = input_data.get("job_to_be_done", {}).get("task", "Unknown Task")
    filenames = [doc["filename"] for doc in input_data.get("documents", [])]
    return input_data, persona, job, filenames

def build_intelligent_query(persona, job):
    """Builds an intelligent query based on persona and job requirements using config."""
    job_lower = job.lower()
    
    # Build context-aware query using config templates
    query_parts = []
    
    # Add relevant query templates based on job content
    for template_name, template_content in QUERY_TEMPLATES.items():
        # Check if template keywords are relevant to the job
        template_lower = template_content.lower()
        if any(keyword in job_lower for keyword in template_lower.split()):
            query_parts.append(template_content)
    
    # If no templates match, use a generic approach
    if not query_parts:
        # Extract key terms from job description
        job_words = job_lower.split()
        # Add relevant keywords from config
        for category, keywords in QUERY_KEYWORDS.items():
            if any(keyword in job_lower for keyword in keywords):
                query_parts.extend(keywords[:3])  # Limit to top 3 keywords per category
    
    return " ".join(query_parts)

def should_include_section(section_title, text, job):
    """Intelligent filtering based on job requirements using config."""
    job_lower = job.lower()
    title_lower = section_title.lower()
    text_lower = text.lower()
    
    # Check exclusion rules from config
    for category, config in PENALTY_WORDS.items():
        if config["action"] == "exclude":
            if any(keyword in text_lower for keyword in config["keywords"]):
                return False
    
    # Check if section is relevant to any configured keywords
    relevant_keywords = []
    for category, keywords in QUERY_KEYWORDS.items():
        relevant_keywords.extend(keywords)
    
    # If section doesn't match any relevant keywords, exclude it
    if not any(keyword in title_lower or keyword in text_lower for keyword in relevant_keywords):
        return False
    
    return True

def calculate_relevance_score(section_title, text, query, job, document_name):
    """Calculate a more sophisticated relevance score using config."""
    title_lower = section_title.lower()
    text_lower = text.lower()
    job_lower = job.lower()
    
    score = 0.0
    
    # Document preference score
    for doc_pattern, preference_score in DOCUMENT_PREFERENCES.items():
        if doc_pattern.lower() in document_name.lower():
            score += preference_score * SCORING_WEIGHTS["document_preference"]
            break
    
    # Boost word scoring
    for category, config in BOOST_WORDS.items():
        if any(keyword in text_lower for keyword in config["keywords"]):
            score += config["score"] * SCORING_WEIGHTS["keyword_boost"]
    
    # Penalty word scoring
    for category, config in PENALTY_WORDS.items():
        if config["action"] == "penalty":
            if any(keyword in text_lower for keyword in config["keywords"]):
                score += config["score"] * SCORING_WEIGHTS["penalty"]
    
    return score

def clean_text(text):
    """Cleans and normalizes text content."""
    if not text:
        return ""
    
    # Remove Unicode bullet points and other special characters
    text = re.sub(r'[\uf0b7\u2022\u2023\u25e6\u2043\u2219]', '', text)
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove numbered lists
    text = re.sub(r'\d+\.\s*', '', text)
    
    # Clean up any remaining bullet-like formatting
    text = re.sub(r'•\s*', '', text)  # Remove any remaining bullet points
    text = re.sub(r'-\s*', '', text)  # Remove dash bullets
    text = re.sub(r'\*\s*', '', text)  # Remove asterisk bullets
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_for_json(text):
    """Cleans text to be JSON serializable."""
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove or replace problematic characters
    text = text.replace('\u0000', '')  # Remove null bytes
    text = text.replace('\u2028', ' ')  # Replace line separator
    text = text.replace('\u2029', ' ')  # Replace paragraph separator
    
    # Remove other control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Clean up the text
    text = clean_text(text)
    
    # Limit length to prevent memory issues
    if len(text) > 2000:
        text = text[:2000] + "..."
    
    return text

def convert_to_json_serializable(obj):
    """Convert numpy types and other non-serializable objects to JSON-compatible types."""
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
    """Get or create the sentence transformer model with caching."""
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer('all-MiniLM-L12-v2')
    return _model_cache

def process_sections_intelligently(all_sections, query, job):
    """Processes sections using intelligent filtering and scoring with config."""
    model = get_model()
    
    # Filter sections based on job requirements
    filtered_sections = []
    for section in all_sections:
        if should_include_section(section['section_title'], section['text'], job):
            filtered_sections.append(section)
    
    if not filtered_sections:
        print("Warning: No sections passed the intelligent filter. Using all sections.")
        filtered_sections = all_sections
    
    # Create section texts for embedding
    section_texts = [f"{s['section_title']} {s['text']}" for s in filtered_sections]
    
    # Batch encode all section texts at once
    section_embeddings = model.encode(section_texts, convert_to_tensor=False, show_progress_bar=False)
    query_embedding = model.encode([query], convert_to_tensor=False, show_progress_bar=False)[0]
    
    # Calculate semantic similarity scores
    semantic_scores = cosine_similarity([query_embedding], section_embeddings)[0]
    
    # Combine semantic scores with intelligent scoring
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
    
    # Sort by combined score and get top K
    top_sections = sorted(combined_scores, key=lambda x: -x[1])[:TOP_K]
    
    return top_sections

def main():
    """Main execution function."""
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
    # Removed verbose query output - query is still used internally and saved to output
    
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
        refined_text = clean_for_json(sec["text"])[:1000]  # Increased length for better context
        
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
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert all values to JSON serializable types
    output = convert_to_json_serializable(output)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        print(f"Output written to {output_path}")
        print(f"Found {len(top_sections)} relevant sections")
        print("Configuration can be modified in query_config.py")
    except Exception as e:
        print(f"Error writing output: {e}")
        # Try to write a simplified version
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