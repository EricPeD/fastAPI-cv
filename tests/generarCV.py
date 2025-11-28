import fitz  # PyMuPDF
from pathlib import Path

# Path to the base markdown file
base_md_path = Path("testCV/cv/sample_cv.md")
# Output directory for new PDF files
output_dir = Path("testCV/cv/")
output_dir.mkdir(parents=True, exist_ok=True)

# Read the base markdown content
base_md_content = base_md_path.read_text(encoding="utf-8")

# Generate 14 additional unique PDF files
num_variants = 14
generated_files = []

for i in range(1, num_variants + 1):
    new_name = f"Juan Pérez Variante {i}"
    new_email = f"juan.variante{i}@email.com"
    new_phone = f"+34 600 123 4{i:02d}"  # Two digits for phone variation

    # Replace placeholders in the base content
    variant_content = base_md_content.replace("# Juan Pérez García", f"# {new_name}")
    variant_content = variant_content.replace("juan.perez.dev@email.com", new_email)
    variant_content = variant_content.replace("+34 600 123 456", new_phone)

    # Create a new PDF file
    pdf_file_name = f"sample_cv_variant_{i:02d}.pdf"
    output_pdf_path = output_dir / pdf_file_name

    doc = fitz.open()  # new PDF document
    page = doc.new_page()  # new page
    page.insert_text(
        (50, 50), variant_content, fontname="helv", fontsize=10
    )  # Insert text, adjust position, font and size as needed

    doc.save(output_pdf_path)
    doc.close()

    generated_files.append(output_pdf_path)
    print(f"Generated: {output_pdf_path}")

print(f"\nGenerated {len(generated_files)} PDF variants in {output_dir}")
