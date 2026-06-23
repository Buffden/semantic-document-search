import fitz  # pymupdf


def parse_pdf(filepath: str) -> list[dict]:
	doc = fitz.open(filepath)
	pages = []

	for page_num, page in enumerate(doc, start = 1):
		text = page.get_text()
		if text.strip():
			pages.append({"text": text, "page": page_num})

	doc.close()
	return pages
