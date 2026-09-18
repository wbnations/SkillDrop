# SkillDrop

SkillDrop is a hackathon prototype for bringing focused AI Skills Navigator learning moments into Microsoft Teams.

The current demo shows:

- An AI Skills Navigator-style sandbox for the real **Build your AI transformation plan** playlist
- Topic-level **Send this topic to Teams** actions
- A structured SkillDrop payload for a workflow/Power Automate handoff
- A lightweight Teams app package for custom app sideload testing

## Run locally

```bash
python3 -m http.server 8788
```

Then open:

```text
http://127.0.0.1:8788/
```

## GitHub Pages

This repo is ready for GitHub Pages because the sandbox is published as `index.html`.

Recommended Pages setting:

```text
Deploy from a branch -> main -> / (root)
```

## Teams app install test

Upload this package in Teams to check whether custom app sideloading is allowed:

```text
teams-app/skilldrop-test/skilldrop-test-teams-app.zip
```