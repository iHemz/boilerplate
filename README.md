# Boilerplate

A production-shaped starting point for a **Next.js + FastAPI** product: the layering,
quality gates, and agent tooling already wired and green, so a new project starts at the
interesting part.

This is not a template you fill in — it's a working app with one reference vertical slice
(`items`) that demonstrates every layer. Copy it, rename it, replace the slice.

## What's in the box

**Frontend** — Next.js 16 (App Router), React 19, TypeScript in strict mode with
`noUncheckedIndexedAccess`, Tailwind v4 with design tokens, TanStack Query, Vitest +
Testing Library, Playwright, ESLint, Prettier, Stylelint.

**Backend** — FastAPI on Python 3.12 with `uv`, a one-directional layered architecture
(route → service → domain → repository), typed settings, centralised error mapping,
structured JSON logging in production, pytest, ruff (lint + format), and a non-root
Dockerfile.

**Model providers** — one client for Claude and Grok behind a shared protocol, with
retries, schema-enforced structured output on both, usage/cost logging, and **narrow**
failover: only an unusable provider (exhausted credit, rejected key, hard capacity) advances
the chain, so a malformed request fails loudly on one account instead of billing two. The
test suite has an autouse guard that fails any test which reaches for a real client.

**Repo** — pre-commit hook (lint-staged, tsc, naming conventions, ruff), GitHub Actions CI
with path filters so docs-only changes skip the matrix, `.editorconfig`, and a `.claude/`
directory of skills, commands, and agents.

## Getting started

Prerequisites: Node 24+, [pnpm](https://pnpm.io), [uv](https://docs.astral.sh/uv/).

```bash
pnpm install
cp apps/web/.env.local.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env

# Terminal 1 — API on :8000
cd apps/api && uv sync && uv run uvicorn main:app --reload

# Terminal 2 — web on :3000
pnpm --filter web dev
```

Open http://localhost:3000. The page lists items from the API, creates them, and moves
them through a status machine — the full `page → view → query → api → route → service →
domain → repository` path in one screen.

## Adopting it for a new product

Run the `/adopt` skill with your spec:

```
/adopt path/to/spec.md
```

It copies the foundation, renames it, strips the example slice, and builds the first
vertical slice from the spec — following the layering the boilerplate already enforces.

Doing it by hand is the same six steps, written out in
[`.claude/skills/adopt/SKILL.md`](.claude/skills/adopt/SKILL.md).

## The rules worth knowing

The full set is in [`CLAUDE.md`](CLAUDE.md). The load-bearing ones:

- **`lib/api.ts` is the only module that calls `fetch`.** Components call query hooks.
- **`app/**` are server components.** Interactivity lives in `components/<domain>/*View.tsx`.
- **Backend layers are one-directional.** Domain logic is pure — no I/O, no framework
  imports — which is why it's the cheapest place to test.
- **Only repositories touch storage,** and services depend on the `Protocol`, not the
  implementation. Swapping in-memory for Postgres is one new class and one line in `deps.py`.
- **Routes have no try/except.** Services raise `core.errors` exceptions;
  `api/error_handlers.py` maps them to status codes once.
- **Every model call goes through `core/llm.py`.** Use `parse()` with a Pydantic schema
  when you need structured data — the provider enforces it, so there's no JSON to repair.
  `core/providers.py` is the only module allowed to import a provider SDK.
- **Failover stays narrow.** Widening it past `ProviderUnavailable` re-runs bugs on a
  second account and hides them behind the fallback's answer.

## Commands

```bash
# Frontend
pnpm --filter web dev | build | typecheck | lint | test | test:e2e | format:check

# Backend
cd apps/api && uv run uvicorn main:app --reload
cd apps/api && uv run ruff check . && uv run ruff format --check . && uv run pytest
```

## Storage

The reference slice ships an in-memory repository — zero setup, and it makes the
`Protocol` seam obvious. It does not survive a restart. To move to a real database, add a
second class implementing `ItemsRepository` and change the provider in `apps/api/api/deps.py`.
Nothing above that line changes.

## License

MIT
