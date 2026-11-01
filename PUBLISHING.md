# Publishing rule

This repository is **snapshot-only**.

- Public Git history is intentionally not retained.
- Every publish is a full-tree snapshot: one new root commit, force-pushed to `main`.
- Do not merge public history; do not rely on `git log` as a public audit trail.
- The previous public tree is replaced, not appended.
- Long-lived archives, if needed, live in a separate private repository.

Publish with:

```powershell
pwsh scripts/publish-snapshot.ps1 -Message "snapshot: <what changed>"
```

Before publishing, make sure the working tree contains only files that should be public. Drafts, local notes, databases, logs, and build artifacts must be excluded or gitignored first.
