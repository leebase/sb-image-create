# sb-image-create Architecture

> Record of technical decisions that shape how the application is implemented.

---

## 2026-03-20 - Built-In Prompt Logic Instead Of Runtime Markdown Parsing

**Decision:** The Python app will encode prompt-building logic directly in code rather than reading `skills/*.md` or `agents/*.md` files at runtime.

**Rationale:** The app is meant to be callable from anywhere with predictable behavior. Bundling the prompt rules into the executable code is more portable, less fragile, and easier to version than relying on external markdown files at call time.

**Alternatives rejected:**
- Read skill files dynamically at runtime: rejected because it couples execution to repo file layout and creates drift risk.
- Keep all prompt logic only in docs: rejected because it would leave implementation behavior underspecified.

**Consequences:**
- Updating prompt logic requires a code change and redeploy/reinstall.
- Skills and agent docs remain valuable as upgrade references and design guidance.

---

## 2026-03-20 - One Invocation Produces Paired Outputs

**Decision:** The `generate` command creates both the cover and thumbnail in one invocation.

**Rationale:** This matches the actual story-packaging workflow and reduces orchestration complexity for calling agents.

**Alternatives rejected:**
- Separate `cover` and `thumbnail` commands: rejected because it pushes pairing logic to callers.

**Consequences:**
- Output naming and metadata must consistently describe both assets together.
- Thumbnail generation can directly use the freshly generated cover as its source.

---

## 2026-03-20 - Derived Output Naming

**Decision:** Output filenames are derived from a filename-safe slug of the title unless `--name-root` is explicitly provided.

**Rationale:** This keeps the command terse while preserving predictable output paths for automation.

**Alternatives rejected:**
- Require full output paths for every call: rejected because it adds repetitive boilerplate.

**Consequences:**
- The slugging function is part of the contract and must be tested.
- The app should fail clearly if a safe slug cannot be derived.
