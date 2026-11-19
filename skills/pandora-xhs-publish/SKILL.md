---
name: pandora-xhs-publish
description: Read a Xiaohongshu note from a Markdown file and fill its title, body, images, and relevant topic in the creator publishing page using Computer Use. Use when the user asks to prepare a note for Xiaohongshu; the user must log in if prompted.
---

# Pandora Xiaohongshu Publishing Assistant

Use Computer Use to prepare a note in the Xiaohongshu creator publishing page from a Markdown file the user specifies. Fill the page for the user to review; do not publish the note.

Expect a card in `{{你的仓库}}/内容创作/02-待发布/` (`status: review`). Its images stay in `{{你的仓库}}/assets/xhs-images/<slug>/`. Read image links as the full path `{{你的仓库}}/assets/xhs-images/<slug>/01.png` (and `02.png` onward in that same folder). That path stays valid wherever the card sits. Replace `{{你的仓库}}` before use. After the user confirms the note was published, move only the card to `{{你的仓库}}/内容创作/03-已发布/` and set `status: published`. If the card also has `状态`, set it to `已发布`. Leave the image files in `assets/xhs-images/`. Do not move the card before that confirmation.

## Workflow

1. Ask for the Markdown file path only if the user has not provided one. If the user gives a slug or title without a path, look in `{{你的仓库}}/内容创作/02-待发布/`. Read the file and identify the title, body/caption, and image links. Preserve supplied wording and ordering; do not rewrite copy unless the user asks or gives permission to draft missing content.
2. Check that the title, body, and referenced images are identifiable. If required information is missing or ambiguous, report the specific issue before changing the publishing form.
3. Open the Xiaohongshu creator publishing page using Computer Use. If login or verification is required, stop and ask the user to complete it in the browser. Do not handle passwords or authentication codes or bypass verification. Continue after the logged-in creator page is visibly available.
4. Choose the publishing mode that matches the material (image-and-text when the note has images). Enter the title and body, preserving wording and line breaks as closely as the interface allows.
5. Add each referenced image through normal browser and file-picker controls. Images are the files at `{{你的仓库}}/assets/xhs-images/<slug>/`, in Markdown order. Preserve that order. If an image cannot be accessed or uploaded, stop and report which image could not be added; do not omit or replace it silently.
6. Add at least one relevant topic to the note. Prefer an accurate, available platform topic that matches the note's subject and reader value. Avoid unrelated high-traffic suggestions. Verify that the selected topic appears in the note before proceeding.
7. Only declare the note original when the user explicitly asks for an original declaration and the note's authorship can reasonably support that claim. Open the original declaration switch, read the on-screen notice, select the acknowledgement checkbox, and click the final “声明原创” action. If the content includes material whose ownership or authorization is unclear, pause and ask the user before making the claim. Verify that the page shows the declaration completed. Do not infer permission to declare originality merely from a request to fill a note.
8. Review the page visually. Confirm title, body, image count and order, selected topic, and (when requested) completed originality status. Mention any interface-imposed formatting differences.
9. Leave the page open for the user to review. Never click Publish, Schedule, or an equivalent action to publish the note. Do not alter account settings, add locations, select commercial disclosures, or change other fields unless the user explicitly asks.
10. Only after the user confirms the note was published, move the card to `{{你的仓库}}/内容创作/03-已发布/` and set `status: published` (`状态: 已发布` when that field exists). Do not move `{{你的仓库}}/assets/xhs-images/<slug>/`.

## Computer Use

Use the computer-use browser controls and visible page state. Prefer ordinary click, type, scroll, and file-picker actions. Do not use hidden page scripting, direct APIs, browser storage, or methods that bypass the visible creator workflow. Keep the user informed when login is required and when the form is ready for review.
