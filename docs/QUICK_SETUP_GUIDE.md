# Quick Setup Guide - Query Configuration

## 🚀 Get Started in 3 Steps

### Step 1: Copy the Template
```bash
cp docs/query_config_template.py query_config.py
```

### Step 2: Customize for Your Domain
Edit `query_config.py` and modify the sections below:

#### A. Define Your Keywords
```python
QUERY_KEYWORDS = {
    # Replace with your domain-specific categories
    "your_domain": ["keyword1", "keyword2", "keyword3"],
    "technical": ["implementation", "architecture", "deployment"],
    "business": ["strategy", "marketing", "sales"],
    "general": ["content", "information", "data"]
}
```

#### B. Set Your Boost Words
```python
BOOST_WORDS = {
    "important_terms": {
        "keywords": ["critical", "essential", "key", "important"],
        "score": 1.5  # Higher score = more important
    }
}
```

#### C. Define Exclusions
```python
PENALTY_WORDS = {
    "irrelevant": {
        "keywords": ["unrelated", "off-topic"],
        "action": "exclude"  # Completely exclude
    },
    "low_priority": {
        "keywords": ["basic", "introductory"],
        "action": "penalty",
        "score": -1.0  # Reduce relevance
    }
}
```

### Step 3: Test and Refine
```bash
python main.py
```

## 📋 Common Customization Examples

### For Technical Documentation
```python
QUERY_KEYWORDS = {
    "implementation": ["code", "implementation", "deployment", "setup"],
    "architecture": ["design", "architecture", "system", "infrastructure"],
    "troubleshooting": ["error", "debug", "fix", "issue", "problem"],
    "api": ["endpoint", "api", "interface", "method", "function"]
}
```

### For Business Analysis
```python
QUERY_KEYWORDS = {
    "strategy": ["strategy", "planning", "roadmap", "vision"],
    "marketing": ["marketing", "campaign", "promotion", "brand"],
    "sales": ["sales", "revenue", "customer", "conversion"],
    "finance": ["budget", "cost", "ROI", "profit", "investment"]
}
```

### For Legal Documents
```python
QUERY_KEYWORDS = {
    "compliance": ["compliance", "regulation", "legal", "requirement"],
    "contract": ["contract", "agreement", "terms", "conditions"],
    "liability": ["liability", "risk", "responsibility", "obligation"],
    "intellectual_property": ["patent", "copyright", "trademark", "IP"]
}
```

## ⚙️ Scoring Weight Guidelines

### Conservative Approach (Less Aggressive)
```python
SCORING_WEIGHTS = {
    "semantic_similarity": 0.8,    # Rely more on AI understanding
    "keyword_boost": 0.5,          # Less emphasis on keywords
    "document_preference": 0.3,    # Minimal source preference
    "penalty": 0.8                 # Moderate penalties
}
```

### Aggressive Approach (More Specific)
```python
SCORING_WEIGHTS = {
    "semantic_similarity": 1.2,    # Balance AI and keywords
    "keyword_boost": 1.5,          # Strong keyword emphasis
    "document_preference": 0.8,    # Strong source preference
    "penalty": 1.5                 # Strong penalties
}
```

## 🔧 Troubleshooting

### Results Too Broad?
- Increase `keyword_boost` weight
- Add more specific keywords
- Use stronger penalties

### Results Too Narrow?
- Decrease `keyword_boost` weight
- Add more general keywords
- Reduce penalties

### Wrong Content Types?
- Adjust `DOCUMENT_PREFERENCES`
- Review `PENALTY_WORDS` exclusions
- Check `QUERY_KEYWORDS` categories

## 📝 Best Practices

1. **Start Simple**: Begin with basic keywords and add complexity gradually
2. **Test Incrementally**: Make small changes and test each one
3. **Use Examples**: Look at your actual documents to identify key terms
4. **Balance Weights**: Don't make any single factor too dominant
5. **Document Changes**: Keep notes of what works for future reference

## 🎯 Quick Reference

| Setting | Purpose | Example Values |
|---------|---------|----------------|
| `QUERY_KEYWORDS` | Define relevant categories | `["technical", "business", "user"]` |
| `BOOST_WORDS` | Increase relevance | `{"score": 1.5}` |
| `PENALTY_WORDS` | Decrease/exclude content | `{"action": "exclude"}` |
| `DOCUMENT_PREFERENCES` | Weight document sources | `{"Manual": 3.0, "Guide": 1.0}` |
| `SCORING_WEIGHTS` | Balance scoring factors | `{"semantic": 1.0, "keyword": 1.0}` |

## 🚀 Ready to Start?

1. Copy the template: `cp docs/query_config_template.py query_config.py`
2. Edit the file with your domain-specific terms
3. Run the system: `python main.py`
4. Review results and refine as needed

Happy customizing! 🎉 