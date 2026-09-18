# SkillDrop

Today, learners are busy and often cannot commit to a full module in one sitting. They may also be asked to sign in and navigate before they have experienced any value. We believe these barriers can suppress starts and repeat participation.

SkillDrop tests a simpler approach: a colleague shares one focused, role-relevant lesson directly in Microsoft Teams. No account is required to read it, practice one idea, or get immediate value. The learner can then return to work and continue learning later at their own pace. Only after value has been delivered are they invited to save progress with one click using Microsoft sign-in.

SkillDrop repurposes existing AI Skills Navigator (ASN) content into self-contained Drops. Structured modules already contain learning-objective chunks; long-form videos and webinars can be segmented automatically from their transcripts. This creates short learning moments without requiring new content authoring from the ASN team.

Each Drop goes beyond passive consumption. It can include a short practice task or knowledge check that asks the learner to demonstrate what they understood. A later follow-up--potentially weeks or months afterward--asks how the skill worked in practice: what they applied, what changed, and whether it produced meaningful business value. The learner's response creates evidence connecting skilling to real work outcomes, not just course completion.

The experience is instrumented across the full loop: content-led signup, practice completion, return behavior, peer sharing, organizational spread, application, and longer-term perceived value. SkillDrop turns ASN content into a measurable path from immediate learning, to behavior change, to potential business impact.

**SkillDrop: Skill at your pace. Stay in your flow.**

## Current demo

The current demo shows an ASN-style course experience, a Unit 3 SkillDrop Copilot handoff, a downloadable skill file, a return-to-ASN results page with Frontier Points, and an ASN business-leader dashboard for UTM behavior, learner outcomes, Copilot handoff signals, and share-driven registrations.

## Run locally

```bash
python3 -m http.server 8788
```

Then open:

```text
http://127.0.0.1:8788/
```

## Local Teams workflow handoff

The primary hosted demo uses Teams share links and Copilot handoff buttons, not a backend. A Power Automate HTTP trigger path is still present as a local/runtime experiment, but this tenant's default developer DLP policy may block `HttpRequestReceived`, so do not rely on it for the final demo.

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
https://wbnations.github.io/SkillDrop/#return
https://wbnations.github.io/SkillDrop/#admin
```

## Copilot SkillDrop file

Use this file when testing the Copilot handoff:

```text
skills/SkillDrop_CopilotChat.md
```

Recommended test flow:

1. Open `https://wbnations.github.io/SkillDrop/`
2. Start the recommended Copilot module and navigate to **Unit 3: Explore Copilot experiences**
3. Click **Copy Copilot prompt** or **Download skill file**
4. Click **Open Copilot**, paste the prompt, and complete the coaching flow
5. Return to `#return` to submit the completion summary and claim 250 Frontier Points
6. Open `#admin` to view sample UTM behavior, handoff actions, Frontier Points, and new registrant trail

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