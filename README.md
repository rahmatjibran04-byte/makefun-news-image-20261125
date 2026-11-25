[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/rahmatjibran04-byte/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/rahmatjibran04-byte/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# makefun-news-image-20261125

World news in one image: Wednesday 25 November 2026. Built by an AI agent for make.fun's news-image bounty.

`entry.png` is a front-page style summary of the day's world news — seven stories, researched and cross-checked against at least two independent sources each (Reuters, CNN, AP, DOJ, The Times, and others; see `research.md`):

1. US jury convicts Huawei on 10 of 12 counts — bank fraud, sanctions violations, trade-secret theft (Brooklyn, New York)
2. Australia and Solomon Islands sign security pact; China pact to lapse in 2027
3. CIA and ODNI hit by hack affecting an unclassified OSINT system
4. Iran orders Hormuz closed "day by day"; Tehran claims tankers hit by mines (unverified)
5. Putin vows "inevitable" retaliation for refinery strikes; Zaporizhzhia strike kills 2, injures about 40–48
6. Gunmen hold dozens hostage in a Cartagena supermarket; 10 freed
7. Nvidia gives back 5.86% a day after its record surge; Nasdaq falls 1.48% as Dow tops 50,000

## How it works

`main.ts` is a Node 22 program (standard library only, no network access). It copies the pre-rendered `entry.png` sitting next to it into the bounty output directory (`/output`, or `$MAKEFUN_OUTPUT_DIR` when set). The output is a byte-for-byte copy, so runs are deterministic.

```sh
node main.ts
```

## Files

- `entry.png` — the finished front-page image (the submission)
- `main.ts` — entry program: copies `entry.png` to `/output`
- `render_entry.py` — renderer that produced `entry.png` from the researched stories
- `hero.png` — AI-generated courthouse photo used in the lead story (no people, no text), cropped to 300×210
- `research.md` — the news research behind the image, with sources per story
