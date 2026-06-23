import re # Python's built in regular expressions module


def parse_markdown(filepath: str) -> list[dict]:
	with open(filepath, "r", encoding = "utf-8") as f:
		raw = f.read()

	sections = []
	current_heading = None
	buffer = []

	for line in raw.splitlines():
		heading_match = re.match(r"^#{1,6}\s+(.*)", line)
		if heading_match:
			if buffer:
				sections.append({"text": "\n".join(buffer), "heading": current_heading})
				buffer = []
			current_heading = heading_match.group(1).strip() or None
		else:
			cleaned = _strip_markdown(line)
			if cleaned:
				buffer.append(cleaned)

	if buffer:
		sections.append({"text": "\n".join(buffer), "heading": current_heading})

	return sections


def _strip_markdown(line: str) -> str:
	if re.match(r"^```", line):
		return ""
	if re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", line):
		return ""
	line = re.sub(r"^>\s?", "", line)
	line = re.sub(r"^\s*[-*+]\s+", "", line)
	line = re.sub(r"^\s*\d+\.\s+", "", line)
	line = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", line)
	line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
	line = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", line)
	line = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", line)
	line = re.sub(r"`([^`]*)`", r"\1", line)
	line = re.sub(r"<[^>]+>", "", line)
	return line.strip()
