# Word Document Versions of Documentation

This directory contains Microsoft Word (.docx) versions of the TBH Secure Agents documentation. These files are provided for users who prefer to read or print documentation in Word format.

## Download Word Documents

### Core Documentation
- [Installation Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Usage Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Version Changes (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)

### Security Documentation
- [Security Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Security Profiles Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Hybrid Security Validation Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Attack Prevention (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)

### Feature Documentation
- [Guardrails Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Result Destination Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Error Messages Guide (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)
- [Performance Optimization (Word)](https://docs.google.com/document/d/1Yx9VFUk6IFSegWWPCAjnQb6Je4NJpYO_7UHhzV8kHJA/export?format=docx)

## Converting Markdown to Word

You can convert the Markdown documentation to Word documents using one of these methods:

### Method 1: Using Pandoc (Recommended)

[Pandoc](https://pandoc.org/) is a universal document converter that can convert Markdown to Word.

1. Install Pandoc from [pandoc.org/installing.html](https://pandoc.org/installing.html)
2. Run the following command to convert a Markdown file to Word:

```bash
cd SecureAgents
pandoc -f markdown -t docx docs/installation.md -o docs/word_docs/installation.docx
```

### Method 2: Using Online Converters

You can use online Markdown to Word converters:

1. [Markdown to Word Converter](https://word2md.com/)
2. [CloudConvert](https://cloudconvert.com/md-to-docx)
3. [Dillinger](https://dillinger.io/) (Export to Word)

### Method 3: Copy and Paste into Word

1. Open the Markdown file in a text editor or GitHub
2. Copy the content
3. Paste into Microsoft Word
4. Format as needed

## Batch Conversion Script

For your convenience, we've included scripts to convert all documentation files at once:

### For macOS/Linux:

```bash
cd SecureAgents
./scripts/generate_word_docs.sh
```

### For Windows:

```bash
cd SecureAgents
scripts\generate_word_docs.bat
```

## Contact

If you need help with the documentation or encounter any issues with the Word documents, please contact:

- Email: saish.shinde.jb@gmail.com
- GitHub: Open an issue on the [GitHub repository](https://github.com/saishshinde15/TBH.AI_SecureAgents)
