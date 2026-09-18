# SkillDrop

SkillDrop is a hackathon prototype for bringing focused AI Skills Navigator learning moments into Microsoft Teams.

The current demo shows:

- An AI Skills Navigator-style sandbox for the real **Build your AI transformation plan** playlist
- A focused **Drive business value with Microsoft Copilot solutions** demo flow
- A Unit 3 SkillDrop action for bringing the Copilot Chat scenario into Teams
- A hosted lightweight Drop route that can open in the Teams browser
- A richer Teams app route for the sideloaded full experience
- A lightweight workflow-share path that uses Teams share instead of a backend

## Run locally

```bash
python3 -m http.server 8788
```

Then open:

```text
http://127.0.0.1:8788/
```

## Local Teams workflow handoff

The browser demo calls a local proxy at `http://127.0.0.1:8764/skilldrop`.

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