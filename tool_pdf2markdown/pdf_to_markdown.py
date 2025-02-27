import pdfplumber
import fitz  # PyMuPDF
import os
from pathlib import Path
import re
from PIL import Image
import io

def sanitize_filename(filename):
    """Convert string to valid filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def pdf_to_markdown(pdf_path):
    # Get the paths
    pdf_path = Path(pdf_path)
    base_name = pdf_path.stem
    output_dir = pdf_path.parent / base_name
    image_dir = output_dir / "images"
    markdown_path = output_dir / f"{base_name}.md"
    
    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    
    markdown_content = []
    image_counter = 1
    
    # Extract text using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        for page in pages:
            text = page.extract_text()
            if text:
                markdown_content.append(text)
    
    # Extract images using PyMuPDF
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Generate image filename
            image_filename = f"image_{image_counter}.png"
            image_path = image_dir / image_filename
            
            # Convert and save image
            image = Image.open(io.BytesIO(image_bytes))
            image.save(image_path)
            
            # Add image reference to markdown with relative path
            markdown_content.append(f"\n![Image {image_counter}](images/{image_filename})\n")
            image_counter += 1
    
    pdf_document.close()
    
    # Write markdown content to file
    with open(markdown_path, 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(markdown_content))
    
    return markdown_path, image_dir

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_markdown.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)
    
    try:
        markdown_path, image_dir = pdf_to_markdown(pdf_path)
        print(f"Successfully converted PDF to Markdown: {markdown_path}")
        print(f"Images saved in directory: {image_dir}")
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        sys.exit(1) 