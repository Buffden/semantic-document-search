from pathlib import Path
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .markdown_parser import parse_markdown


def _parse_txt(filepath: str) -> list[dict]:
	with open(filepath, "r", encoding = "utf-8") as f:
		return [{"text": f.read()}]


_PARSERS = {
	".txt": _parse_txt,
	".pdf": parse_pdf,
	".docx": parse_docx,
	".md": parse_markdown,
}

SUPPORTED_EXTENSIONS = set(_PARSERS.keys())


def _resolve_parser(filepath: str):
	ext = Path(filepath).suffix.lower()
	parser = _PARSERS.get(ext)
	if parser is None:
		raise ValueError(f"Unsupported file type: {ext}")
	return parser


def _flatten(sections: list[dict]) -> str:
	return "\n\n".join(s["text"] for s in sections)


def parse(filepath: str) -> str:
	parser = _resolve_parser(filepath)
	return _flatten(parser(filepath))
