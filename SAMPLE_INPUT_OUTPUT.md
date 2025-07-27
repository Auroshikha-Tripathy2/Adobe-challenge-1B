# Sample Input/Output for Testing

## Sample Input

### challenge_input.json
```json
{
  "persona": {
    "role": "Food Contractor",
    "experience": "5+ years in corporate catering",
    "specialization": "Vegetarian and dietary restriction menus"
  },
  "job_to_be_done": {
    "task": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items.",
    "constraints": [
      "Must be vegetarian",
      "Include gluten-free options",
      "Suitable for corporate event",
      "Buffet-style presentation"
    ],
    "target_audience": "Corporate professionals, mixed dietary preferences"
  },
  "documents": [
    {"filename": "Dinner Ideas - Mains_1.pdf"},
    {"filename": "Dinner Ideas - Mains_2.pdf"},
    {"filename": "Dinner Ideas - Sides_1.pdf"},
    {"filename": "Dinner Ideas - Sides_2.pdf"},
    {"filename": "Dinner Ideas - Sides_3.pdf"}
  ],
  "requirements": {
    "top_k": 5,
    "focus_areas": ["main dishes", "side dishes", "presentation", "dietary compliance"]
  }
}
```

### Sample PDF Content Structure
```
Dinner Ideas - Mains_1.pdf:
├── Section: "Vegetarian Pasta Primavera"
│   ├── Content: "Fresh seasonal vegetables with al dente pasta..."
│   └── Page: 1
├── Section: "Quinoa Buddha Bowl"
│   ├── Content: "Nutritious quinoa with roasted vegetables..."
│   └── Page: 2
└── Section: "Grilled Portobello Mushrooms"
    ├── Content: "Marinated portobello mushrooms with herbs..."
    └── Page: 3

Dinner Ideas - Sides_1.pdf:
├── Section: "Gluten-Free Roasted Vegetables"
│   ├── Content: "Assorted seasonal vegetables roasted with olive oil..."
│   └── Page: 1
├── Section: "Quinoa Pilaf"
│   ├── Content: "Fluffy quinoa with aromatic spices..."
│   └── Page: 2
└── Section: "Fresh Garden Salad"
    ├── Content: "Mixed greens with cherry tomatoes and cucumber..."
    └── Page: 3
```

## Expected Output

### challenge_output.json
```json
{
  "metadata": {
    "input_documents": [
      "Dinner Ideas - Mains_1.pdf",
      "Dinner Ideas - Mains_2.pdf",
      "Dinner Ideas - Sides_1.pdf",
      "Dinner Ideas - Sides_2.pdf",
      "Dinner Ideas - Sides_3.pdf"
    ],
    "persona": "Food Contractor",
    "job_to_be_done": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items.",
    "intelligent_query": "dinner menu mains sides entrees vegetarian plant-based vegetable gluten-free gluten free buffet serve platter presentation corporate professional elegant gathering event party celebration",
    "config_used": "query_config.py"
  },
  "extracted_sections": [
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "section_title": "Vegetarian Pasta Primavera",
      "importance_rank": 1,
      "page_number": 1
    },
    {
      "document": "Dinner Ideas - Sides_1.pdf",
      "section_title": "Gluten-Free Roasted Vegetables",
      "importance_rank": 2,
      "page_number": 1
    },
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "section_title": "Quinoa Buddha Bowl",
      "importance_rank": 3,
      "page_number": 2
    },
    {
      "document": "Dinner Ideas - Sides_1.pdf",
      "section_title": "Quinoa Pilaf",
      "importance_rank": 4,
      "page_number": 2
    },
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "section_title": "Grilled Portobello Mushrooms",
      "importance_rank": 5,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "refined_text": "Fresh seasonal vegetables with al dente pasta, tossed in a light olive oil and herb sauce. Perfect for a buffet-style presentation. Can be made gluten-free with appropriate pasta alternatives. This dish offers a colorful and nutritious option that appeals to both vegetarians and those with dietary restrictions. The combination of crisp vegetables and perfectly cooked pasta creates a satisfying main course that works well in a corporate setting.",
      "page_number": 1
    },
    {
      "document": "Dinner Ideas - Sides_1.pdf",
      "refined_text": "Assorted seasonal vegetables roasted with olive oil, garlic, and fresh herbs. Naturally gluten-free and perfect for buffet service. Includes carrots, zucchini, bell peppers, and cherry tomatoes. This side dish provides essential nutrients while accommodating various dietary needs. The roasting process enhances natural flavors and creates an appealing presentation that complements any main course.",
      "page_number": 1
    },
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "refined_text": "Nutritious quinoa with roasted vegetables, avocado, and a tahini dressing. Complete protein source suitable for vegetarian diets. Can be customized for gluten-free requirements. This bowl-style dish offers a modern, healthy option that's both visually appealing and nutritionally balanced. Perfect for corporate events where health-conscious choices are valued.",
      "page_number": 2
    },
    {
      "document": "Dinner Ideas - Sides_1.pdf",
      "refined_text": "Fluffy quinoa with aromatic spices, dried fruits, and nuts. Gluten-free grain option that adds protein and texture to the buffet spread. Includes golden raisins and toasted almonds. This pilaf provides a sophisticated side dish that elevates the overall menu while meeting dietary requirements. The combination of sweet and savory elements creates a memorable dining experience.",
      "page_number": 2
    },
    {
      "document": "Dinner Ideas - Mains_1.pdf",
      "refined_text": "Marinated portobello mushrooms with herbs and balsamic glaze. Substantial vegetarian option that can serve as a main course. Naturally gluten-free and suitable for buffet presentation. These meaty mushrooms provide a satisfying alternative to traditional protein sources while maintaining visual appeal and flavor complexity. Perfect for corporate gatherings where dietary diversity is important.",
      "page_number": 3
    }
  ]
}
```

## Testing Scenarios

### Test Case 1: Basic Vegetarian Menu
- **Input**: 3 dinner PDFs with vegetarian content
- **Expected**: Top 5 vegetarian main dishes and sides
- **Validation**: All results should be vegetarian, include gluten-free options

### Test Case 2: Dietary Restrictions Focus
- **Input**: Mix of regular and dietary-specific PDFs
- **Expected**: Prioritize gluten-free and vegetarian options
- **Validation**: Results should emphasize dietary compliance

### Test Case 3: Corporate Event Focus
- **Input**: Various meal type PDFs (breakfast, lunch, dinner)
- **Expected**: Dinner-focused content with corporate presentation
- **Validation**: Results should favor dinner and professional presentation

### Test Case 4: Performance Test
- **Input**: 5 PDFs with 20+ sections each
- **Expected**: Processing completes within 60 seconds
- **Validation**: Time measurement and memory usage monitoring

## Validation Checklist

- [ ] All extracted sections are relevant to the job requirements
- [ ] Vegetarian and gluten-free options are prioritized
- [ ] Dinner-specific content is favored over breakfast/lunch
- [ ] Processing time is under 60 seconds
- [ ] Output JSON is properly formatted and complete
- [ ] No irrelevant content (meat dishes, breakfast items) included
- [ ] Model size remains under 1GB
- [ ] CPU-only execution without GPU dependencies 