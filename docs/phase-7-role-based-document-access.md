# RDE-7 | Phase 7: Role-Based Document Access

**Status:** Todo
**Type:** Feature
**Priority:** Medium
**Depends on:** RDE-6

---

## Goal

Control which documents a user can search and chat over -- not every user should see every document. Right now any query searches the entire Chroma collection. In a real product, documents belong to teams, projects, or individuals. This phase adds an access control layer: documents are tagged with ownership metadata at ingestion time, and all search and retrieval is filtered by the current user's permissions before results are returned.

---

## What Changes from Phase 6

- Ingestion extended to accept an `--owner` or `--access` flag, stored as metadata on every chunk
- Search and RAG pipeline wrapped with an access filter that injects a metadata constraint before querying Chroma
- A simple `users.json` config defines users and their allowed document groups
- All modes (search, chat, one-shot QA) go through the access layer -- no bypass path

---

## Tasks

- [ ] Create `users.json` -- defines users, their roles, and which document groups they can access
  ```json
  {
    "alice": { "role": "admin", "groups": ["engineering", "hr"] },
    "bob":   { "role": "member", "groups": ["engineering"] }
  }
  ```
- [ ] Create `access.py` -- given a username, returns the set of allowed source groups as a Chroma metadata filter
- [ ] Update `ingest.py` -- add `--owner <group>` CLI flag; tag all chunks with the group value on ingestion
- [ ] Update `search.py` -- accept a `user` parameter, call `access.py` to get the filter, inject it into `collection.query()`
- [ ] Update `rag.py` -- accept a `--user` argument, pass the access filter through to retrieval
- [ ] Update `chat.py` -- accept a `--user` argument, enforce access filter on every turn
- [ ] Test: ingest the same document under two different owner groups; verify that a user with access to only one group cannot retrieve chunks from the other

---

## Acceptance Criteria

- `python ingest.py documents/hr-policy.pdf --owner hr` tags all chunks with `group=hr`
- `python rag.py --user bob "What is the leave policy?"` returns no results if Bob does not have access to `hr` group
- `python rag.py --user alice "What is the leave policy?"` returns the correct answer since Alice has access to `hr`
- Access is enforced at the Chroma query level -- no chunks from disallowed groups appear in results under any mode
- All three modes (rag, chat, search) respect the same access rules

---

## Stack Additions

None -- uses existing Chroma metadata filtering.

---

## Questions to Answer Before Closing

- Why is enforcing access at the vector DB query level safer than filtering results after retrieval?
- What happens if a document is re-ingested with a different owner -- which chunks win?
- How would you model group-based access vs user-based access in metadata?
- What does this pattern look like in production when the user identity comes from a JWT instead of a config file?
