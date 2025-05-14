# TBH Secure Agents - Stakeholder Demo

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

## Competitive Analysis Demo

This example demonstrates a comprehensive business use case for the TBH Secure Agents framework: a competitive analysis project using multiple AI experts working together to research the cloud computing industry, analyze competitors, and develop strategic recommendations.

### Business Value Demonstrated

This demo shows how TBH Secure Agents can:

1. **Automate Complex Analysis**: Transform market research into actionable business strategy
2. **Enable Multi-Expert Collaboration**: Coordinate specialized experts for comprehensive analysis
3. **Improve Decision Making**: Generate strategic recommendations based on competitive intelligence
4. **Increase Efficiency**: Complete what would take a team weeks in minutes
5. **Maintain Security**: Process sensitive business data with appropriate security controls
6. **Deliver Consistent Results**: Produce professional outputs in multiple formats

### Features Demonstrated

The example showcases key technical capabilities:

- **Multiple Specialized Experts**: Creating experts with different roles and expertise
- **Sequential Operations**: Building a workflow where each expert builds on previous results
- **Squad Coordination**: Managing multiple experts working together on a complex task
- **Dynamic Guardrails**: Controlling expert behavior with runtime parameters
- **Multi-Format Output**: Saving results in both Markdown and JSON formats

### Running the Demo

To run this example:

1. Install the package:
   ```bash
   pip install tbh-secure-agents
   ```

2. Set your Google API key as an environment variable:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here  # Replace with your actual API key
   ```

3. Run the script:
   ```bash
   python examples/stakeholder_demo.py
   ```

4. Review the outputs in the `output` directory:
   - `strategic_recommendations.md`: Actionable strategic recommendations
   - `competitive_analysis_summary.json`: Complete analysis in structured JSON format

### Implementation Details

The demo implements a three-stage analysis pipeline:

1. **Market Research**: An expert researches the cloud computing industry with focus on AI services
2. **Competitor Analysis**: A second expert analyzes the top competitors based on the research
3. **Strategy Development**: A third expert creates strategic recommendations based on the analysis

All three experts work together in a squad, with each operation building on the results of the previous one.

### Terminal Output

When running this example, you'll see detailed terminal output showing:

- The initialization of each expert with their specialty and security profile
- The execution of each operation in sequence
- Progress updates as the analysis moves through different stages
- Completion status and timing information for each step
- Final output locations for the generated files

This terminal output provides visibility into the multi-expert workflow and demonstrates the framework's capabilities without requiring any additional print statements.

### Security Considerations

This demo uses the minimal security profile for simplicity in demonstration. For production use cases with sensitive data, consider using the "default" or "high" security profile.

### Customization Options

This example can be easily adapted for your specific business needs:

- Change the industry focus to your specific sector
- Modify the guardrail parameters to target different aspects
- Adjust the expert specialties and backgrounds
- Customize the output formats and file paths

### Next Steps

After reviewing this demo, consider:

1. Customizing it for your specific industry or business needs
2. Exploring the other examples in the `examples` directory
3. Reading the comprehensive documentation in the `docs` directory
4. Implementing a proof-of-concept for your specific use case
