# Personal Writing Assistant

Fine-tune prompts — not models — to make an LLM write in *your* voice.

## Overview

This project analyzes samples of your writing (emails, posts, docs) and turns them into a reusable **style profile**. That profile is then injected into an LLM prompt (via prompt engineering, not fine-tuning) so generated content matches your tone, vocabulary, sentence structure, and quirks.

**Core idea:** instead of expensive model fine-tuning, extract stylistic patterns from your writing samples and inject them into the system prompt as few-shot examples + explicit style rules — sometimes called "prompt-based style transfer."

## How It Works

1. **Collect samples** — provide 10–50 examples of your writing (emails, LinkedIn posts, blog posts, etc.)
2. **Style analysis** — an LLM analyzes samples to extract tone, sentence length patterns, vocabulary preferences, formatting habits (bullets vs. prose, emoji use), and common phrases/openers/closers
3. **Style profile generation** — this gets condensed into a reusable style guide (structured JSON + prompt text)
4. **Generation** — when you ask for new content, the style profile + relevant example snippets are injected into the prompt
5. **Feedback loop (optional)** — rate or edit outputs, and the system refines the style profile over time

## Data Flow

```
Writing samples → style_analyzer.py → style_profile.json
                                            ↓
User request ("write an email about X") → prompt_builder.py
     (injects style_profile + relevant few-shot examples)
                                            ↓
                                       llm.py → draft output
                                            ↓
                            User edits/approves → feedback/learner.py
                                            ↓
                               style_profile.json gets refined
```

## Project Structure

```
writing-assistant/
│
├── app/
│   ├── main.py                     # Entry point (CLI or Streamlit UI)
│   ├── config.py                   # API keys, model settings
│   │
│   ├── style_engine/
│   │   ├── sample_collector.py     # Ingest writing samples (paste, upload, email export)
│   │   ├── style_analyzer.py       # LLM call: extract tone/vocab/structure patterns
│   │   ├── style_profile.py        # Build + store structured style profile (JSON)
│   │   └── profile_updater.py      # Refine profile based on user edits/feedback
│   │
│   ├── generation/
│   │   ├── prompt_builder.py       # Combine style profile + few-shot examples + task
│   │   ├── llm.py                  # Claude/GPT API wrapper
│   │   └── content_types.py        # Templates per format (email, post, message, etc.)
│   │
│   ├── feedback/
│   │   ├── diff_tracker.py         # Compare user edits vs. generated draft
│   │   └── learner.py              # Update style profile from repeated edit patterns
│   │
│   └── utils/
│       └── text_cleaner.py
│
├── data/
│   ├── writing_samples/            # Raw input samples (txt/docx/email exports)
│   ├── style_profiles/             # Saved JSON style profiles (per user/context)
│   └── generation_history/         # Past outputs + edits for learning
│
├── tests/
│   ├── test_style_analyzer.py
│   ├── test_prompt_builder.py
│   └── test_generation.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.sh
```

## Getting Started

### Prerequisites

- Python 3.10+
- An Anthropic (or OpenAI) API key

### Installation

```bash
git clone <repo-url>
cd writing-assistant
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in your API key
```

### Usage

```bash
./run.sh
```

or directly:

```bash
python -m app.main
```

**Typical flow:**

1. Add writing samples to `data/writing_samples/` (or paste them in via the CLI/UI)
2. Run style analysis to generate a profile in `data/style_profiles/`
3. Request new content ("write a follow-up email about the Q3 deadline") and get a draft matching your style
4. Edit or approve the draft — edits are logged to `data/generation_history/` and can feed back into profile refinement

## Configuration

Set the following in `.env` (see `.env.example`):

```
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-6
```

## Status / Roadmap

- [x] Project structure defined
- [ ] Sample collection (paste / file upload)
- [ ] Style analyzer (LLM-based extraction)
- [ ] Style profile schema + storage
- [ ] Prompt builder + generation
- [ ] Content-type templates (email, post, message)
- [ ] Feedback loop: diff tracking
- [ ] Feedback loop: profile refinement from edits

> **Note:** The feedback loop (`diff_tracker.py`, `learner.py`) is intentionally scoped as a v2 feature. Automatically inferring *why* an edit was made (tone vs. factual correction vs. one-off preference) from a raw diff is hard to get right. The initial version supports manual profile editing; automated learning comes once real edit patterns are observed.

## Design Notes

- **Why prompt engineering instead of fine-tuning?** Cheaper, faster to iterate, fully transparent (you can read exactly what's being injected), and easy to update as your writing style evolves — no retraining required.
- **Style profiles are versioned per user/context** — you might want a different profile for professional emails vs. casual social posts.
- Prompt templates used by the analyzer and generator are kept separate from application logic so they can be iterated on independently of the code.

## License

TBD
