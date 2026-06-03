# Commit description template (required sections)

**Output format — two separate copyable parts:**

1. **Title** — on its own line, wrapped in **inline code** (backticks) so the user can copy it separately.
2. **Description** — all sections below in **one** fenced code block (` ```text `) so the UI shows a **Copy** button. Do not split description into multiple fences.

**Do NOT** put Title inside the fenced block. Title and Description must be visually and structurally separate for easy copy-paste into commit title / PR body fields.

All sections required; use YES/NO where noted.

## Structure

1. **🤖 AI Contribution** — tick one: None / Consult / Assist / Heavy. For Assist/Heavy, also tick sub-checklist when true:
   - I have manually reviewed logic
   - I understand the code generated
   - I tested critical paths
2. **Scope of changes** — In scope (ticket + brief); Out of scope (or "NO")
3. **API changes** — Per endpoint: name on its own line, indented bullets; or "NO"
4. **DB changes** — YES/NO (+ sql/migration details if YES)
5. **Config changes** — YES/NO
6. **Integration** — YES/NO
7. **Permission** — YES/NO

## Title format

`[LINKID-XXXX] - <6–14 words, outcome-focused, no trailing period>`

## Minimal example

Title: `[LINKID-6313] - add private object key to import storage`

Description (single block — one fence for Copy button):

```text
## 🤖 AI Contribution
- [ ] None
- [ ] Consult
- [x] Assist
- [ ] Heavy
### If Assist / Heavy:
- [x] I have manually reviewed logic
- [x] I understand the code generated
- [x] I tested critical paths

1. Scope of changes:
- In scope: [LINKID-6313]: private object key for import storage
- Out of scope: NO
2. API changes:
POST /import-storage: add privateObjectKey to request/response
3. DB changes: NO
4. Config changes: NO
5. Integration: NO
6. Permission: NO
```
