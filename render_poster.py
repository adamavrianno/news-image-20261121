#!/usr/bin/env python3
"""Render poster.png: a 1024x1024 typographic news poster summing up
Saturday 21 November 2026 world news.

Run: python3 render_poster.py
Writes poster.png next to this script. Deterministic: no timestamps,
no randomness, no network. DejaVu Sans fonts from the system.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 56
CONTENT_W = W - 2 * MARGIN

NAVY = (11, 30, 54)        # dark navy background
PANEL = (18, 42, 72)       # slightly lighter navy for the lead block
WHITE = (255, 255, 255)
SUMMARY = (215, 226, 240)  # near-white blue-grey for summaries
ACCENT = (240, 168, 50)    # warm amber for kickers and rules
MUTED = (140, 162, 190)    # muted blue-grey for the footer
HAIRLINE = (42, 74, 110)   # divider lines

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
REG = FONT_DIR + "DejaVuSans.ttf"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"

MASTHEAD = "WORLD NEWS"
DATE_LINE = "Saturday, 21 November 2026"
FOOTER = "21 November 2026 \u00b7 World news summary"

# (kicker, headline, summary) — wording is the competition's own.
STORIES = [
    (
        "POLAND \u00b7 CONFLICT",
        "Russian missiles land in Poland",
        "Two missiles and a suspected drone came down; Warsaw calls it a "
        "deliberate provocation and NATO calls it a grave airspace violation.",
    ),
    (
        "JUSTICE \u00b7 THE HAGUE",
        "World Court: Myanmar committed genocide",
        "The ICJ rules Myanmar's forces committed state-sponsored genocide "
        "against the Rohingya.",
    ),
    (
        "DIPLOMACY",
        "Trump, Xi and Putin end first trilateral summit",
        "The three leaders leave the first three-way summit with few "
        "concrete results.",
    ),
    (
        "MARKETS",
        "S&P 500 enters correction as AI stocks plunge",
        "US shares fell about 3.7% on Friday as AI and chip stocks sold off.",
    ),
    (
        "EUROPE",
        "UK and EU sign food, carbon and youth-mobility deals",
        "Three agreements signed at a Brussels summit, deepening "
        "post-Brexit ties.",
    ),
    (
        "MIDDLE EAST",
        "Saudi coalition intercepts Houthi missiles over Riyadh",
        "Three ballistic missiles destroyed over the capital; the coalition "
        "strikes Hodeidah in reply.",
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def line_height(f):
    ascent, descent = f.getmetrics()
    return ascent + descent


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def render():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    f_mast = font(BOLD, 80)
    f_date = font(REG, 25)
    f_lead_kick = font(BOLD, 21)
    f_lead_head = font(BOLD, 38)
    f_lead_sum = font(REG, 23)
    f_kick = font(BOLD, 18)
    f_head = font(BOLD, 27)
    f_sum = font(REG, 20)
    f_foot = font(REG, 18)

    report = []
    y = 36

    # Masthead
    d.text((MARGIN, y), MASTHEAD, font=f_mast, fill=WHITE)
    y += line_height(f_mast)
    report.append(("masthead bottom", y))

    # Accent rule
    y += 12
    d.rectangle([MARGIN, y, MARGIN + 110, y + 5], fill=ACCENT)
    y += 5 + 14

    # Date line
    d.text((MARGIN, y), DATE_LINE, font=f_date, fill=SUMMARY)
    y += line_height(f_date)
    report.append(("date bottom", y))

    # Lead story panel (background first, then text)
    y += 20
    panel_top = y
    inner_x = MARGIN + 26
    inner_w = CONTENT_W - 52
    py = panel_top + 24
    kicker, headline, summary = STORIES[0]
    head_lines = wrap(d, headline, f_lead_head, inner_w)
    assert len(head_lines) <= 2, "lead headline over 2 lines: %r" % head_lines
    sum_lines = wrap(d, summary, f_lead_sum, inner_w)
    panel_h = (
        24
        + line_height(f_lead_kick) + 8
        + len(head_lines) * line_height(f_lead_head) + 7
        + len(sum_lines) * line_height(f_lead_sum)
        + 24
    )
    d.rounded_rectangle(
        [MARGIN, panel_top, W - MARGIN, panel_top + panel_h],
        radius=10, fill=PANEL,
    )
    d.text((inner_x, py), kicker, font=f_lead_kick, fill=ACCENT)
    py += line_height(f_lead_kick) + 8
    for line in head_lines:
        d.text((inner_x, py), line, font=f_lead_head, fill=WHITE)
        py += line_height(f_lead_head)
    py += 7
    for line in sum_lines:
        d.text((inner_x, py), line, font=f_lead_sum, fill=SUMMARY)
        py += line_height(f_lead_sum)
    y = panel_top + panel_h
    report.append(("lead panel bottom", y))
    report.append(("lead headline lines", len(head_lines)))
    report.append(("lead summary lines", len(sum_lines)))

    # Stories 2-6 as a list
    y += 14
    for idx, (kicker, headline, summary) in enumerate(STORIES[1:], start=2):
        if idx > 2:
            d.line([MARGIN, y, W - MARGIN, y], fill=HAIRLINE, width=1)
            y += 10
        d.text((MARGIN, y), kicker, font=f_kick, fill=ACCENT)
        y += line_height(f_kick) + 5
        head_lines = wrap(d, headline, f_head, CONTENT_W)
        assert len(head_lines) <= 2, "headline over 2 lines: %r" % head_lines
        for line in head_lines:
            d.text((MARGIN, y), line, font=f_head, fill=WHITE)
            y += line_height(f_head)
        y += 4
        sum_lines = wrap(d, summary, f_sum, CONTENT_W)
        for line in sum_lines:
            d.text((MARGIN, y), line, font=f_sum, fill=SUMMARY)
            y += line_height(f_sum)
        y += 8
        report.append(("story %d bottom (head %d lines, sum %d lines)"
                       % (idx, len(head_lines), len(sum_lines)), y))

    # Footer
    y += 6
    foot_w = d.textlength(FOOTER, font=f_foot)
    d.text(((W - foot_w) / 2, y), FOOTER, font=f_foot, fill=MUTED)
    y += line_height(f_foot)
    report.append(("footer bottom", y))
    report.append(("bottom margin", H - y))

    for name, value in report:
        print("%-28s %s" % (name, value))
    assert y <= H - 24, "poster overflows: bottom edge %d" % y
    return img, report


if __name__ == "__main__":
    poster, report = render()
    poster.save("poster.png", format="PNG")
    for name, value in report:
        print("%-28s %s" % (name, value))
    print("saved poster.png")
