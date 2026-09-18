# SkillDrop

SkillDrop is a hackathon prototype for bringing focused AI Skills Navigator learning moments into Microsoft Teams.

The current demo shows:

- An AI Skills Navigator-style sandbox for the real **Build your AI transformation plan** playlist
- A focused **Drive business value with Microsoft Copilot solutions** demo flow
- A Unit 3 SkillDrop action for bringing the Copilot Chat scenario into Teams
- A hosted lightweight Drop route that can open in the Teams browser
- A richer Teams app route for the sideloaded full experience
- A lightweight workflow-share path that uses Teams share instead of a backend
- A runtime-configured Power Automate HTTP trigger path for sending a workflow card without committing secrets
- A downloadable Copilot SkillDrop skill file for applying Unit 3 to the learner's own work context

## Run locally

```bash
python3 -m http.server 8788
```

Then open:

```text
http://127.0.0.1:8788/
```

## Local Teams workflow handoff

The browser demo can call a Power Automate HTTP trigger at runtime. Do not commit the trigger URL to GitHub.

Recommended Power Automate flow:

1. Trigger: **When an HTTP request is received**
2. Action: **Post card in a chat or channel**
3. Optional action: create a SharePoint list item for telemetry

The GitHub-hosted page sends the payload with an unverified browser POST so the Flow URL can stay out of the repo. Treat the Teams card or Flow run history as the confirmation source.

Expected JSON payload:

```json
{
  "title": "SkillDrop: Copilot Chat for client-call preparation",
  "course": "Drive business value with Microsoft Copilot solutions",
  "unit": "Unit 3 of 8 - Explore Copilot experiences",
  "concept": "Copilot Chat gives fast, context-aware answers grounded in organizational data.",
  "scenario": "Imagine a regional manager needs a summary of last quarter's performance before a client call. Copilot Chat pulls data from reports and emails, delivering a concise, accurate summary in seconds.",
  "question": "What is the biggest business value in the regional manager scenario?",
  "choices": [
    "A. A faster, context-aware summary before the client call",
    "B. A longer report with every source copied in",
    "C. A new place to manually search for documents"
  ],
  "correctChoice": "A",
  "practicePrompt": "Think of a client or stakeholder conversation this week. What quick summary would help you walk in better prepared?",
  "dropUrl": "https://wbnations.github.io/SkillDrop/#drop",
  "fullExperienceUrl": "https://teams.microsoft.com/l/entity/9c2ae80f-253c-4772-86d7-3ed5e1bc8cb2/skilldrop-full?webUrl=https%3A%2F%2Fwbnations.github.io%2FSkillDrop%2F%23teams-full&label=SkillDrop",
  "footerCta": "Get the full SkillDrop experience with the ASN Teams app."
}
```

Suggested card footer:

```text
Get the full SkillDrop experience with the ASN Teams app.
```

Legacy local proxy path:

The browser demo can also call a local proxy at `http://127.0.0.1:8764/skilldrop`.

For a reliable Teams card demo, create a Power Automate flow with an HTTP request trigger, then run:

```bash
SKILLDROP_FLOW_URL='<your Power Automate HTTP trigger URL>' python3 proxy-server.py
```

Without `SKILLDROP_FLOW_URL`, the UI still shows the payload path, but it reports that the workflow is not connected instead of claiming a Teams card was sent.

## GitHub Pages

This repo is ready for GitHub Pages because the sandbox is published as `index.html`.

Primary demo routes:

```text
https://wbnations.github.io/SkillDrop/
https://wbnations.github.io/SkillDrop/#drop
https://wbnations.github.io/SkillDrop/#teams-full
```

## Copilot SkillDrop file

Use this file when testing the Copilot handoff:

```text
skills/SkillDrop_CopilotChat.md
```

Recommended test flow:

1. Open `https://wbnations.github.io/SkillDrop/#drop`
2. Click **Copy Copilot SkillDrop prompt**
3. Click **Open Copilot**
4. Paste the prompt into Copilot
5. Optionally download/upload `SkillDrop_CopilotChat.md` as a structured skill artifact

Recommended Pages setting:

```text
Deploy from a branch -> main -> / (root)
```

## Teams app install test

Upload this package in Teams to install the fuller SkillDrop Teams experience:

```text
teams-app/skilldrop-test/skilldrop-test-teams-app.zip
```

The Teams app points to:

```text
https://wbnations.github.io/SkillDrop/#teams-full
```