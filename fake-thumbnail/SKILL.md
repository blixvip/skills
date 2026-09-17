---
name: fake-thumbnail
description: Produce a clearly labeled dummy thumbnail concept for testing skill discovery and thumbnail workflows. Use when asked for a fake thumbnail, test thumbnail, or placeholder thumbnail concept.
---

# Fake Thumbnail

Return a small text-only thumbnail mockup for the supplied topic. This is a test skill; its output is a concept, not a generated image.

Use the user's topic and any requested text or colors. If no topic is supplied, use "My Next Video" without asking a follow-up question.

Return these fields:

- **Type:** TEST MOCKUP — no image generated.
- **Topic:** The supplied topic, or the default.
- **Canvas:** 1280 × 720, 16:9.
- **Headline:** A short sample headline, ideally two to four words.
- **Layout:** One sentence describing the main subject and headline placement.
- **Colors:** Two or three colors suited to the concept.

Keep the result under 120 words. Do not invoke image generation, download assets, write files, or publish anything for this test. If the user requests a finished image, explain that this skill only returns a text mockup; do not claim to have generated an image.
