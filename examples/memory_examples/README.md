# Memory Examples

This directory contains practical examples demonstrating the TBH Secure Agents framework with **simplified memory usage**. All examples use simple string-based parameters instead of complex enum imports.

## 🎯 Featured Examples

### 🔬 AI Research & Content Creation Team
**File:** `ai_research_content_creation_team.py`
- **Agents:** Research Specialist, Content Writer, Content Editor
- **Features:** Template variables, conditional guardrails, sequential processes, memory integration
- **Use Case:** Academic research, content publishing, knowledge management

### 📊 Business Intelligence Squad
**File:** `business_intelligence_squad.py`
- **Agents:** Market Analyst, Business Strategist, Intelligence Reporter
- **Features:** Advanced conditional guardrails with select syntax, multiple output formats
- **Use Case:** Market analysis, strategic planning, business intelligence reporting



## 🚀 Simplified Memory Usage

All examples demonstrate **user-friendly memory** with simple string parameters:

```python
from tbh_secure_agents import Expert, Operation, Squad

# Create an expert with memory enabled
expert = Expert(
    specialty="AI Specialist",
    objective="Analyze and remember key insights",
    memory_duration="long_term"  # Simple memory activation
)

# Store memory with simple strings (no enum imports needed!)
expert.remember(
    content="Key insight about the project",
    memory_type="LONG_TERM",     # Simple string
    priority="HIGH",             # Simple string
    tags=["important", "project"]
)

# Recall memories with simple strings
memories = expert.recall(
    query="project insights",
    memory_type="LONG_TERM",     # Simple string
    limit=5
)
```

**No complex imports required!** Just use: `from tbh_secure_agents import Expert, Operation, Squad`

## Framework Features Demonstrated

All comprehensive examples showcase:

✅ **Expert Agents** - Specialized AI agents with defined roles and memory  
✅ **Template Variables** - Dynamic behavior using `{variable_name}` syntax  
✅ **Conditional Guardrails** - Smart control flow with `select` syntax  
✅ **Sequential Squad Processes** - Coordinated multi-agent workflows  
✅ **Operations with Result Destinations** - Structured output management  
✅ **Memory Integration** - Long-term knowledge retention and sharing  
✅ **Security Profiles** - Minimal security for development environments  
✅ **Real-World Workflows** - Professional multi-agent team patterns  

## Running Examples

### Comprehensive Multi-Agent Examples
```bash
# AI Research Team (recommended starting point)
python ai_research_content_creation_team.py

# Business Intelligence
python business_intelligence_squad.py

# Software Development
python software_development_team.py
```

### Memory Options Reference

### Memory Options Reference

**Keep it simple - just two things:**

**When creating Expert:**
- `memory_duration="long_term"` - Enables memory

**When using remember():**
- `memory_type="LONG_TERM"` - Stores permanently

Done!

## Requirements

- Google Generative AI API key
- All dependencies installed (see main README)

## Setup

```bash
export GOOGLE_API_KEY="your_api_key_here"
cd examples/memory_examples
python <example_name>.py
```
