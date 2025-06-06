# Memory Usage Guide

## Automatic Memory System

The SecureAgents framework has **automatic memory** - no manual memory calls needed. Just set `memory_duration` when creating experts.

## Memory Options

```python
from tbh_secure_agents import Expert

# Automatic long-term memory with ChromaDB
expert = Expert(
    specialty="AI Research Specialist",
    objective="Research AI technologies", 
    background="Expert researcher",
    memory_duration="long_term",  # Uses ChromaDB backend
    user_id="researcher_001"
)

# Automatic working memory with ChromaDB  
expert = Expert(
    specialty="Content Writer",
    objective="Write engaging content",
    background="Professional writer", 
    memory_duration="auto",  # Uses ChromaDB backend
    user_id="writer_001"
)

# No memory
expert = Expert(
    specialty="Simple Calculator",
    objective="Perform calculations",
    background="Math expert",
    memory_duration="disabled"  # No memory storage
)
```

## Real Example: AI Research Team

```python
# Research Specialist - remembers research data automatically
research_specialist = Expert(
    specialty="Research Specialist in AI technology",
    objective="Conduct comprehensive research on AI automation",
    background="Expert researcher with industry analysis capabilities",
    memory_duration="long_term",  # Automatically stores all research
    user_id="research_specialist_001"
)

# Content Writer - remembers writing patterns automatically  
content_writer = Expert(
    specialty="Content Writer specializing in business technology",
    objective="Transform research into strategic guides",
    background="Skilled at creating actionable business content",
    memory_duration="auto",  # Automatically stores writing context
    user_id="content_writer_001"
)

# Use in Squad - memory works automatically
from tbh_secure_agents import Squad, Operation

research_operation = Operation(
    instructions="Research AI customer service automation trends and ROI",
    expected_output="Comprehensive research analysis",
    expert=research_specialist
)

writing_operation = Operation(
    instructions="Create implementation guide based on research",
    expected_output="Strategic implementation guide", 
    expert=content_writer
)

# Squad execution - experts automatically remember context
squad = Squad(
    experts=[research_specialist, content_writer],
    operations=[research_operation, writing_operation],
    process="sequential"
)

result = squad.deploy()  # Memory happens automatically
```

## Memory Backends

- **`long_term`**: ChromaDB vector storage with encryption
- **`auto`**: ChromaDB vector storage with smart context retention
- **`disabled`**: No memory storage

## Key Points

✅ **No manual memory calls needed** - everything is automatic  
✅ **ChromaDB backend** - vector storage with encryption  
✅ **Context sharing** - experts remember between operations  
✅ **Persistent storage** - memory survives between sessions  
✅ **Security** - all memory encrypted by default
