# Content Guidelines

Rules for MDX content in client tenant repositories.

## File structure

Each language has its own directory under `content/`:

```
content/
├── lt/          # Lithuanian (default/pilot)
│   ├── pages/   # Static pages (index, apie, kontaktai, etc.)
│   ├── news/    # Blog/news items (YYYY-MM-slug.mdx)
│   └── blocks/  # Reusable snippets
├── en/          # English mirror
└── ru/          # Russian mirror
```

## MDX front-matter

Every MDX file must have front-matter matching `schemas/content.schema.json`:

```yaml
---
title: "Page Title"
lang: lt
type: page
slug: page-slug
description: "Brief description for SEO"
---
```

## Image rules (WCAG 2.2 AA)

- Every `<img>` must have an `alt` attribute
- Decorative images use `alt=""`
- Complex images need a text description nearby
- Store images in `assets/client-owns/` (tracked via Git LFS)

## Content parity

- v1: LT (default language) must have all pages. EN/RU are warning-only.
- v2: All three languages must have identical page structures.

## News items

File naming: `YYYY-MM-slug.mdx` (e.g., `2026-09-kvietimas.mdx`)
