# 7. Recommendation, Limitations, and Stakeholder Value

*Rubric: 10 marks. Integration; Human Dimension; Caring | Communication; human-centred AI*

This file is written from the final results of notebooks 11 to 14 (see
`06-evaluation-plan.md` for every number and its source table).

## 7.1 Recommendation

> The analysis shows that cancellation risk can be estimated using only information
> available **at booking time** (the day-zero variant). **XGBoost** gave the best
> ranking quality of the six models compared (CV PR-AUC 0.765, Test PR-AUC 0.774 vs
> 0.273 for a no-skill model), with Random Forest a close second
> (`06-evaluation-plan.md` §6.4). We recommend the reservations team use the
> calibrated output as a **3-tier risk score (Low / Medium / High)**, not a hard
> accept/reject decision, to focus limited staff time on the bookings most likely to
> cancel. On Test, the **High tier (score 0.35 or more) holds 32.5% of bookings but
> 77.8% of all cancellations**, and 65.3% of High bookings did cancel. The Low tier
> holds 52.2% of bookings with a 4.8% cancel rate. The main drivers of the score are
> the guest's country, lead time, booking agent, number of special requests and
> market segment.

Suggested use of each tier:

| Tier | Score | What staff do | Test evidence |
|---|---|---|---|
| High | 0.35 and above | Reconfirm the booking, offer flexible rebooking, include in overbooking allowance | 65.3% cancel; 77.8% of all cancellations |
| Medium | 0.18 to 0.35 | Watch; send a standard reminder closer to arrival | 23.2% cancel |
| Low | below 0.18 | No action | 4.8% cancel |

Under the illustrative costs in `06-evaluation-plan.md` §6.5, this policy lowers the
expected cost of cancellations by about 27.7% per 1,000 bookings (17,934 vs 24,792).
The hotel should replace those costs with its own before using this figure.

## 7.2 Stakeholder value

- **Reservations manager:** a ranked worklist instead of treating all bookings
  equally. Following up on about one booking in three (the High tier) reaches more
  than three out of four cancellations.
- **Revenue management:** a calibrated probability (expected calibration error 0.007)
  that can be summed over a night's bookings to estimate expected cancellations, an
  evidence-based input to overbooking and deposit-policy decisions.
- **Front office / operations:** earlier visibility into likely cancellations supports
  staffing and room-allocation planning.
- **Where it helps least:** Direct and Corporate bookings. The model catches only 32%
  and 43% of their cancellations, so staff should not assume a Low score is safe for
  those segments.

## 7.3 Limitations

- **Historical, not current data, and the model drifts.** Bookings span 2015-2017
  for two specific hotels. The temporal check in notebook 14 shows the cost of time:
  trained on 2015-2016 and tested on 2017, PR-AUC falls from 0.774 to 0.650 and recall
  from 0.778 to 0.519, because the cancel rate rose from about 25% to 32%. In use, the
  model must be retrained regularly (for example every quarter) and its threshold
  re-checked on recent bookings. The 0.774 Test score is only valid for bookings like
  the training period.
- **Two hotels only.** One City Hotel, one Resort Hotel, findings may not
  transfer to hotels of a different size, market, or region.
- **No causal claims.** Associations found (e.g. `country`, `deposit_type`, prior
  cancellations) are *correlational*. In particular, the `Non Refund` →
  cancellation relationship (99.36% raw, 94.59% after de-duplication, §3.5) is almost certainly confounded by
  booking channel/process, not a simple causal effect of the deposit policy
  itself; this must not be reported as "changing deposit policy will change
  cancellation rates" without further evidence.
- **Missing real-world variables.** No data on price competitiveness, weather,
  local events, guest income, or actual reason for cancellation; the model can
  only use what's in this table.
- **Errors are inevitable.** At the 0.35 threshold on Test, 1,474 of 4,248 flagged
  bookings (35%) did not cancel, and 791 of 3,565 cancellations (22%) were missed.
  Errors are uneven: Direct and Corporate bookings are mostly missed.
- **Close race between the top two models.** XGBoost beat Random Forest by only
  0.0065 CV PR-AUC (p = 0.054). Either would serve; XGBoost was picked by a fixed
  rule, not because it is clearly better.
- **Explanations are global only.** SHAP was not run (`shap` was not installed), so
  per-booking explanations are not yet available. Permutation importance gives the
  global drivers.
- **Threshold is a business judgement, not a statistical fact.** The 0.35 threshold
  rests on an illustrative cost assumption (a missed cancellation costs about 1.8
  times a false alarm). It holds for ratios from 1.5 to 2.0; outside that range it
  moves (0.52 at 1.0, 0.25 at 3.0). The hotel should confirm the costs.

## 7.4 Risks and responsible-use guardrails

- **Fairness:** `country` is the single most important feature, and the audit in
  `06-evaluation-plan.md` §6.6 flagged 8 of 11 country groups. Portuguese bookings
  get 1.36 times the average false alarm rate; Dutch and Belgian bookings have their
  cancellations missed more often (recall about 0.57 to 0.58 vs 0.77 overall). The
  score must never be used to treat guests differently by nationality (for example
  stricter deposits or worse rates). Actions on a High score should be the same
  helpful contact for every guest. A version without `country` should be tested
  before any real use, to see how much accuracy it costs.
- **Transparency:** front-office staff should be able to see the top factors
  behind a given booking's score, not just a bare number. This needs per-booking
  SHAP explanations, which are the next step (install `shap` and re-run notebook 13).
- **Human oversight:** the score supports a human decision (follow-up call,
  monitoring); it must not automatically cancel, upcharge, or deny a booking.
- **Privacy:** the public dataset already has guest-identifying information
  removed; a real deployment on live guest data would need its own data-governance
  and consent review, which is out of scope for this academic project but is
  flagged here so it isn't silently assumed away.
