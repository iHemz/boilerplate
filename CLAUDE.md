# Project Instructions

> Adopted from the [boilerplate](https://github.com/iHemz/boilerplate). Replace the
> placeholder lines marked `<!-- ADOPT -->` with this project's specifics, then delete
> this note.

<!-- ADOPT --> **What this is:** one paragraph on the product, who uses it, and what
"working" means. An agent that knows the product makes better calls than one that only
knows the code.

## Quick reference

| Task           | Command                                            |
| -------------- | -------------------------------------------------- |
| Dev (web)      | `pnpm --filter web dev` → http://localhost:3000 |
| Dev (api)      | `cd apps/api && uv run uvicorn main:app --reload` → http://localhost:8000 |
| Typecheck      | `pnpm --filter web typecheck`                 |
| Lint           | `pnpm --filter web lint`                      |
| Format         | `pnpm --filter web format` / `format:check`   |
| Unit tests     | `pnpm --filter web test`                      |
| E2E tests      | `pnpm --filter web test:e2e`                  |
| Build          | `pnpm --filter web build`                     |
| Python lint    | `cd apps/api && uv run ruff check .`                |
| Python format  | `cd apps/api && uv run ruff format .`               |
| Python tests   | `cd apps/api && uv run pytest`                      |

**Package managers:** `pnpm` for `apps/web`, `uv` for `apps/api`. Do not use npm, yarn, or pip.
`pnpm install` runs at the **workspace root**, not inside a package.

## Structure

```
.
├── apps/
│   ├── web/             Next.js 16 · React 19 · TypeScript (strict) · Tailwind v4 · TanStack Query
│   │   ├── app/         Routes. Thin server components — no "use client", no hooks.
│   │   ├── components/  Client logic, grouped by domain, assembled by a *View component.
│   │   ├── lib/         api.ts (the only bridge to the API), queries/, utils.ts
│   │   └── e2e/         Playwright specs
│   └── api/             FastAPI · Python 3.12 · uv
│       ├── api/         routes/ (thin), deps.py (assembly), error_handlers.py
│       ├── core/        config, errors, logging, llm — cross-cutting infrastructure
│       ├── domain/      Pure models and logic. No I/O, no framework imports.
│       ├── services/    Use-cases. Orchestrate domain + repositories; raise domain errors.
│       ├── repositories/ The only layer that touches storage.
│       └── tests/       Mirrors the source tree
├── packages/            Shared workspace packages (types, ui, config) — empty until needed
├── .claude/             skills/, commands/, agents/
├── .husky/              Pre-commit quality gate
└── .github/workflows/   CI
```

## Architecture rules

**`apps/web` flow — enforce it end to end:**
`page (server) → *View (client) → query hook → lib/api.ts → apps/api`

- `app/**` are server components. Adding `"use client"` there is a smell — push the
  interactivity into a `components/<domain>/*View.tsx` instead.
- `lib/api.ts` is the only module that calls `fetch`. Components never do.
- One TanStack Query hook file per domain in `lib/queries/`, with a query-key factory.

**`apps/api` layers — one-directional, no shortcuts:**
`route → service → domain → repository`

- Routes validate shape and delegate. No business rules, no try/except — domain errors
  are mapped to HTTP centrally in `api/error_handlers.py`.
- Services own the use-case and raise `core.errors` exceptions. They never import FastAPI.
- Domain logic is pure: no I/O, no framework, no storage. This is where tests are cheapest.
- Repositories are the only place that touches storage. Services depend on the `Protocol`,
  never a concrete class, so the backing store is swappable.
- Everything crossing a boundary is a Pydantic model, never a raw dict.
- Every Claude call goes through `core/llm.py`. Use `parse()` with a Pydantic schema when
  you need structured data — the API enforces the schema, so there is no JSON to repair.

## Naming (enforced by the pre-commit hook)

- `.tsx` → PascalCase: `ItemCard.tsx`, `ItemsView.tsx`
- `.ts` → lowercase-first: `api.ts`, `use-items.ts`
- Folders → lowercase-first: `components/`, `lib/queries/`
- Next.js reserved names are exempt: `page.tsx`, `layout.tsx`, `route.ts`, `error.tsx`, …
- Python follows PEP 8 (`snake_case`), enforced by ruff.

## Git workflow

**Never commit or push directly to `main`.** Every change goes through a feature branch
and a PR.

1. Check the branch (`git branch --show-current`). If on `main`, branch first.
2. Branch names: `feat/`, `fix/`, `refactor/`, `chore/`, `docs/`, `test/` + kebab-case.
3. Conventional commits: `type(scope): subject`, describing **what changed and why** —
   never how it was built or what tooling was involved.
4. `/ship` does the whole flow: branch → gates → commit → push → PR.

## Before opening a PR

- [ ] `pnpm --filter web typecheck` passes
- [ ] `pnpm --filter web lint` passes
- [ ] `pnpm --filter web format:check` clean
- [ ] `pnpm --filter web test` passes
- [ ] `pnpm --filter web build` succeeds
- [ ] `cd apps/api && uv run ruff check . && uv run ruff format --check . && uv run pytest`
- [ ] Verified in the browser — no console errors, no hydration warnings
- [ ] Responsive at ~375px / 768px / 1280px; keyboard-accessible; respects
      `prefers-reduced-motion`

## Helpers

**Skills:** `/ship`, `/test`, `/bugs`, `/principal`, `/triage`, `/tycoon`, `/resolve-conflicts`
**Commands:** `/play`, `/html-transformer`
**Agents:** `code-review`, `research-agent`, `ui-ux-expert`
