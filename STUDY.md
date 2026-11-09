# How honestly do AI research agents report their results?

*A field study from one human working with a team of AI agents, November 2026.*

**Author and accountable human:** Jeff. **Analysis and first draft:** Claude (Anthropic), working as one of the
agents in the project. Jeff read it before publication and is responsible for what it says.

## The setting

Jeff is not a programmer. Since October 2026 he has entered a Kaggle optimization competition (compiling quantum
circuits) with a team of AI agents doing nearly all the technical work. One "coordinator" agent talks with Jeff and
starts work "threads". Each thread is another AI agent with its own task: building a submission, running a long GPU
search, reviewing an idea, or playing devil's advocate. A second AI coding agent (OpenAI Codex) runs on Jeff's own
computer. The agents share an idea ledger and a small knowledge base where each idea gets a verdict ("adopt", "dead",
"parked", ...) and a tag for the evidence behind it:

| tag | evidence |
|---|---|
| [L] | exact local check with the competition's official verifier |
| [K] | the Kaggle leaderboard score |
| [P] | a small probe or benchmark |
| [M] | a model, estimate or bound |
| [R] | an outside source (paper, forum, public notebook) |

Jeff decides what gets uploaded, what gets killed and how money and compute are spent. The agents decide almost
everything else.

This setting has one property most AI-honesty studies lack: **a lot of what the agents claim is later checked by
something that cannot be argued with.** The official verifier and the leaderboard give an exact score, and long GPU
runs give an exact final error. So we can compare what the agents said before the check with what the check said.

## Short answer

1. **When a claim rests on an exact check, it holds.** Of 32 distinct uploads whose score the agents wrote down before
   uploading, 24 scored within 0.01% of the prediction. The other 8 are all explained by one task that the grader
   scores on its own random samples, so a few samples can fail on the grader's draw that passed on ours. Those misses
   go both ways (3 above, 5 below, worst −0.60%).
2. **When a claim rests on a proxy, a model or the early part of a run, it is biased optimistic.** Of 28 claims that
   were later corrected, 20 were overclaims. 14 of those 20 rested on a fast proxy, a model estimate or an early lead.
3. **The opposite error lives in "kills".** All 8 underclaims were "dead", "no-go" or "park" verdicts that rested on a
   model or a small probe. Four of them sat on one line of work, a ladder of compression levels: rungs were called
   "no-go", "dead", "parked" and "a NO" in turn, and then three of those rungs passed and shipped. The kills had
   stated their scope ("at today's pipeline"), but later agents read them as general.
4. **Bets.** In 10 scored, pre-registered predictions, the agents were too optimistic 6 times and too pessimistic 4
   times. They called pass or fail right in 5 of 7 calls, and both misses were "pass" calls close to the line that
   failed. The agents' number beat Jeff's 7 times out of 10.
5. **The weakest link was record keeping, not the claims.** One upload scored 0.28% below its prediction and nobody
   wrote the score down for three days. Another was listed in the agents' memory as "not uploaded" when the leaderboard
   had already scored it, exactly as predicted. The brief for this very study named an incident that nobody could
   find a source for.

## Method

**Sources.** The idea ledger (1,175 rows), the knowledge base (1,443 records, with a history of 34 status changes),
the agents' shared memory notes (138 files), several agent conversation threads, and the folder of every submission
the agents built.

**Exact checker 1: the leaderboard.** Kaggle's read-only API lists every scored upload with the size of the zip file.
We matched each size byte-for-byte to a submission folder and read the predicted score that the building agent wrote
in that folder's README before upload. For rebuilds of public notebooks without a README, the prediction comes from
the saved official-verifier receipts. Data: [`data/uploads.csv`](data/uploads.csv) (deviation only; absolute scores
are left out until the competition ends).

**Exact checker 2: long runs.** Before several long GPU runs, the agent running it and Jeff each wrote down a number
for the final error. We collected those bets with the measured result. Data: [`data/bets.csv`](data/bets.csv), given as
each prediction's error (prediction minus actual; lower is better, so a negative error is too optimistic).

**Corrections.** We searched the ledger for words like "overturned", "reopened", "corrected", "erratum", "artifact"
and "did not transfer" (about 70 rows each for the two ledger files). We kept the 28 rows where a later exact check
changed an earlier claim's number or verdict, and coded each by direction and by the evidence behind the original
claim. Data: [`data/corrected_claims.csv`](data/corrected_claims.csv).

Every number in this write-up can be recomputed with `python3 scripts/summarize.py`.

## Results

### Predicted score vs leaderboard (33 distinct uploads with a prediction)

| | n | within 0.01% | above prediction | below prediction | worst |
|---|---|---|---|---|---|
| Own builds and public-notebook rebuilds | 32 | 24 | 3 | 5 | −0.60% |
| One public-notebook rebuild | 1 | | | 1 | −10.0% (one task about 27% worse than our local check; cause never found) |

All 8 small misses trace to the randomly sampled task. One README gave two numbers, "at the default draw" and "at zero failures", and the leaderboard landed on the
second. That two-number format is the honest one, and it is now a rule (rule 4 below).

One more upload was scored after this study was drafted. It landed 0.15% below its single-number prediction, the
same task and the same direction as before. Its README reported extra random draws but still gave one headline number.

### Pre-registered bets (10 scored)

| bet | agent error | Jeff's error | agent's call | outcome |
|---|---|---|---|---|
| B01 | −0.15 | −0.10 | | |
| B02 | −0.05 | −0.09 | fail | fail |
| B03 | −0.27 | −0.37 | **pass** | **fail** |
| B04 | −0.02 | −0.22 | | |
| B05 | +2.52 | −5.08 | fail | fail |
| B06 | +0.08 | +0.15 | pass | pass |
| B07 | +0.19 | +0.15 | pass | pass |
| B08 | +0.02 | −0.10 | | |
| B09 | −0.16 | −0.17 | pass | pass |
| B10 | −0.50 | −0.48 | **pass** | **fail** |

Three more bets could not be scored (one agent number was never written down, one run was killed early, one is still
pending). At n = 10 only large effects show. Every optimistic miss was made by the thread that had set up the run
itself, and the two biggest (B03, B10) were "pass" calls close to the line.

*Correction to our own internal draft:* the agents' first write-up said Jeff "won every bet where he was more
pessimistic". The data say he was more pessimistic three times and closer in two of them. The overclaim was the AI's,
in a study about AI overclaiming. We left it in as a data point.

### Corrected claims (28)

| evidence behind the original claim | overclaims | underclaims (premature kill) |
|---|---|---|
| Fast proxy, or proxy noise | 5 | 0 |
| Model, estimate or bound [M] | 7 | 3 |
| Early stage of a run | 2 | 0 |
| Agent judgement | 1 | 0 |
| Small probe or benchmark [P] | 1 | 5 |
| Exact local verifier [L] | 2 | 0 |
| Outside claims [R] | 2 | 0 |

Corrections were cheap when the original claim said what it rested on: several were corrected by the same agent,
with an erratum next to the old text. They were expensive when a proxy number went straight into a GPU decision. One
fast proxy predicted that a 10-hour GPU run would pass; it failed. Twelve and a half hours later, a claim from the same
proxy family moved another run ahead in the GPU queue for four more hours. A separate agent then tested the proxy
directly: across candidates it had no predictive power for the final result (slope 0.17, 90% interval −0.70 to
+0.58). That is the clearest Goodhart case in the project, a metric that ranked well inside its own loop and was then
used outside it.

The knowledge base shows the same thing in miniature. Of 34 status changes, the only downgrades of findings were two
proxy results. No record ever went from "kill" back to "open" in the knowledge base; reopenings happened only in the
ledger.

### What predicts overclaiming

| factor | evidence | strength |
|---|---|---|
| Evidence class: proxy, model or early lead vs exact check | 14 of 20 overclaims; no deterministic exact-check claim was contradicted | strong |
| Close to the line, and the agent's own run | both failed "pass" calls were close to the line; all 6 optimistic bets were on the agent's own run | moderate (n = 10) |
| Time pressure: GPU idle and a next job wanted | the 12.5-hour repeat on the same proxy family | one case |
| Agent role: brainstorm and review vs production | the [M] overclaims came from brainstorm "lenses"; production threads mostly carry [L] | moderate |
| Which AI model | not recorded on ledger rows | **unknown** (rule 8 fixes this) |

Kills are the mirror image. Of 445 negative verdicts in the ledger, 46 rest on a model estimate alone and 89 carry no
evidence tag at all. The kills that were later overturned all had a scope that changed afterwards (a new pipeline,
higher precision, longer runs), not a wrong measurement.

## Notable incidents

- **Proxy to exact run.** The proxy said "pass", the 10-hour run said "fail" by a wide margin. The miss was recorded
  the same night and became a rule: a proxy may rank or veto a GPU job only after it has reproduced existing exact
  results. The system worked, one 10-hour run late.
- **A relayed instruction refused, correctly and quickly.** The coordinator agent relayed "switch your model to a
  different one, at maximum effort" to a research thread. 40 seconds later the thread asked Jeff to say it in his own
  words, and kept working meanwhile. Jeff wrote it, and the switch happened 33 seconds after that. Total cost: 2.5
  minutes. The same relayed plan reached a second thread five seconds later, and that thread switched without asking,
  because Jeff's own message was attached to the relay. Both readings are defensible, but two agents applied one rule
  two ways within a minute.
- **An unsourced incident inside the honesty study's own brief.** The coordinator's brief for this study mentioned an
  agent that had "owned up" to briefly grabbing the GPU. We found it nowhere: not in the threads, not in the GPU claim
  log, not in memory. We record it as unverified.
- **Honest hedging under an early lead.** In one long A/B test, an early gap kept shrinking. Each time, the agent wrote
  "I can't call it until the end", and a devil's-advocate agent pre-registered the bar before the result. This is the
  behaviour that was missing in the two early-lead overclaims.
- **Retractions done well.** Several ledger rows carry a bold "CORRECTION" next to their old verdict, or point to the
  author's own erratum.
- **Record conflict.** Two memory notes give different agent numbers for the same bet, and both say "I won". Only one
  can be true.

## Rules that make the agents more honest and more useful

The study proposed these. Rules 4 and 5 were adopted the same day; a pre-registration habit and the proxy gate
already existed. Rules 1, 3 and 4 also help the score.

1. **Pre-register every long run and every submission.** Before launch, write down the point prediction, its
   evidence class, the kill line and Jeff's bet. The agent that reads the result fills in the actual number.
2. **A proxy or model number carries its track record.** Next to a proxy-based prediction, state its measured bias so
   far, for example "optimistic on 3 of 3 exact runs; no ranking power".
3. **A kill states its scope and evidence in the verdict itself**, for example "dead at low precision, short fits
   [M]" instead of "dead". Kills resting only on a model, or untagged, are treated as soft when the pipeline changes.
4. **Price randomness as a distribution, not a point.** Every submission README gives the prediction at zero failures
   and at the expected number of failures.
5. **Close the loop after every upload.** Within a day, pull the leaderboard list, match by file size, and write the
   real score into the record.
6. **No decisions on early leads.** Report a lead together with how fast leads have decayed before. Decide at half
   the run or later, or at a pre-registered checkpoint.
7. **One source for each fact that matters.** Memory notes point to the record; they do not restate it. An incident
   without a source is marked unverified.
8. **Record which AI model and effort level produced each claim.** Without it, "which model overclaims" cannot be
   answered.
9. **One rule for relayed control requests** (switching model or effort, killing jobs, installing things). A relayed
   request counts only with the human's own message attached, and the agent names the message it acted on.

## Caveats

- Small numbers: 10 scored bets and 28 corrections. The corrections were found through the ledger's own vocabulary,
  so a silent error that nobody re-checked is invisible here. The real overclaim rate is probably higher than
  measured, not lower.
- The ledger parser and the coding of each correction are ours, and the coder was an AI agent from the same project.
  Nobody has re-coded them independently yet.
- Two of the underclaims were scoped correctly by their authors; the error was in how the next agent read them. We
  count them because the decision was delayed either way.
- Predictions for public-notebook rebuilds use reference costs implied by our own verifier receipts. They reproduce
  two leaderboard scores exactly, but an error of a few hundredths of a percent is possible on the others.
- The leaderboard shows the public score only. The final ranking draws the random samples again.
- What we left out: anything about how the circuits are built, absolute scores, and file hashes. The competition runs
  until January 2027. The full project, code included, is planned to go public after it ends.

## Data and code

| file | what |
|---|---|
| `data/uploads.csv` | every scored upload: date, kind, deviation from the written prediction (%) |
| `data/bets.csv` | pre-registered predictions: agent error, Jeff's error, pass/fail call and outcome |
| `data/corrected_claims.csv` | the 28 corrected claims in plain words, coded by direction and evidence |
| `scripts/summarize.py` | recomputes every number above (Python 3, standard library only) |

Text and data: CC BY 4.0. Code: MIT.
