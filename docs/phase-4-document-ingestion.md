# RDE-4 | Phase 4: Document Ingestion

**Status:** Todo
**Type:** Feature
**Priority:** High
**Depends on:** RDE-3

---

## Goal

Support real document formats and a proper ingestion trigger -- not just static `.txt` files in a folder. Add format-specific parsers for PDF, DOCX, and Markdown, and expose a CLI command so users can drop in a file and ingest it without editing code.

---

## What Changes from Phase 3

- New `ingest/` module with format-specific parsers
- `ingest.py` updated to accept a file path or directory as a CLI argument and route by file extension
- Any format in, plain text out -- same embedding and Chroma storage flow after parsing

---

## Tasks

- [ ] Create `ingest/pdf_parser.py` -- extract plain text from PDF files using `pymupdf` or `pdfplumber`
- [ ] Create `ingest/docx_parser.py` -- extract plain text from DOCX files using `python-docx`
- [ ] Create `ingest/markdown_parser.py` -- strip Markdown syntax, return clean plain text
- [ ] Create `ingest/router.py` -- detect file type by extension, call the right parser, return plain text
- [ ] Update `ingest.py` with CLI interface -- `python ingest.py <file_or_directory>` ingests any supported format
- [ ] Add deduplication to `ingest.py` -- before adding chunks for a file, delete all existing Chroma chunks with the same `source` metadata value so re-ingesting replaces rather than duplicates

---

## Acceptance Criteria

- `python ingest.py documents/report.pdf` parses the PDF and ingests all chunks into Chroma
- `python ingest.py documents/notes.docx` parses the DOCX and ingests all chunks into Chroma
- `python ingest.py documents/readme.md` strips Markdown and ingests clean text into Chroma
- `python ingest.py documents/` ingests all supported files in the directory
- Re-running ingestion on the same file replaces its chunks -- no duplicates accumulate in Chroma
- `rag.py` and `search.py` work correctly over newly ingested PDFs and DOCX files

---

## Stack Additions

- `pymupdf` or `pdfplumber` for PDF parsing
- `python-docx` for DOCX parsing

---

## Questions to Answer Before Closing

- How do you handle PDFs with tables or images -- what gets lost?
- What metadata is worth extracting at parse time (title, author, page number)?
- How do you handle multi-page PDFs where a chunk might span a page boundary?
- What happens if the same file is ingested twice -- how do you avoid duplicate vectors?
