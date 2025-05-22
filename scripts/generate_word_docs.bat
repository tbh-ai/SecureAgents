@echo off
REM Generate Word documents from Markdown files

REM Change to the project root directory
cd /d "%~dp0\.."

REM Check if Pandoc is installed
where pandoc >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Pandoc is not installed. Please install Pandoc and try again.
    echo Installation instructions: https://pandoc.org/installing.html
    exit /b 1
)

REM Create the word_docs directory if it doesn't exist
if not exist "docs\word_docs" mkdir "docs\word_docs"

REM Convert each Markdown file to a Word document
echo Converting Markdown files to Word documents...

REM Get all Markdown files in the docs directory
set "md_files="
for %%F in (docs\*.md) do (
    set /a "file_count+=1"
    set "md_files=!md_files! %%F"
)

echo Found %file_count% Markdown files to convert

REM Convert each file
set "success_count=0"
for %%F in (docs\*.md) do (
    REM Get the filename without the path and extension
    set "filename=%%~nF"
    
    REM Skip README.md files
    if "!filename!" == "README" (
        echo Skipping %%F
    ) else (
        REM Create the output file path
        set "docx_file=docs\word_docs\!filename!.docx"
        
        echo Converting %%F to !docx_file!
        
        REM Convert the file
        pandoc -f markdown -t docx "%%F" -o "!docx_file!"
        if !ERRORLEVEL! equ 0 (
            echo Successfully converted %%F to !docx_file!
            set /a "success_count+=1"
        ) else (
            echo Failed to convert %%F to !docx_file!
        )
    )
)

REM Print summary
echo Conversion complete: %success_count% of %file_count% files converted successfully
echo Word documents are available in docs\word_docs
