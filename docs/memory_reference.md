# Memory Quick Reference

## Basic Setup

```python
from tbh_secure_agents import Expert

# Long-term memory (ChromaDB)
expert = Expert(
    specialty="Your Expert Role", 
    objective="Your Expert Goal",
    background="Your Expert Background",
    memory_duration="long_term",
    user_id="unique_user_id"
)

# Auto memory (ChromaDB) 
expert = Expert(
    specialty="Your Expert Role",
    objective="Your Expert Goal", 
    background="Your Expert Background",
    memory_duration="auto",
    user_id="unique_user_id"
)

# No memory
expert = Expert(
    specialty="Your Expert Role",
    objective="Your Expert Goal",
    background="Your Expert Background", 
    memory_duration="disabled"
)
```

## Memory Types

| Type | Backend | Use Case |
|------|---------|----------|
| `long_term` | ChromaDB | Persistent knowledge, research data |
| `auto` | ChromaDB | Smart context retention, conversations |
| `disabled` | None | Simple tasks, no memory needed |

## AI Research Example

```python
from tbh_secure_agents import Expert, Squad, Operation

# Create experts with automatic memory
researcher = Expert(
    specialty="AI Research Specialist",
    objective="Research AI automation trends",
    background="Industry analysis expert",
    memory_duration="long_term",  # Remembers all research
    user_id="researcher_001"
)

writer = Expert(
    specialty="Content Writer", 
    objective="Create business guides",
    background="Technical writing expert",
    memory_duration="auto",  # Remembers writing context
    user_id="writer_001"
)

# Create operations
research_op = Operation(
    instructions="Research AI customer service automation ROI and trends",
    expected_output="Research analysis with data and insights",
    expert=researcher
)

writing_op = Operation(
    instructions="Create implementation guide based on research findings", 
    expected_output="Strategic implementation guide for executives",
    expert=writer
)

# Execute with automatic memory
squad = Squad(
    experts=[researcher, writer],
    operations=[research_op, writing_op],
    process="sequential"
)

result = squad.deploy()  # Memory works automatically
```

## Key Features

- ✅ **Automatic**: No manual memory calls required
- ✅ **ChromaDB**: Vector storage with encryption  
- ✅ **Persistent**: Memory survives between sessions
- ✅ **Secure**: All memory encrypted by default
- ✅ **Context Aware**: Experts remember previous interactions
