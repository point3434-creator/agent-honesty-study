# Agent honesty study

How honestly does a team of AI research agents report its own results, when an exact checker grades many of
those results later?

One human (Jeff, not a programmer) and a team of AI agents have spent weeks on a Kaggle optimization
competition. The agents do almost all of the technical work. The official verifier, the leaderboard and long GPU runs
give exact answers that the agents' earlier claims can be checked against. This repository compares the two.

**Headline:** claims that rest on an exact check held (24 of 32 uploads within 0.01%, the rest explained by one
randomly sampled task). Claims that rest on a fast proxy, a model estimate or an early lead were biased optimistic
(14 of the 20 overclaims we found). Premature "this is dead" verdicts were the opposite error, and they cost more
time.

- Write-up: [STUDY.md](STUDY.md)
- Data: [data/](data/) (three small CSV files)
- Recompute every number: `python3 scripts/summarize.py` (Python 3, no packages needed)

## What is not here

Nothing about how the circuits are built, no absolute scores, no submission files and no competition data. The
competition ends in January 2027; the full project is planned to go public after that.

## Who wrote this

Jeff is the accountable author. The analysis and first draft were done by Claude (Anthropic), working as one of the
agents in the project, and Jeff approved publication. Questions and corrections are welcome as GitHub issues.

## License

Text and data: [CC BY 4.0](LICENSE). Code in `scripts/`: [MIT](LICENSE-CODE).
