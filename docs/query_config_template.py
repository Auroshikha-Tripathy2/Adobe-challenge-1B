# =============================================================================
# QUERY CONFIGURATION TEMPLATE
# =============================================================================
# 
# This is a template file for customizing the intelligent document analysis system.
# Copy this file to 'query_config.py' and modify the values below to match your
# specific use case and domain requirements.
#
# INSTRUCTIONS:
# 1. Copy this file to 'query_config.py'
# 2. Modify the categories and keywords below to match your domain
# 3. Adjust scoring weights and preferences as needed
# 4. Test with your documents to fine-tune the results
#
# =============================================================================

# =============================================================================
# QUERY KEYWORDS - Define categories of relevant terms for your domain
# =============================================================================
# These keywords are used to build intelligent queries and filter content.
# Add categories that are relevant to your specific use case.

QUERY_KEYWORDS = {
    # EXAMPLE: Food service domain
    "dinner": ["dinner", "main", "side", "entree", "dish", "recipe"],
    "vegetarian": ["vegetarian", "vegan", "plant-based"],
    "gluten_free": ["gluten-free", "gluten free", "celiac"],
    "buffet": ["buffet", "family style", "serve yourself"],
    "corporate": ["corporate", "business", "professional", "formal"],
    "gathering": ["gathering", "event", "party", "celebration"],
    
    # ADD YOUR OWN CATEGORIES HERE:
    # "your_category": ["keyword1", "keyword2", "keyword3"],
    # "technical_terms": ["implementation", "architecture", "deployment"],
    # "business_terms": ["strategy", "marketing", "sales", "customer"],
    
    # Keep this general category for broader content
    "general": ["content", "information", "data", "details", "analysis"]
}

# =============================================================================
# BOOST WORDS - Terms that increase relevance score when found
# =============================================================================
# These words boost the relevance score when found in document content.
# Higher scores = more important content.

BOOST_WORDS = {
    # EXAMPLE: Food service boosts
    "vegetarian": {
        "keywords": ["vegetable", "veggie", "tofu", "tempeh", "legume", "bean", "lentil", "chickpea", "quinoa", "mushroom", "spinach", "kale", "broccoli", "cauliflower", "zucchini", "eggplant", "bell pepper", "tomato", "onion", "garlic", "ginger", "herbs", "spices"],
        "score": 1.5  # Increase score by 1.5 when these words are found
    },
    "gluten_free": {
        "keywords": ["gluten-free", "gluten free", "quinoa", "rice", "corn", "potato", "sweet potato", "buckwheat", "millet", "amaranth", "teff", "sorghum", "arrowroot", "tapioca", "cassava"],
        "score": 1.0
    },
    "buffet_friendly": {
        "keywords": ["serve", "platter", "bowl", "dish", "presentation", "garnish", "arrange", "display", "portion", "individual", "bite-sized", "finger food"],
        "score": 0.5
    },
    "corporate_appropriate": {
        "keywords": ["elegant", "sophisticated", "professional", "presentation", "garnish", "refined", "upscale", "premium", "quality", "artisanal"],
        "score": 0.5
    },
    "dinner_specific": {
        "keywords": ["dinner", "main course", "side dish", "entree", "evening meal"],
        "score": 2.0
    },
    
    # ADD YOUR OWN BOOST CATEGORIES HERE:
    # "technical_expertise": {
    #     "keywords": ["advanced", "expert", "professional", "certified", "specialized"],
    #     "score": 1.0
    # },
    # "business_value": {
    #     "keywords": ["ROI", "profit", "revenue", "growth", "efficiency", "cost-effective"],
    #     "score": 1.5
    # }
}

# =============================================================================
# PENALTY WORDS - Terms that decrease relevance or exclude content
# =============================================================================
# These words either exclude content entirely or reduce its relevance score.

PENALTY_WORDS = {
    # EXAMPLE: Food service exclusions
    "meat_products": {
        "keywords": ["chicken", "beef", "pork", "lamb", "fish", "seafood", "meat", "bacon", "sausage", "ham", "turkey", "duck", "goose", "venison", "rabbit", "quail", "pheasant"],
        "action": "exclude"  # Completely exclude these items
    },
    "gluten_products": {
        "keywords": ["bread", "pasta", "flour", "wheat", "rye", "barley", "couscous", "bulgur", "semolina", "durum", "spelt", "kamut", "farro", "einkorn"],
        "action": "exclude"  # Completely exclude these items
    },
    "breakfast_lunch": {
        "keywords": ["breakfast", "lunch", "morning", "noon", "brunch", "cereal", "pancake", "waffle", "omelette", "sandwich"],
        "action": "penalty",  # Apply penalty but don't exclude
        "score": -2.0  # Reduce score by 2.0 when these words are found
    },
    "desserts": {
        "keywords": ["dessert", "cake", "pie", "cookie", "ice cream", "pudding", "custard", "chocolate", "candy", "sweet"],
        "action": "penalty",
        "score": -1.0
    },
    
    # ADD YOUR OWN PENALTY CATEGORIES HERE:
    # "irrelevant_topics": {
    #     "keywords": ["unrelated", "off-topic", "irrelevant"],
    #     "action": "exclude"
    # },
    # "low_priority": {
    #     "keywords": ["basic", "introductory", "beginner", "simple"],
    #     "action": "penalty",
    #     "score": -1.0
    # }
}

# =============================================================================
# DOCUMENT PREFERENCES - Weight different document sources
# =============================================================================
# Higher scores = preferred document types. Use partial matches for flexibility.

DOCUMENT_PREFERENCES = {
    # EXAMPLE: Food service preferences
    "Dinner Ideas - Mains": 0,      # Neutral preference
    "Dinner Ideas - Sides": 0.5,    # Slight preference
    "Dinner Ideas": 5.0,            # Strong preference for dinner content
    "Lunch Ideas": 0.5,             # Slight preference
    "Breakfast Ideas": 0.0,         # No preference
    
    # ADD YOUR OWN DOCUMENT PREFERENCES HERE:
    # "Technical Manuals": 3.0,      # Strong preference for technical docs
    # "User Guides": 1.0,            # Moderate preference
    # "Marketing Materials": 0.0,    # No preference
}

# =============================================================================
# QUERY TEMPLATES - Pre-built query components
# =============================================================================
# These templates are used to build intelligent queries based on job requirements.

QUERY_TEMPLATES = {
    # EXAMPLE: Food service templates
    "dinner_menu": "dinner menu mains sides entrees",
    "vegetarian": "vegetarian plant-based vegetable",
    "gluten_free": "gluten-free gluten free",
    "buffet": "buffet serve platter presentation",
    "corporate": "corporate professional elegant",
    "gathering": "gathering event party celebration",
    
    # ADD YOUR OWN QUERY TEMPLATES HERE:
    # "technical_implementation": "implementation architecture deployment",
    # "business_strategy": "strategy planning business development",
    # "customer_service": "customer support service satisfaction",
}

# =============================================================================
# SCORING WEIGHTS - Balance different scoring components
# =============================================================================
# Adjust these weights to control how different factors influence the final score.

SCORING_WEIGHTS = {
    "semantic_similarity": 1.0,     # AI semantic matching (0.5-2.0 recommended)
    "keyword_boost": 1.0,           # Keyword matching boosts (0.5-2.0 recommended)
    "document_preference": 0.5,     # Document source preference (0.1-1.0 recommended)
    "penalty": 1.0                  # Penalty application (0.5-2.0 recommended)
}

# =============================================================================
# CUSTOMIZATION TIPS
# =============================================================================
#
# 1. START WITH KEYWORDS: Begin by defining QUERY_KEYWORDS for your domain
# 2. ADD BOOSTS: Identify important terms that should increase relevance
# 3. SET PENALTIES: Define terms that should be excluded or penalized
# 4. ADJUST PREFERENCES: Weight different document sources appropriately
# 5. FINE-TUNE WEIGHTS: Balance the scoring components for optimal results
#
# TESTING WORKFLOW:
# 1. Make small changes and test with your documents
# 2. Review the output to see how changes affect results
# 3. Iterate and refine based on actual performance
# 4. Keep a backup of working configurations
#
# ============================================================================= 