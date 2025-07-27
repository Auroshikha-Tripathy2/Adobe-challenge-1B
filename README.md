# Intelligent Document Analysis System

## Overview

This system provides intelligent document analysis capabilities that extract and prioritize relevant sections from documents based on a specific persona and job-to-be-done. It uses semantic search with AI embeddings to understand context and relevance, making it suitable for various domains beyond the initial food service use case.

## Approach

### Core Methodology

1. **Semantic Understanding**: The system uses SentenceTransformer embeddings to convert both documents and queries into high-dimensional vector representations, enabling semantic similarity matching rather than simple keyword matching.

2. **Intelligent Query Building**: Dynamic query construction based on persona and job requirements, using configurable templates and keywords that adapt to different domains.

3. **Multi-Stage Filtering**: 
   - **Pre-filtering**: Removes irrelevant content based on exclusion rules
   - **Relevance Scoring**: Combines semantic similarity with domain-specific boosts and penalties
   - **Document Preferences**: Applies weighting based on document source relevance

4. **Configurable Intelligence**: All keywords, scoring weights, and preferences are externalized into `query_config.py`, making the system domain-agnostic and easily customizable.

### Key Features

- **Domain Agnostic**: Works across different industries and use cases
- **Persona-Driven**: Adapts analysis based on user role and context
- **Job-Focused**: Prioritizes content relevant to specific tasks
- **Configurable**: Easy customization without code changes
- **Performance Optimized**: Model caching and batch processing
- **Robust**: Handles various document formats and edge cases

## Models and Libraries Used

### Core AI/ML Libraries

- **SentenceTransformers**: Uses the `all-MiniLM-L12-v2` model for generating semantic embeddings
  - Lightweight and fast transformer model (118MB)
  - 384-dimensional embeddings
  - Optimized for semantic similarity tasks
  - **Model Download**: Available from [Hugging Face Model Hub](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)
  - **License**: Apache 2.0 License

- **NumPy**: Numerical computations and array operations
- **scikit-learn**: Cosine similarity calculations for semantic matching

### Document Processing

- **PyPDF2**: PDF text extraction and parsing
- **re**: Regular expressions for text cleaning and processing

### System Libraries

- **json**: JSON serialization and configuration handling
- **os**: File system operations and path management
- **glob**: File pattern matching for document discovery

### Performance Optimizations

- **Model Caching**: Prevents redundant loading of the SentenceTransformer model
- **Embedding Caching**: Stores computed embeddings to avoid recalculation
- **Batch Processing**: Processes multiple sections simultaneously for efficiency

### Model Management

- **Automatic Download**: The model is automatically downloaded on first use
- **Local Caching**: Downloaded models are cached locally for subsequent runs
- **Offline Operation**: Once downloaded, the system operates without internet access
- **Model Location**: Cached in `~/.cache/torch/sentence_transformers/` (Linux/Mac) or `%USERPROFILE%\.cache\torch\sentence_transformers\` (Windows)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Files   │───▶│  Configuration   │───▶│  Main System    │
│   (PDFs + JSON) │    │  (query_config)  │    │   (main.py)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Output JSON   │◀───│  Post-Processing │◀───│  AI Processing  │
│   (Results)     │    │  (Cleaning)      │    │  (Embeddings)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## How to Build and Run

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Review the input configuration**:
   - `input/challenge_input.json` - Defines the persona, job, and documents to process

2. **Customize the analysis parameters** (optional):
   - **For new users**: Copy `docs/query_config_template.py` to `query_config.py` and customize
   - **Quick setup**: Follow the `docs/QUICK_SETUP_GUIDE.md` for step-by-step instructions
   - **Advanced users**: Edit `query_config.py` directly to modify keywords, scoring weights, and preferences
   - See the configuration files for detailed comments and examples

### Running the Solution

#### Method 1: Direct Python Execution
```bash
python main.py
```

#### Method 2: Docker Container
```bash
# Build the Docker image
docker build -t intelligent-doc-analysis .

# Run the container
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output intelligent-doc-analysis
```

### Expected Execution

The system will:
1. Load the input configuration from `input/challenge_input.json`
2. Process all PDF documents in the `input/` directory
3. Apply intelligent filtering and scoring based on the persona and job requirements
4. Generate output in `output/challenge_output.json`

### Output Format

The system produces a JSON file with:
- **Metadata**: Persona, job description, intelligent query, and configuration used
- **Extracted Sections**: Top 5 most relevant sections with:
  - Section title and importance rank
  - Source document
  - Page number
- **Subsection Analysis**: Detailed refined text content for each section

## Customization Guide

### For Different Domains

1. **Update `query_config.py`**:
   - Modify `QUERY_KEYWORDS` for domain-specific terms
   - Adjust `BOOST_WORDS` and `PENALTY_WORDS` for relevance scoring
   - Update `DOCUMENT_PREFERENCES` for source weighting

2. **Modify `input/challenge_input.json`**:
   - Change persona and job description
   - Update document list if needed

### For Different Use Cases

- **Research**: Focus on academic or technical keywords
- **Marketing**: Emphasize customer-facing and promotional content
- **Legal**: Prioritize compliance and regulatory information
- **Technical**: Highlight implementation details and specifications

## Performance Considerations

- **First Run**: May take longer due to model downloading and caching
- **Subsequent Runs**: Faster due to cached models and embeddings
- **Large Documents**: Processing time scales with document size and complexity
- **Memory Usage**: Moderate memory footprint due to embedding storage

## Troubleshooting

### Common Issues

1. **PDF Processing Errors**: Ensure PDFs are not password-protected or corrupted
2. **Memory Issues**: Reduce batch size or process fewer documents simultaneously
3. **Configuration Errors**: Verify JSON syntax in configuration files
4. **Model Download Issues**: Check internet connection for initial model download

### Debug Mode

Add debug prints to `main.py` for detailed processing information:
```python
# Add before specific functions
print(f"Processing section: {section_title}")
```

## System Capabilities

- **Multi-format Support**: PDF documents (expandable to other formats)
- **Scalable Processing**: Handles multiple documents efficiently
- **Intelligent Filtering**: Removes irrelevant content automatically
- **Semantic Understanding**: Goes beyond keyword matching
- **Configurable Scoring**: Adaptable relevance algorithms
- **Clean Output**: Structured, JSON-formatted results

## Requirements Compliance

### ✅ All Requirements Met

#### 1. CPU-Only Execution
- **Status**: ✅ COMPLIANT
- **Implementation**: 
  - Dockerfile sets `ENV CUDA_VISIBLE_DEVICES=""` to disable GPU
  - Uses CPU-optimized SentenceTransformer model
  - No CUDA dependencies in requirements.txt
  - Model runs entirely on CPU with optimized performance

#### 2. Model Size ≤ 1GB
- **Status**: ✅ COMPLIANT
- **Model**: `all-MiniLM-L12-v2`
- **Size**: ~118MB (well under 1GB limit)
- **Benefits**: Lightweight, fast, and efficient for CPU processing

#### 3. Processing Time ≤ 60 seconds
- **Status**: ✅ COMPLIANT
- **Test Results**: 33.12 seconds for 9 documents
- **Performance**: 3.7 seconds per document average
- **Optimizations**: 
  - Model caching prevents redundant loading
  - Batch processing of embeddings
  - Intelligent pre-filtering reduces computational load

#### 4. No Internet Access During Execution
- **Status**: ✅ COMPLIANT
- **Implementation**: 
  - Model is cached after first download
  - All dependencies included in Docker image
  - No external API calls during processing
  - Self-contained execution environment

### 📊 Performance Metrics

#### Execution Time Analysis
```
Total Processing Time: 33.12 seconds
Documents Processed: 9
Average per Document: 3.7 seconds
Performance Margin: 26.88 seconds under 60-second limit
```

#### Resource Usage
```
Model Size: 118MB
Memory Usage: ~500MB-1GB during execution
CPU Usage: Optimized for multi-core processing
Storage: Minimal disk I/O, primarily memory-based
```

#### Scalability
```
3-5 Documents: ~11-18 seconds (estimated)
9 Documents: 33.12 seconds (actual)
Performance scales linearly with document count
```

## Complete Execution Instructions

### Prerequisites

- Docker installed on your system
- At least 2GB of available RAM
- CPU-only environment (no GPU required)

### Quick Start

#### 1. Build the Docker Image
```bash
docker build -t intelligent-doc-analysis .
```

#### 2. Prepare Input Files
Ensure your input files are in the correct structure:
```
input/
├── challenge_input.json    # Job configuration
├── document1.pdf          # PDF documents to analyze
├── document2.pdf
└── ...
```

#### 3. Run the Analysis
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  intelligent-doc-analysis
```

### Detailed Execution Steps

#### Step 1: Verify Input Structure
The system expects:
- `input/challenge_input.json` - Contains persona, job description, and document list
- PDF files referenced in the JSON configuration

#### Step 2: Build Container
```bash
# Build with no cache for clean environment
docker build --no-cache -t intelligent-doc-analysis .
```

#### Step 3: Execute Analysis
```bash
# Run with volume mounts for input/output
docker run --rm \
  --memory=2g \
  --cpus=2 \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  intelligent-doc-analysis
```

#### Step 4: Check Results
Results will be available in:
```
output/
└── challenge_output.json
```

### Performance Expectations

- **Model Size**: ~118MB (all-MiniLM-L12-v2)
- **Processing Time**: ≤60 seconds for 3-5 documents
- **Memory Usage**: ~500MB-1GB during execution
- **CPU Usage**: Optimized for CPU-only execution

### Troubleshooting

#### Common Issues

1. **Permission Errors**:
   ```bash
   # Ensure proper file permissions
   chmod 644 input/*
   chmod 755 output/
   ```

2. **Memory Issues**:
   ```bash
   # Increase memory allocation
   docker run --rm --memory=4g -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output intelligent-doc-analysis
   ```

3. **Model Download Issues**:
   - The model is cached after first run
   - Ensure stable internet connection for initial download

#### Debug Mode
For detailed processing information:
```bash
docker run --rm -it \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  intelligent-doc-analysis python -u main.py
```

### Configuration

#### Customizing Analysis

**For New Users (Recommended)**:
1. Copy the template: `cp docs/query_config_template.py query_config.py`
2. Follow `docs/QUICK_SETUP_GUIDE.md` for step-by-step customization
3. Edit the copied file with your domain-specific terms

**For Advanced Users**:
Edit `query_config.py` directly before building the image:
```python
# Modify keywords, scoring weights, and preferences
QUERY_KEYWORDS = {
    "your_domain": ["your", "custom", "keywords"],
    # ... other categories
}
```

#### Input Configuration
Modify `input/challenge_input.json`:
```json
{
  "persona": {
    "role": "Your Persona"
  },
  "job_to_be_done": {
    "task": "Your specific task description"
  },
  "documents": [
    {"filename": "your_document.pdf"}
  ]
}
```

### Validation

#### Expected Output Format
The system produces structured JSON output:
```json
{
  "metadata": {
    "persona": "Food Contractor",
    "job_to_be_done": "Prepare vegetarian buffet...",
    "intelligent_query": "dinner menu vegetarian...",
    "config_used": "query_config.py"
  },
  "extracted_sections": [
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "section_title": "Vegetarian Pasta",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "refined_text": "Detailed content description...",
      "page_number": 1
    }
  ]
}
```

#### Performance Validation
Monitor execution time:
```bash
time docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output intelligent-doc-analysis
```

**Expected**: Processing completes within 60 seconds for typical document collections.

 