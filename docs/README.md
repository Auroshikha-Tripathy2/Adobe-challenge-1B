# Documentation

This folder contains documentation and configuration templates for the Intelligent Document Analysis System.

## Files

### `query_config_template.py`
A comprehensive template for customizing the system's intelligent analysis parameters. This file includes:
- **Query Keywords**: Define categories of relevant terms for your domain
- **Boost Words**: Terms that increase relevance score when found
- **Penalty Words**: Terms that decrease relevance or exclude content
- **Document Preferences**: Weight different document sources
- **Query Templates**: Pre-built query components
- **Scoring Weights**: Balance different scoring components

### `QUICK_SETUP_GUIDE.md`
A step-by-step guide for quickly customizing the system for new domains. Includes:
- **3-Step Quick Start**: Copy template, customize, test
- **Common Examples**: Technical, business, legal domains
- **Scoring Guidelines**: Conservative vs aggressive approaches
- **Troubleshooting**: Common issues and solutions
- **Best Practices**: Tips for optimal configuration

## Usage

1. **For new users**: Start with `QUICK_SETUP_GUIDE.md`
2. **Copy the template**: `cp docs/query_config_template.py query_config.py`
3. **Customize**: Edit `query_config.py` with your domain-specific terms
4. **Test**: Run the system and refine as needed

## Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `query_config_template.py` | Configuration template | Starting a new project |
| `QUICK_SETUP_GUIDE.md` | Setup instructions | First-time setup or new domain | 