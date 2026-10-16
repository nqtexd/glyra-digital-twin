# Glyra: research and implementation brief

Prepared 16 October 2026 for Sanjay P, Chennai Institute of Technology, AI & ML, graduating 2029. Solo software prototype.

## Problem and scope

A single glucose reading cannot explain a developing excursion. Glyra combines a synthetic health record with recent simulated continuous glucose readings and logged meals, then forecasts glucose 30–120 minutes ahead. The interface shows the forecast's uncertainty and refuses to forecast when readings are stale or insufficient. The initial user is a clinician reviewing a simulated patient. This is a research demonstration, with no dosing advice or claim of clinical validity.

## Evidence and implications

- The organiser requires a specific chronic condition, fusion of historical EHR and dynamic sensor data, a working prediction model, and a clinician dashboard. Synthetic data are explicitly permitted. Select type 2 diabetes; simulated CGM avoids hardware and patient-data access. [Digital Twin Challenge requirements](https://unstop.com/hackathons/crp-digital-twin-challenge-2026-happiest-health-1757873/amp)
- A1C averages can conceal short glucose excursions. Recent time-series context therefore matters. [ADA Clinical Diabetes, 2024](https://diabetesjournals.org/clinical/article/42/3/398/154390/Detection-and-Intervention-Use-of-Continuous)
- Long-range glucose forecasting remains difficult. Physiological models and meal information offer useful modelling ideas, but published type 1 diabetes findings cannot establish type 2 diabetes performance for this prototype. [Long-Term Glucose Forecasting, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6806292/)
- Published work studies combinations of daily activity and glucose signals. This supports investigating multimodal features, rather than assuming they guarantee improvement. [Neural Physiological Model](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373455/)
- A diabetes forecasting study separates participants between training, validation and testing to avoid leakage. Glyra uses separate synthetic people for training, interval calibration and testing. [Temporal and Behaviour-Aware Multimodal Modelling](https://pmc.ncbi.nlm.nih.gov/articles/PMC13119999/)

## Product differentiation hypothesis

The contribution is a transparent, locally executable review workflow: provenance for both streams, learned forecasts with separate calibration, visible persistence baseline, data-quality abstention, and replayable scenarios. This is an engineering and usability hypothesis, not a claim that glucose forecasting or uncertainty displays are new inventions.

## Alternatives

Persistence is the simplest baseline: future glucose equals the current reading. A trend line adds recent direction but may extrapolate badly. A learned regression can combine recent history with baseline physiology and known meal history. A full physiological simulator or neural model could be a later replacement after licensed real-world data and independent validation are available. A chatbot alone would not satisfy the working-model requirement.

## Planned implementation

1. Seeded synthetic generator with variable baselines, meal absorption, sleep, activity, sensor noise and unannounced future meals.
2. Ridge regression at four horizons; fixed training-only normalization; separate patient groups for calibration and test.
3. Absolute residual quantiles calibrated on a separate group. Intervals are pointwise and demonstrate synthetic benchmark behaviour only; they do not guarantee coverage for patients, a whole trajectory or scenario edits.
4. Browser-local inference with bundled model coefficients and fixtures. No API key, hardware or network inference dependency.
5. Patient list, longitudinal chart, EHR context, event log, data-quality report, replay, scenario comparison, local CSV import, and JSON review export.
6. Data-quality gates for missing, out-of-order, stale or invalid readings. An illustrative review threshold marks crossings; it is configurable and is not a diagnosis.

## Evaluation and adoption

Report actual MAE, RMSE, empirical interval coverage and persistence performance on held-out synthetic people. Publish seeds, splits, generator, model and benchmark output. Add missingness and malformed-input tests. Do not claim real clinical accuracy, validated intervention effects, hospital adoption, interviews, revenue or pilot results.

Potential next step: supervised usability review with clinicians, followed by independently collected, appropriately governed retrospective evaluation. Future commercial model: clinic subscription only after demonstrating usefulness and meeting applicable requirements. Pricing and adoption are unvalidated assumptions.

## Competition-specific packaging

Digital Twin: public repository; team/college information; project title, use case, stack, model, license; deck; architecture PDF/PPT; minimum 20-minute explanatory demo. Register by 18 October 2026 at 19:00 IST; code submission ends 20 October at 19:00 IST, according to listing checked today. The listing allows one-person teams but separately says two members travel; solo participation may need organiser clarification at finalist stage.

HACKS 2026: registration confirmed in Unstop UI. Online submission requires a PDF converted from a deck, covering problem, solution, innovation, approach, prototype, impact, scalability, business/sustainability, roadmap and team. Exact offline venue/date and any restrictions on prior code need final verification before attending or reusing code in the onsite build.

## AI disclosure

Codex assisted research, source code, design, documentation, decks and demo preparation. Sanjay must understand and be able to explain the work. Attribute libraries and research. Disclose reuse wherever requested and follow each event's build-window rules.
