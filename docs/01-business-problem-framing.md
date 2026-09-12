# 1. Business Problem Framing and Lens/Task Formulation

*Rubric: 5 marks — Foundational Knowledge; Integration | Problem framing; critical thinking*

## 1.1 Business context

Hotels accept bookings well in advance of arrival, but a large share of those bookings
are cancelled before check-in. Cancellations create uncertainty for staffing,
overbooking strategy, pricing, and revenue forecasting. In our dataset, **37.04%**
of all bookings (44,224 of 119,390) end in cancellation or no-show — this is not a
rare event, it is a routine operating condition the hotel has to manage.

## 1.2 Stakeholder

**Primary stakeholder:** Hotel Revenue / Reservations Manager, at both hotels
represented in the data (a City Hotel and a Resort Hotel).

**Secondary stakeholders:** Front-office / operations team (staffing and room
allocation), and hotel management (overbooking and cancellation-policy decisions).

## 1.3 Decision need

> Given the information available at (or shortly after) the time a booking is made,
> which bookings are at high risk of being cancelled, so that the reservations team
> can prioritise them for monitoring, confirmation follow-up, or revenue-management
> action (e.g. overbooking allowance, deposit policy) — **without** turning the score
> into an automatic punitive action against a guest.

## 1.4 Primary lens: Predictive

We frame this primarily as a **predictive** problem: build a model that estimates
the probability that a given booking will be cancelled, using information known at
or near booking time.

## 1.5 Secondary lens: Explanatory / descriptive

> Which booking characteristics are most strongly associated with cancellation, and
> can that association be explained in terms a non-technical reservations manager
> can act on?

This secondary lens is answered through EDA (`03-data-understanding.md`) and model
explainability (`06-evaluation-plan.md`), and is what turns a black-box score into
something a hotel can actually use operationally.

## 1.6 Unit of analysis

**One hotel booking** (one row in `hotel_bookings.csv`), not one guest and not one
stay-night. A returning guest can appear as several independent booking rows.

## 1.7 Task and exact output

- **Task type:** Supervised binary classification.
- **Target variable:** `is_canceled` (1 = cancelled or no-show, 0 = completed stay).
- **Exact output:** For each booking, a calibrated cancellation probability
  `P(is_canceled = 1)` in `[0, 1]`, plus a discrete risk tier (Low / Medium / High)
  derived from an operationally chosen threshold (see `06-evaluation-plan.md` §
  threshold analysis). The output is a **decision-support score**, not an automated
  accept/reject action.
- **Grain of prediction:** at booking level, using only fields that would realistically
  be known at or shortly after booking creation (see the leakage discussion in
  `03-data-understanding.md` and `04-preprocessing-feature-engineering.md`).

## 1.8 Rationale for this framing

- Cancellation prediction is a **routine, recurring** decision (every booking needs a
  score), unlike a one-off diagnostic question — this justifies a trained model over
  a single ad-hoc analysis.
- The target is directly present in the data (`is_canceled`), well-defined, and — as
  shown in `03-data-understanding.md` — is perfectly reconstructable from
  `reservation_status`, confirming it is a clean, unambiguous label.
- A probability + risk tier output (rather than a bare yes/no) matches how revenue
  managers actually work: they prioritise a ranked list under limited staff time,
  they don't need a hard binary verdict.
- We explicitly reject "prevent cancellations" as the business problem: the model
  cannot change guest behaviour, it can only inform which bookings deserve
  attention. This framing boundary is what prevents scope creep into an intervention
  model we do not have data to build (we don't observe what happens when a hotel
  intervenes on a flagged booking).

## 1.9 Success criteria (business, not just statistical)

A model is "successful" for this project if it:
1. Meaningfully outperforms the naive baseline (always-predict-majority-class,
   62.96% accuracy) on recall/precision/PR-AUC for the cancelled class, not just
   accuracy (see `06-evaluation-plan.md` for why accuracy alone is misleading here).
2. Uses only information available at prediction time (no leakage from
   `reservation_status` / `reservation_status_date`, see `04-preprocessing-feature-engineering.md`).
3. Produces a probability a manager can reasonably act on at some operational
   threshold, with the trade-off between false positives and false negatives made
   explicit rather than hidden inside a default 0.5 cutoff.
