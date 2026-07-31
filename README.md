# autodigest

`autodigest` is a personal learning repository for digesting complex topics in a repeatable way.

The goal is not to store everything. The goal is to turn difficult material into your own structured understanding:

1. Capture raw material.
2. Split it into digestible units.
3. Extract claims, concepts, mechanisms, examples, and open questions.
4. Rebuild the idea in your own language.
5. Produce reusable notes, explanations, checklists, diagrams, or essays.

## Repository Layout

```text
autodigest/
  inbox/       Raw notes, links, copied fragments, temporary ideas.
  sources/     Source records for books, papers, talks, docs, code, or courses.
  digests/     Processed learning notes, one digest per focused unit.
  concepts/    Reusable concept pages, definitions, models, and distinctions.
  outputs/     Final artifacts: essays, study guides, talks, diagrams, prompts.
  prompts/     Prompts used for AI-assisted digestion.
  scripts/     Small local automation.
  templates/   Markdown templates.
```

## Core Workflow

### 1. Start From A Topic

Create a source file:

```bash
cp templates/source.md sources/my-topic.md
```

Record:

- What you are studying.
- Why it matters.
- Where the material comes from.
- What kind of output you want.

### 2. Create Digest Notes

Use one digest note per narrow unit:

```bash
cp templates/digest.md digests/my-topic-part-1.md
```

A good digest unit is small enough that you can explain it clearly in 5 to 15 minutes.

### 3. Promote Concepts

When a term, mechanism, pattern, or distinction appears repeatedly, create a concept page:

```bash
cp templates/concept.md concepts/my-concept.md
```

Concept pages should become stable reference material.

### 4. Produce Something

Turn the processed material into an output:

```bash
cp templates/output.md outputs/my-topic-explained.md
```

Outputs are where understanding becomes communicable.

## Automation

Create a new learning packet with:

```bash
python3 scripts/new_digest.py "Transformer Attention"
```

This creates linked files in `sources/`, `digests/`, and `outputs/`.

## Digest Standard

Every serious digest should answer:

- What problem is this solving?
- What are the core parts?
- How do the parts interact?
- What is the minimum runnable example or concrete case?
- What do I still not understand?
- How would I explain this to someone one level below me?

## Git Habit

Commit when a unit of understanding becomes clearer:

```bash
git add .
git commit -m "Digest transformer attention basics"
```

