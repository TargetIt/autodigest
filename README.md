# autodigest

`autodigest` is a personal learning repository and writing workflow for digesting complex concepts in a repeatable way.

The goal is not to store everything. The goal is to turn difficult material into your own structured understanding:

1. Capture raw material.
2. Identify the exact object to digest.
3. Extract claims, concepts, mechanisms, examples, and open questions.
4. Rebuild the idea from multiple angles.
5. Produce several explanation articles that make the concept usable.

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
  workflows/   The fixed Auto Digest workflow.
```

## Auto Digest Workflow

When you say "use Auto Digest" for a complex concept, process the target with this workflow:

1. Define the digestion target.
2. State the source boundary: what evidence is available and what must not be invented.
3. Build a neutral core model of the concept.
4. Rewrite the concept into eight explanation articles:
   - first principles
   - customer demand
   - everyday analogy
   - historical development
   - layered system structure
   - cybernetics and feedback
   - information theory
   - runnable demo
5. Extract reusable concepts and unresolved questions.
6. Turn the result into final outputs.

The detailed workflow is in `workflows/autodigest.md`.

## Start A New Auto Digest Packet

```bash
python3 scripts/new_digest.py "Transformer Attention"
```

This creates linked files in `sources/`, `digests/`, `concepts/`, and `outputs/<topic>/`.

The output folder contains the eight article drafts.

## Manual Workflow

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
