import docx


def parse_docx(filepath: str) -> list[dict]:
	doc = docx.Document(filepath)
	sections = []
	current_heading = None
	buffer = []

	for para in doc.paragraphs:
		if para.style.name.startswith("Heading"):
			if buffer:
				sections.append({"text": "\n".join(buffer), "heading": current_heading})
				buffer = []
			current_heading = para.text.strip() or None
		else:
			if para.text.strip():
				buffer.append(para.text.strip())

	if buffer:
		sections.append({"text": "\n".join(buffer), "heading": current_heading})

	return sections
