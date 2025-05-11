# TBH Secure Agents - Jupyter Notebooks

This directory contains Jupyter notebooks that demonstrate the features and capabilities of the TBH Secure Agents framework in an interactive format.

## Available Notebooks

### TBH_Secure_Agents_Features_Demo.ipynb

A comprehensive demonstration of all the key features added in the latest version of the framework:

1. **Basic Usage**: Creating experts, operations, and squads
2. **Security Profiles**: Using different security profiles (minimal, low, standard)
3. **Guardrails**: Using template variables and conditional formatting
4. **Result Destination**: Saving results to files in various formats

This notebook uses minimal security settings to make it easier to understand and run.

### TBH_Secure_Agents_Demo.ipynb

A general introduction to the TBH Secure Agents framework, covering the basic concepts and usage.

### guardrails_example.ipynb

A focused demonstration of the guardrails feature, showing how to use template variables and conditional formatting.

## Running the Notebooks

### Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click on "File" > "Upload notebook"
3. Upload the notebook you want to run
4. Make sure to set your Google API key in the notebook
5. Run the cells in sequence

### Local Jupyter

1. Install Jupyter: `pip install jupyter`
2. Navigate to the directory containing the notebooks
3. Run `jupyter notebook`
4. Open the notebook you want to run
5. Make sure to set your Google API key in the notebook
6. Run the cells in sequence

## API Key

All notebooks require a Google API key to use the Gemini model. You can get an API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

## Security Settings

The notebooks use minimal security settings to make them easier to understand and run. In a production environment, you should use higher security settings appropriate for your use case.
