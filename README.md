# Glyra

A glucose digital twin research prototype that combines a synthetic health record with recent simulated continuous glucose measurements and logged meals. Glyra produces learned 30–120 minute forecasts, shows pointwise uncertainty, and withholds forecasts when the input window fails data-quality checks.

**Research demonstration only. All included people, measurements and benchmark results are synthetic. No real patient validation, diagnosis, medication or dosing advice.**

## Team and college

- Participant: **Sanjay P**, solo team **sanjaytenn11**
- College: **Chennai Institute of Technology**, India
- Course: **Artificial Intelligence and Machine Learning**
- Graduation year: **2029**

## Problem statement and healthcare use case

A single glucose value omits recent dynamics and record context. A reviewer needs to see the recent trajectory, already logged events, forecast uncertainty and whether inputs are trustworthy enough for inference. Glyra implements that review workflow for a synthetic type 2 diabetes use case. Intended practical usefulness remains a hypothesis for later usability testing.

## Run the prototype

Install Node.js 20 or later, clone this repository, then run:

```sh
npm start
```

Open **http://127.0.0.1:4173**. There are no runtime npm dependencies, API credentials or hardware requirements. A static HTTP host can also serve `dist/` directly. Open the page through HTTP; opening `index.html` as a local file does not reliably permit fetching model JSON.

## Working features

- Three synthetic patient records with independently computed forecasts.
- Observed glucose, four forecast horizons, persistence reference and calibrated pointwise interval.
- Replay slider and automatic replay; future readings and future meal events never enter model features.
- Historical record context and timestamped synthetic meal log.
- Exploratory sleep/activity sensitivity comparison, explicitly separated from treatment or causal claims.
- Missing/stale-data demonstrations that withhold forecasts.
- Local CSV import with validation, source inspection, fixture restore and CSV export.
- JSON review export including model version, synthetic provenance and limitations.
- Responsive desktop/mobile interface, dark appearance and reduced-motion support.

## Technical stack and model

Frontend: HTML, CSS and JavaScript ES modules. Inference: browser-local matrix computation. Local preview server: Node.js built-in HTTP/file modules. Training: Python with NumPy. Presentation: editable PowerPoint, with PDF counterparts.

`train.py` generates **150 synthetic people**, four days each. IDs 1–100 train the model; IDs 101–125 calibrate intervals; IDs 126–150 form the held-out test cohort. The seed is `4100 + person id`.

Sixteen features combine recent glucose statistics, clock phase, record context and contributions from already logged meals. Training-only means/standard deviations normalize features. Four ridge regression heads use a fixed penalty of 8 with an unpenalized intercept. Separate absolute residual quantiles provide nominal 90% pointwise intervals. The test people do not train either the coefficients or interval quantiles.

## Reproduce training and tests

```sh
python -m pip install numpy
python train.py
npm test
```

The generated coefficients, fixtures and benchmark are committed in `dist/data/`, so retraining is optional for running the UI. Training produces 18,400 train windows, 4,600 calibration windows and 4,600 test windows.

| Horizon | Glyra MAE, mg/dL | Persistence MAE, mg/dL | RMSE, mg/dL | Empirical interval coverage |
|---|---:|---:|---:|---:|
| 30 min | 6.48 | 10.35 | 12.56 | 90.0% |
| 60 min | 13.53 | 18.48 | 21.14 | 89.9% |
| 90 min | 18.03 | 25.09 | 24.66 | 89.9% |
| 120 min | 19.64 | 29.79 | 25.38 | 89.8% |

These are **synthetic-only results** from `dist/data/benchmark.json`. Windows within a person are dependent. Intervals do not guarantee coverage for real patients, entire trajectories or edited scenarios. Unannounced future meals can cause large errors. This generator is not a validated physiological simulator.

The tests verify Python/JavaScript inference parity, exclusion of future information, forecast withholding, patient-disjoint splits and invalid CSV rejection. Desktop/mobile browser QA additionally exercises navigation, scenarios, data-quality failure and the evidence screen.

## Presentations, architecture and demonstration

- [Project presentation (PDF)](submission/Glyra-Project.pdf)
- [Editable project presentation (PowerPoint)](submission/Glyra-Project.pptx)
- [Architecture diagram (PDF)](submission/Glyra-Architecture.pdf)
- [Editable architecture diagram (PowerPoint)](submission/Glyra-Architecture.pptx)
- [20-minute narrated walkthrough (MP4)](submission/Glyra-Demo-20min.mp4)
- [Demo transcript](submission/Demo-Transcript.md)
- [Chapter timings](submission/Demo-Chapters.json)

**[Unlisted YouTube demonstration](https://youtu.be/yjmeaV-YoaI)** — uploaded 16 October 2026; YouTube displays 20:01 and confirms unlisted visibility. The video is a narrated presentation with screenshots of the working prototype.

## Data contract and limitations

CSV header: `minute,glucose`. Require at least 13 ordered readings, exact five-minute intervals, finite values in 40–400 mg/dL, no duplicates, at most 5,000 rows and 500 KB. Imports remain in browser memory and pair with the current synthetic record. No meal log is inferred. This pairing is unsupported for real physiology.

Input gates check compatibility and freshness; they do not establish clinical safety. No real clinician interviews, pilot, hospital deployment, adoption, revenue, economic saving or treatment benefit has been demonstrated. Next steps would require independent retrospective validation, appropriately governed data and clinician usability review.

## Research, originality and AI disclosure

[RESEARCH.md](RESEARCH.md) explains the evidence, alternatives, project scope and design rationale. Sources include [ADA Clinical Diabetes](https://diabetesjournals.org/clinical/article/42/3/398/154390/Detection-and-Intervention-Use-of-Continuous), [long-term physiological glucose forecasting](https://pmc.ncbi.nlm.nih.gov/articles/PMC6806292/), [multimodal physiological encoding](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373455/), and [participant-level evaluation splits](https://pmc.ncbi.nlm.nih.gov/articles/PMC13119999/). Published type 1 diabetes findings do not validate this type 2 synthetic demonstration.

Codex assisted research, code, visual design, tests, documentation, presentations and demonstration preparation. Narration uses a synthetic voice. This submission does not claim unaided authorship. Sanjay must understand and explain the work during evaluation. Reuse and third-party tools should be disclosed wherever an event requests them; onsite build-window rules still apply.

## Open-source license

Project code and original documentation: **MIT**, see [LICENSE](LICENSE). Browser and Node platform APIs require no distributed library. Retraining uses NumPy under its BSD license. Google Fonts serves DM Sans and Manrope under their respective open font licenses; the UI falls back to system fonts when offline. Presentation screenshots show this prototype. Source research remains the property of its respective authors.
