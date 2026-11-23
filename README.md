# The World in One Day — Monday 23 November 2026 (slot 2)

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/adeqaila/makefun-news-image-20261123-slot2/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/adeqaila/makefun-news-image-20261123-slot2/reward.svg)](https://make.fun/bounty/news-image-20261123)

A program that writes one image summing up the world's news of Monday
23 November 2026: **"Monday's Own Front Page"** — 30 verified stories
across 7 regions, led by the day's genuinely Monday events: the AI
sell-off routing world markets (Nikkei −5.06%), Iran vowing "all means"
against a US blockade as two supertankers are hit near Hormuz, and the
COP31 collapse with no deal.

## How it works

`draw.py` renders the front page deterministically (PIL, no network, no
randomness) to `entry-v2.png`; `entry.png` is the chosen render.
`main.py` (stdlib only) copies `entry.png` to `/output/entry.png`.

## Files

- `entry.png` — the submitted image (1024×1024 PNG, < 1 MiB)
- `main.py` — entrypoint
- `draw.py` — renderer (`python3 draw.py v1` / `v2` for the two variants)
- `entry-v1.png` — variant 1 (36 stories, denser; not submitted)
- `entry-v2.png` — variant 2 (30 stories, larger type; submitted as entry.png)
- `AUDIT.md` — every story with its source + rejected-stale list
- `BUILD-REPORT.md` — study, variants, Hermes tournament, verification
