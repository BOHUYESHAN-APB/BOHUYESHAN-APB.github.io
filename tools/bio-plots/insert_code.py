# -*- coding: utf-8 -*-
"""Insert standalone plotting snippets into gallery post 1.

- SNIPPETS_A/B: keyed by the unique last CSV line of each data toggle;
  the code block is appended inside that toggle, right before endhideToggle.
- NEW_BLOCKS: keyed by a unique caption line; a brand-new code-only toggle is
  inserted right after the caption paragraph.
Idempotent: skips a key if its marker text is already present in the file.
"""
from pathlib import Path

from snippets_a import SNIPPETS_A
from snippets_b import SNIPPETS_B, NEW_BLOCKS

MARKER = "**绘图代码（Python，独立可运行）**"
POST = (Path(__file__).resolve().parent.parent.parent / "source" / "_posts"
        / "2026-09-12-01-生信图表大全-从火山图到森林图的解读与绘制.md")
ALLOWED = (Path(__file__).resolve().parent.parent.parent / "source" / "_posts").resolve()


def main():
    target = POST.resolve()
    if not target.is_relative_to(ALLOWED) or target.suffix != ".md":
        raise ValueError("refusing to write outside _posts")
    text = target.read_text(encoding="utf-8")

    inserted, skipped = 0, 0
    for key, code in {**SNIPPETS_A, **SNIPPETS_B}.items():
        if MARKER in text and text.count(key) >= 2:
            skipped += 1
            continue
        anchor = key + "\n```\n\n{% endhideToggle %}"
        if anchor not in text:
            print("ANCHOR NOT FOUND:", key)
            continue
        block = (key + "\n```\n\n" + MARKER + "\n\n```python\n"
                 + code.strip("\n") + "\n```\n\n{% endhideToggle %}")
        text = text.replace(anchor, block, 1)
        inserted += 1

    for caption, block in NEW_BLOCKS.items():
        if block[:60] in text:
            skipped += 1
            continue
        if caption not in text:
            print("CAPTION NOT FOUND:", caption[:40])
            continue
        text = text.replace(caption, caption + "\n\n" + block, 1)
        inserted += 1

    target.write_text(text, encoding="utf-8", newline="\n")
    print("inserted:", inserted, "skipped:", skipped)


if __name__ == "__main__":
    main()
