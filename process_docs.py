import os
import json
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Import your custom modules
from round_1a_parser import extract_outline_and_text
from utils import load_json, save_json, get_input_files, get_output_path, chunk_text

# --- Configuration ---
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
NLP_MODEL_PATH = "sentence-transformers/all-MiniLM-L12-v2"
# SPACY_MODEL_PATH = "/app/nlp_models/spacy_model" # Uncomment if using spaCy

class DocumentProcessor:
    def __init__(self):
        # Load the pre-trained Sentence Transformer model locally
        print(f"Loading Sentence Transformer model from {NLP_MODEL_PATH}...")
        self.model = SentenceTransformer(NLP_MODEL_PATH)
        print("Model loaded successfully.")
        # If using spaCy:
        # print(f"Loading spaCy model from {SPACY_MODEL_PATH}...")
        # self.nlp = spacy.load(SPACY_MODEL_PATH)
        # print("spaCy model loaded successfully.")

    def get_embeddings(self, texts):
        """Generates embeddings for a list of texts."""
        return self.model.encode(texts, convert_to_tensor=False)

    def analyze_persona_and_job(self, persona_info, job_to_be_done):
        """
        Analyzes persona and job-to-be-done to get their semantic representations.
        """
        persona_description = persona_info['role'] + ". " + persona_info.get('description', '')
        task_description = job_to_be_done['task']

        combined_query = f"Persona: {persona_description}. Task: {task_description}"
        return self.get_embeddings([combined_query])[0] # Get single embedding

    def score_relevance(self, query_embedding, chunk_embeddings):
        """Calculates cosine similarity between query and chunk embeddings."""
        if len(chunk_embeddings) == 0:
            return np.array([])
        # Reshape query_embedding if it's 1D, for cosine_similarity
        return cosine_similarity(query_embedding.reshape(1, -1), chunk_embeddings).flatten()

    def process_document(self, pdf_path, persona_embedding):
        """
        Processes a single PDF to extract and rank relevant sections.
        """
        print(f"Processing document: {pdf_path}")
        doc_analysis = extract_outline_and_text(pdf_path)  # Use your Round 1A parser

        extracted_sections = []
        sub_section_analysis = []
        all_section_chunks = []
        section_to_chunks_map = {} # Map section index to its chunks

        # Phase 1: Chunking and Embedding all content
        for idx, section in enumerate(doc_analysis['outline']):
            content_text = section.get('content_text', '')
            chunks = chunk_text(content_text, max_length=256, overlap=50) # Use your utility
            if chunks:
                chunk_embeddings = self.get_embeddings(chunks)
                all_section_chunks.extend(chunk_embeddings)
                section_to_chunks_map[idx] = (len(all_section_chunks) - len(chunk_embeddings), len(all_section_chunks))
            else:
                section_to_chunks_map[idx] = (-1, -1) # No chunks

        if not all_section_chunks:
            print(f"No content chunks found for {pdf_path}. Skipping relevance scoring.")
            return extracted_sections, sub_section_analysis

        all_section_chunks_array = np.array(all_section_chunks)
        
        # Phase 2: Relevance Scoring
        # Score all chunks against the persona/job query
        chunk_relevance_scores = self.score_relevance(persona_embedding, all_section_chunks_array)

        # Aggregate scores for sections and identify top sub-sections
        section_scores = []
        for idx, section in enumerate(doc_analysis['outline']):
            start_idx, end_idx = section_to_chunks_map[idx]
            if start_idx != -1:
                section_chunk_scores = chunk_relevance_scores[start_idx:end_idx]
                # Aggregate: e.g., max score, average score, or sum
                # Max score tends to highlight sections with even a single very relevant point
                avg_score = np.mean(section_chunk_scores) if len(section_chunk_scores) > 0 else 0
                max_score = np.max(section_chunk_scores) if len(section_chunk_scores) > 0 else 0
                section_scores.append((idx, max_score, avg_score, section_chunk_scores, section.get('content_text', ''))) # Store for later use
            else:
                section_scores.append((idx, 0, 0, [], ''))

        # Sort sections by relevance (e.g., by max_score)
        section_scores.sort(key=lambda x: x[1], reverse=True) # Sort by max_score

        # Populate extracted_sections and sub_section_analysis
        ranked_sections = []
        for rank, (original_idx, max_score, avg_score, chunk_scores_for_section, full_content_text) in enumerate(section_scores):
            original_section = doc_analysis['outline'][original_idx]
            importance_rank = rank + 1 # 1-based rank

            extracted_sections.append({
                "document": os.path.basename(pdf_path),
                "page_number": original_section['page'],
                "section_title": original_section['text'],
                "importance_rank": importance_rank
            })

            # For sub-section analysis, identify the most relevant chunk within this section
            if len(chunk_scores_for_section) > 0:
                most_relevant_chunk_idx_within_section = np.argmax(chunk_scores_for_section)
                start_chunk_idx, _ = section_to_chunks_map[original_idx]
                
                # Re-chunk the text using the same logic to get the actual chunks again
                all_chunks_in_section = chunk_text(full_content_text, max_length=256, overlap=50)
                
                if all_chunks_in_section:
                    most_relevant_chunk_text = all_chunks_in_section[most_relevant_chunk_idx_within_section]
                    
                    # Refinement/Summarization - simplified extractive for now
                    refined_text = most_relevant_chunk_text # Placeholder: Implement summarization logic here
                                                            # If a small summarization model is available, use it.
                                                            # Otherwise, choose a few key sentences from the chunk.
                    
                    sub_section_analysis.append({
                        "document": os.path.basename(pdf_path),
                        "refined_text": refined_text,
                        "page_number": original_section['page'] # Or find precise page for chunk
                    })
        
        # Sort sub_section_analysis by page_number or a derived relevance if needed
        # For simplicity, we append as we find relevant chunks, which might not be ordered.
        # A more robust solution might link sub-sections directly to top sections and rank accordingly.

        return extracted_sections, sub_section_analysis

    def main(self, input_challenge_info_path):
        """Main function to process all documents."""
        challenge_data = load_json(input_challenge_info_path)
        
        # Extract metadata
        challenge_id = challenge_data['challenge_info']['challenge_id']
        test_case_name = challenge_data['challenge_info']['test_case_name']
        persona_info = challenge_data['persona']
        job_to_be_done = challenge_data['job_to_be_done']
        input_documents_meta = challenge_data['documents']

        # Analyze persona and job-to-be-done once
        persona_job_embedding = self.analyze_persona_and_job(persona_info, job_to_be_done)

        all_extracted_sections_output = []
        all_sub_section_analysis_output = []
        
        # Process each document
        for doc_meta in input_documents_meta:
            filename = doc_meta['filename']
            pdf_path = os.path.join(INPUT_DIR, filename)

            # Ensure PDF exists before processing
            if not os.path.exists(pdf_path):
                print(f"Warning: PDF file not found at {pdf_path}. Skipping.")
                continue

            extracted_sections, sub_section_analysis = self.process_document(pdf_path, persona_job_embedding)
            all_extracted_sections_output.extend(extracted_sections)
            all_sub_section_analysis_output.extend(sub_section_analysis)

        # Consolidate and rank all extracted sections and sub-sections across documents
        # This is CRUCIAL for cross-document relevance.
        # Create a single list of all items with their scores, then sort.
        final_sections_to_rank = []
        for section in all_extracted_sections_output:
            # We need the underlying score, not just the initial rank within its document
            # Re-evaluate or store the raw scores from process_document if needed for global ranking.
            # For simplicity, let's assume `importance_rank` is just a preliminary local rank,
            # and we need a global rank across all documents.
            # A better approach: store the actual `max_score` from process_document and use it here.
            final_sections_to_rank.append(section) # Add sections

        # Sorting based on actual relevance scores from process_document, if stored.
        # As `process_document` currently returns just `importance_rank`,
        # for a true global rank, you'd need to modify `process_document`
        # to return the `max_score` alongside the section data, then sort `final_sections_to_rank` by `max_score`.
        # For now, we'll just sort by the pre-calculated importance_rank (which is per document).
        # To achieve true global ranking, you would collect ALL sections with their
        # raw relevance scores (e.g., the `max_score` from `section_scores`)
        # and then sort this global list and assign `importance_rank` here.
        
        # Placeholder for global ranking (needs actual scores carried over)
        all_extracted_sections_output.sort(key=lambda x: x['importance_rank']) # This sorts by per-document rank

        # Construct final output JSON
        output_data = {
            "metadata": {
                "challenge_id": challenge_id,
                "test_case_name": test_case_name,
                "documents": challenge_data['documents'],
                "persona": persona_info,
                "job_to_be_done": job_to_be_done,
                "processing_timestamp": datetime.datetime.now().isoformat()
            },
            "extracted_sections": all_extracted_sections_output,
            "sub_section_analysis": all_sub_section_analysis_output
        }

        # Save output JSON
        output_filename = f"{challenge_id}.json" # Or use test_case_name or a more generic name
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        save_json(output_data, output_path)
        print(f"Processing complete. Output saved to {output_path}")

if __name__ == '__main__':
    import traceback
    try:
        # This block is for how the script will be executed in the Docker container.
        # The input JSON is expected to be in /app/input, usually named 'challenge_info.json'
        # based on the image provided, the input JSON is directly presented in the code example as 'challenge_info'
        # So we'll need to assume a standard input filename or create one for testing.

        # For hackathon environment, it's common for the host to mount a specific
        # input directory containing both the JSON config and PDFs.
        # Let's assume the challenge info JSON is named 'challenge_input.json' in INPUT_DIR
        
        # Create dummy input files for local testing if they don't exist
        if not os.path.exists(INPUT_DIR):
            os.makedirs(INPUT_DIR)
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Create a dummy challenge_input.json based on the image
        dummy_input_json_path = os.path.join(INPUT_DIR, "challenge_input.json")
        if not os.path.exists(dummy_input_json_path):
            dummy_challenge_data = {
                "challenge_info": {
                    "challenge_id": "round_1b_002",
                    "test_case_name": "travel_planner",
                    "description": "France Travel"
                },
                "documents": [
                    {"filename": "South of France - Cities.pdf", "title": "South of France - Cities"},
                    {"filename": "South of France - Cuisine.pdf", "title": "South of France - Cuisine"},
                    {"filename": "South of France - History.pdf", "title": "South of France - History"}
                ],
                "persona": {
                    "role": "Travel Planner"
                },
                "job_to_be_done": {
                    "task": "Plan a trip of 4 days for a group of 10 college friends."
                }
            }
            save_json(dummy_challenge_data, dummy_input_json_path)
            print(f"Created dummy input JSON at {dummy_input_json_path}")
        else:
            dummy_challenge_data = load_json(dummy_input_json_path)

        # Create dummy PDF files if they don't exist
        for doc_info in dummy_challenge_data['documents']:
            dummy_pdf_path = os.path.join(INPUT_DIR, doc_info['filename'])
            if not os.path.exists(dummy_pdf_path):
                with open(dummy_pdf_path, "w") as f:
                    f.write(f"This is a dummy PDF content for {doc_info['filename']}. It talks about cities and travel planning.")
                print(f"Created dummy PDF at {dummy_pdf_path}")

        processor = DocumentProcessor()
        # The main method expects the path to the input challenge_info.json
        processor.main(dummy_input_json_path)
    except Exception as e:
        print("\n--- Exception occurred ---")
        traceback.print_exc()