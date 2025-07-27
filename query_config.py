# Query Configuration for Intelligent Document Analysis
# Users can modify these keywords to customize the system behavior

# Core query keywords for different job types
QUERY_KEYWORDS = {
    "dinner": ["dinner", "main", "side", "entree", "dish", "recipe"],
    "vegetarian": ["vegetarian", "vegan", "plant-based"],
    "gluten_free": ["gluten-free", "gluten free", "celiac"],
    "buffet": ["buffet", "family style", "serve yourself"],
    "corporate": ["corporate", "business", "professional", "formal"],
    "gathering": ["gathering", "event", "party", "celebration"],
    "general": ["content", "information", "data", "details", "analysis"]
}

# Boost words that increase relevance score when found in content
BOOST_WORDS = {
    "vegetarian": {
        "keywords": ["vegetable", "veggie", "tofu", "tempeh", "legume", "bean", "lentil", "chickpea", "quinoa", "mushroom", "spinach", "kale", "broccoli", "cauliflower", "zucchini", "eggplant", "bell pepper", "tomato", "onion", "garlic", "ginger", "herbs", "spices"],
        "score": 1.5
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
    }
}

# Penalty words that decrease relevance score or exclude content
PENALTY_WORDS = {
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
        "score": -2.0
    },
    "desserts": {
        "keywords": ["dessert", "cake", "pie", "cookie", "ice cream", "pudding", "custard", "chocolate", "candy", "sweet"],
        "action": "penalty",
        "score": -1.0
    }
}

# Document type preferences (higher scores for preferred document types)
DOCUMENT_PREFERENCES = {
    "Dinner Ideas - Mains": 0,
    "Dinner Ideas - Sides": 0.5,
    "Dinner Ideas": 5.0,
    "Lunch Ideas": 0.5,
    "Breakfast Ideas": 0.0
}

# Query building templates for different job types
QUERY_TEMPLATES = {
    "dinner_menu": "dinner menu mains sides entrees",
    "vegetarian": "vegetarian plant-based vegetable",
    "gluten_free": "gluten-free gluten free",
    "buffet": "buffet serve platter presentation",
    "corporate": "corporate professional elegant",
    "gathering": "gathering event party celebration"
}

# Scoring weights for different components
SCORING_WEIGHTS = {
    "semantic_similarity": 1.0,
    "keyword_boost": 1.0,
    "document_preference": 0.5,
    "penalty": 1.0
} 