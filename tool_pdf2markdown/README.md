# PDF to Markdown Converter

A Python tool that converts PDF documents to Markdown format while preserving both text and images. The tool creates a structured output with embedded images and maintains the document's readability.

## Features

- Extracts text content from PDF files
- Preserves images and saves them in a dedicated directory
- Creates relative image links in the markdown output
- Handles multiple pages
- Sanitizes filenames for cross-platform compatibility

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd tool_pdf2markdown
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- Python 3.x
- pdfplumber (≥0.10.3) - For text extraction
- PyMuPDF (≥1.23.7) - For image extraction
- Pillow (≥10.0.0) - For image processing

## Usage

Convert a PDF file to Markdown using the following command:

```bash
python pdf_to_markdown.py <path_to_pdf_file>
```

For example:
```bash
python pdf_to_markdown.py test-input/document.pdf
```

### Output Structure

The tool will create:
1. A new directory named after your PDF file
2. A markdown file containing the converted text
3. An `images` subdirectory containing all extracted images

Example output structure:
```
input.pdf
input/
├── input.md
└── images/
    ├── image_1.png
    ├── image_2.png
    └── ...
```

## Error Handling

The tool includes basic error handling for:
- Missing input files
- Invalid file paths
- PDF processing errors

## Limitations

- The quality of text extraction depends on the PDF's structure
- Some complex PDF layouts might not convert perfectly
- Image quality is preserved but file sizes might vary

## License

[Your chosen license] 