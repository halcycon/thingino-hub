# AI Session Onboarding Kit

Resources for developers working on Thingino Hub (or for AI-assisted development).

---

## What's Included

The repository includes AI onboarding assets in `.copilot/onboarding/`:

```
.copilot/
├── 01-about-me.template.md          # Developer preferences
├── 02-project-context.md             # Project overview
├── 03-architecture-map.md            # System architecture
├── 04-commands-checklist.md          # Common development commands
├── 05-code-style-guardrails.md       # Code style rules
├── 06-task-intake.template.md        # How to take on new tasks
├── 07-session-handoff.template.md    # How to end a session
└── 08-kickoff-prompt.template.md     # How to start a session
```

---

## Recommended Workflow

### 1. Initial Setup

Fill out your personal preferences:

```sh
cp .copilot/01-about-me.template.md ~/.copilot/my-preferences.md
# Edit with your preferences (editor, language style, etc.)
```

**Keep it light** — no secrets, just your preferences.

### 2. Starting a Development Session

Use the kickoff prompt to get an AI agent up to speed:

```sh
cat .copilot/08-kickoff-prompt.template.md
```

Copy the content and share with your AI assistant at the start of each session.

### 3. During Development

Reference the style guide to maintain consistency:

- [Code style guardrails](05-code-style-guardrails.md)
- [Commands checklist](04-commands-checklist.md)
- [Architecture map](03-architecture-map.md)

### 4. Ending a Session

Use the handoff template to document progress:

```sh
cat .copilot/07-session-handoff.template.md
```

This helps the next session (or next developer) understand what was done and what's next.

---

## For AI Assistants

If you're an AI agent working on this project:

1. **Read** `02-project-context.md` for the big picture
2. **Review** `03-architecture-map.md` to understand code organization
3. **Check** `05-code-style-guardrails.md` before making changes
4. **Use** `04-commands-checklist.md` for common tasks (running tests, building, etc.)

---

## File Descriptions

| File | Purpose |
|------|---------|
| `01-about-me.template.md` | Personal development preferences (fill once) |
| `02-project-context.md` | High-level overview of what Thingino Hub does |
| `03-architecture-map.md` | Code structure and component relationships |
| `04-commands-checklist.md` | Copy-paste commands for development (build, test, etc.) |
| `05-code-style-guardrails.md` | Coding standards and conventions |
| `06-task-intake.template.md` | How to understand and plan new tasks |
| `07-session-handoff.template.md` | How to document session progress and next steps |
| `08-kickoff-prompt.template.md` | How to brief an AI assistant at session start |

---

## Quick Tips

- **Before coding** – Read the architecture and style guide
- **When stuck** – Check the commands checklist and troubleshooting docs
- **When handing off** – Use the session handoff template to document decisions
- **Keep it DRY** – Use these templates consistently across projects

---

## Need Help?

- **Understanding the codebase?** Start with [Project Context](02-project-context.md)
- **Making changes?** Review [Code Style Guardrails](05-code-style-guardrails.md)
- **Running commands?** Check [Commands Checklist](04-commands-checklist.md)
