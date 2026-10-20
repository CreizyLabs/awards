# How to participate and claim a reward through MathDB

[Home](../README.md) · [Pilot problems](../problems/mathdb-pilot.md) · [Legacy process](award-process.md)

Rules version: **mathdb**. This is the new process for the 49 problems in the
[pilot register](../problems/mathdb-pilot.md). Other problems continue under the
legacy process until their migration is announced. We recommend the new process
for participating problems and intend to extend it to the remaining problem bank.
Adding a MathDB link alone does not migrate a problem.

This repository change prepares the pilot. Formal automatic claims begin after
activation is announced and the official MathDB account is configured. The
[pilot page](../problems/mathdb-pilot.md) records rollout and any unresolved scope;
resolve those questions before automatic handoff for the affected problem.

Problem levels and estimated rewards are not recorded in this repository.

## Contributions and conditions

| Category | Share of the formally announced problem reward | Required evidence |
| --- | --- | --- |
| Solution | 50% | Complete mathematical solution of the original problem, accepted mathematical review, original public date and earliest-valid-contributor evidence. |
| Lean | 30% | Complete formalization of the original problem, corresponding mathematical solution, fixed proof version, verification, original public date and earliest-valid-contributor evidence. |
| Exposition | 20% | Reviewed video, article or other explanation, and a committee decision identifying the first contributor whose exposition satisfies the committee. |

Each category is reviewed, recorded and publicly reviewed separately. These are
category shares, not a reward for every upload or every person whose materials
pass a technical check. The team confirms the applicable formally announced
reward and any joint-author allocation; the catalog supplies no reward estimate.

The [problem index](../problems/README.md#mathdb-pilot-claim-status-columns) shows
independent Solution (under Solver) and Lean registration states; the
[pilot page](../problems/mathdb-pilot.md#pilot-register) also shows Exposition:
blank when no record is published, otherwise `Candidate` or `Awarded`. They summarize the public registers,
not technical acceptance, committee selection, pending claim issues or payment.
Exposition is not gated by a Solved/Lean flag; its own review and committee
selection remain required.

Solution and Lean each require their own complete original result to have become
public **after 2026-01-01**, and the claimant to be the earliest valid contributor
for that problem and category. Compare independently verifiable public history,
including earlier results before the cutoff. Re-uploading, re-verifying or opening
a new issue does not change a result's date or priority. A record stating only
2026-01-01, an uncertain timezone or an unresolved priority conflict goes to the
team for clarification; the agent must not infer qualification.

The cutoff is not automatically applied to Exposition. Content approval or the
earliest upload cannot replace the committee's decision, date and selected version.
Expositions may explain an open problem, but must distinguish proved statements
from unresolved claims and identify citations and original contributions.

## 1. Select the problem and submit to MathDB

Use the JSP entry and its confirmed MathDB link. Check the exact statement, field,
dimension, hypotheses and conclusion. Report a missing or incorrect mapping using
the [correction form](../.github/ISSUE_TEMPLATE/correction.yml); resolve it before
automatic handoff.

Links display no status prefix. The [scope notes](../problems/mathdb-pilot.md#scope-notes)
and catalog metadata record unresolved formulations and page-statement issues;
`Matching page pending` means a full corresponding page has not been located.
These are independent of reward-candidate status. The notes also record related
and alternative pages for review. They do not change the approved formulation by
themselves. In particular, resolve the conflicting P=NP/P!=NP page statements
before automatic handoff, and do not substitute a non-effective Vojta bound for
the selected effective-Mordell problem. JSP-001050 links to the algorithmic form
at [MathDB #332964](https://mathdb.com/p/332964/algorithmic-mordell-conjecture):
compute all points on any genus-at-least-two curve over a number field or finite
extension. This supplies an effective height bound for each input but does not
prescribe linear or polynomial uniform dependence; a stronger quantitative
formulation requires an explicit scope decision.

Submit the relevant materials through MathDB's available submission entry point:

- **Solution:** proof or publication, fixed version, theorem/pages, authors and
  contributions, statement correspondence and original public-history evidence.
- **Lean:** original repository, branch and full 40-character commit SHA, proof
  files and target theorems, toolchain and dependencies, reproduction instructions,
  statement correspondence, axiom audit and corresponding mathematical solution.
- **Exposition:** stable material link, fixed version and publication date, authors,
  topic, cited sources and the reviewed content.

Only a complete solution and a complete Lean proof qualify in their categories.
A target proof must not depend on `sorry`, `admit` or additional unproved
assumptions replacing missing steps. A successful build alone is insufficient.
Uploading someone else's work does not make the uploader the contributor.

**The pilot does not require a proof-submission PR or a merged PR before claiming.**
PRs may still maintain public catalog records; they are not an application gate
for this version. Legacy PRs and earlier submissions remain relevant evidence.

## 2. Review and check reward conditions

MathDB reviews the mathematical solution, verifies Lean and original-problem
coverage, and reviews exposition content. The committee separately selects the
first satisfactory exposition. Each conclusion must identify the actual author,
category, exact material version, scope, UTC date and a report or team-checkable
record. A public page saying "claimed solved", community approval or an author
assertion is not a final accepted review.

MathDB may verify and adopt an existing external Lean verification record rather
than always rebuilding. Adoption must explicitly identify the original repository,
fixed proof version, full problem coverage, completeness and external evidence.
An existing "Lean proof: Yes" catalog flag alone is not adoption.

The agent also checks the date and priority evidence for Solution/Lean or the
committee decision for Exposition. Missing or uncertain evidence pauses only the
affected category. No formal automatic claim or successful-claim notification is
sent for that category until these checks pass.

## 3. Agent claim and personal confirmation

The official MathDB agent creates or updates a **Claim Reward** issue after the
category's technical and reward-condition checks pass. The agent hands off
materials; the actual contributor remains the claimant and potential recipient.
A GitHub account is optional for initial handoff: a stable public MathDB identity
can identify the claimant.

Use one issue per **JSP + actual claimant**, adding later qualifying categories to
the same issue. Search open and closed claims, historical PRs, candidates, awards
and disputes. Keep coauthors' and competing claims linked. Preserve applicant
statements and team decisions; append updates without overwriting them.

After creating or updating the issue, the agent sends a notification from MathDB's
official mailbox to the contributor, with Cc and Reply-To set to
**thejustinsunprize@hejustinsun.com**. It includes the issue, passed categories,
versions, verification and qualification evidence, and required personal response.
Issue creation and notification are separate recoverable tasks: a mail failure
must not create another issue or be described as delivery.

The claimant personally replies to the prize mailbox, links the issue, confirms
their contribution and intention to claim, discloses collaborators and supplies
an independently verifiable identity method. After the team determines the
proposed categories, reward and public attribution, the claimant confirms those
terms again in writing. The agent cannot sign either response or receive payment.

The team independently reviews qualification, priority, attribution, duplicates,
the committee decision and applicable reward. An issue or email does not approve
an award. See the [agent contract](../agent-scope.md) and
[issue template](templates/mathdb-claim-reward.md).

## 4. Public review for each category

Administrators publish accepted categories in the
[candidate register](../candidates/README.md#mathdb-pilot-candidates), linking the
claim, MathDB problem, fixed material and verification/committee evidence. Record
explicit UTC start and scheduled end, separated by 14 full days, and the rule
version. Public review starts at the category's actual candidate publication,
not at submission, verification, issue creation, email or a historical PR merge.

**An accepted Solution may be claimed and publicly reviewed before complete Lean
evidence is available.** After its review ends it remains waiting for that payment
condition. Complete Lean evidence can come from MathDB verification or explicit
adoption of external records, and the formalizer need not claim or receive an
award first. Lean and Exposition do not wait for a solver to register a claim.

Identity checks may proceed during public review. Use an authorized public account
or candidate identifier while identity is pending. Every recipient must complete
identity verification and personal written confirmation before announcement.

Submit objections through the [formal dispute form](../.github/ISSUE_TEMPLATE/dispute.yml).
MathDB handles technical/content re-review; the prize team resolves attribution,
priority, qualification and reward issues. Hold affected categories while material
objections are unresolved. A successful replacement or substantive version or
recipient change requires review and a fresh 14-day notice for the affected
category. Ordinary text corrections and migration of an unchanged record do not
restart its clock. An unsuccessful objection preserves the original start.

## 5. Announcement and payment

After public review, the team checks current technical/committee conclusions,
original date and priority, resolved objections and related pending submissions,
identity, personal confirmations and the applicable payment conditions. Solution
payment additionally requires valid complete Lean evidence for that problem.

Publish the confirmed category in the
[award register](../awards/README.md#mathdb-pilot-awards), retain its completed
public-review dates, evidence and claim links, and update the candidate record.
Keep other categories pending as appropriate. Record **announced / awaiting
payment** separately from **paid**; only a team-confirmed payment result permits
the latter. Closing an issue or reaching the review end is not payment evidence.

If verification, external adoption or a committee decision is withdrawn or its
scope reduced, the agent updates affected claims and notifies the contributors
and team. Loss of complete Lean evidence also holds related Solution payments.
The team handles corrections or revocation of previously announced or paid awards
and preserves their history.

## Private information and transition

Send private identity evidence, email addresses, payment details and delivery
information only through the official email channel or controlled systems. Do not
include them in public GitHub issues or MathDB pages. MathDB notifications identify
MathDB as sender; official prize-team mail comes from **@hejustinsun.com**. The team
never asks for private keys or seed phrases.

Retain the [legacy process](award-process.md), old claims, PRs, public-review dates
and awards. For a migrated pending application, record both rule versions and an
explicit team transition decision in its existing claim. MathDB may adopt prior
verification, but its new upload/adoption date does not replace original dates.
Unchanged candidates retain their existing public-review clock. Previously
announced or paid awards are not automatically recalculated using new shares.

Future expansion updates the approved register and mapping, announces the
effective rule version/time and states how existing applications transition.
Until that happens, problems outside the register continue under the legacy rules.
