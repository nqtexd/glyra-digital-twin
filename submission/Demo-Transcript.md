# Glyra narrated demonstration

AI-assisted presentation; synthetic narration; all patient data and metrics are synthetic.

## 01. Introduction

Welcome to this walkthrough of Glyra, a glucose digital twin research prototype. The project combines a synthetic health record with a simulated continuous glucose stream, then produces forecasts with visible uncertainty. Sanjay P is the solo participant, studying Artificial Intelligence and Machine Learning at Chennai Institute of Technology and graduating in 2029. Codex assisted the research, implementation, design, testing and preparation of this narrated presentation. The narration uses a synthetic voice.

The central question is practical: what would a reviewer need to understand a developing glucose excursion without reconstructing context across separate screens? Glyra puts recent readings, a small health record, already logged meals, model forecasts and data quality in one workspace. It includes working inference, rather than a static dashboard or a chatbot that invents predictions. The model and fixtures ship with the application, so inference can run on the viewer's device without an API credential.

Every person and every measurement in this demonstration is synthetic. The model has no real patient validation and provides no diagnosis, medication advice or insulin dosing. The numerical results describe performance inside the supplied simulator only. Throughout the walkthrough, the distinction between a working engineering demonstration and evidence of clinical usefulness remains explicit. The repository includes the generator, learned coefficients, benchmark, tests, architecture, deck and research notes so an evaluator can inspect the implementation independently.

## 02. Problem and scope

The review problem begins with a limitation of a single measurement. Two people can have the same current glucose value while their recent trajectories differ. One may be rising after a logged meal; another may be returning toward a baseline. A useful review screen should preserve that temporal context instead of replacing it with one unexplained risk label.

The research brief references an American Diabetes Association article explaining that an A one C average can conceal shorter excursions. It also references published work on longer glucose forecasts. That literature motivates investigating meal history and patient context, while warning that predictions beyond an hour are difficult. Some of the cited forecasting studies concern type one diabetes. Their findings do not validate this type two synthetic prototype, and Glyra makes no such transfer claim.

The selected use case is deliberately narrow: a reviewer explores simulated glucose thirty to one hundred and twenty minutes ahead for a synthetic person with type two diabetes. The interface can mark whether a forecast point crosses an illustrative review threshold. It does not diagnose an adverse event or tell someone to change treatment. The intended contribution is an inspectable workflow: show where inputs came from, show what the model actually computes, expose uncertainty, and withhold a forecast when the input window is incompatible. Whether that workflow saves clinician time is a hypothesis for later usability testing, not an outcome already demonstrated.

## 03. Dashboard walkthrough

This is a screenshot of the working application, captured from the local build. The overview contains three synthetic people in the left sidebar. Selecting a person changes the health record, sensor history, logged meals and forecast. The page header identifies the record as synthetic. The initial example is Ananya, a demo identity attached to synthetic person one hundred and twenty six.

The summary row shows current glucose, the forecast at two hours, the largest of the four forecast points, and the first point that crosses the illustrative threshold. These numbers come from the inference engine. They are not fixed presentation values. Below them, the trajectory chart places observed readings to the left of the vertical now marker and forecasts to the right. A shaded band represents the calibrated pointwise interval. A faint horizontal line shows the persistence reference. The amber line is the configurable review threshold.

The replay slider moves the current point through the synthetic record. At each position, the engine recomputes features from the preceding hour and meals logged up to that time. The play control advances the same cursor automatically. A one-hour or two-hour selector changes the visible forecast horizon. The patient context panel supplies the historical stream. Recent events identify the meal logs and sensor sync. Finally, export review downloads a JSON record containing model identity, synthetic provenance, current context, forecast, threshold and limitations. It does not silently send a clinical decision anywhere.

## 04. Architecture

The architecture separates offline model development from runtime inference. On the left are the two input streams. The synthetic health record supplies fasting baseline, A one C, age, previous sleep and an activity index. The dynamic stream supplies five-minute glucose values and the meal events that have already been logged. The arrows show these streams entering the data-quality gate.

Before prediction, the gate checks that there are enough readings, their timestamps are ordered, their spacing is compatible, the latest measurement is fresh, and both readings and record fields fall within supported ranges. If a check fails, the engine returns reasons and an empty forecast array. The interface then shows forecast withheld instead of producing apparently precise numbers from unusable inputs.

When the gate passes, a feature function creates sixteen values. The browser applies normalization learned from training people and four sets of ridge regression coefficients. Each regression head produces one horizon. Separate residual quantiles provide the interval half widths. The dashboard visualizes these outputs and can export a review record.

There is no inference server or hidden language-model call in this path. The bundled model, benchmark and synthetic fixtures are ordinary JSON files. Offline, the Python training script generates the population, fits the regressions, calibrates intervals and writes those files. Runtime JavaScript mirrors the feature calculations. A parity test verifies that the same example produces matching predictions in training and browser inference.

## 05. Generator and training

The generator creates one hundred and fifty synthetic people, with four simulated days for each person. One hundred people belong to training, twenty five to interval calibration, and twenty five to testing. The groups do not overlap. There are eighteen thousand four hundred training windows, four thousand six hundred calibration windows and four thousand six hundred test windows, for twenty seven thousand six hundred windows in total.

Each synthetic person has a baseline and a different meal-response gain. Meal times and carbohydrate amounts vary. The glucose trace combines meal absorption, a circadian component, sleep and activity terms, correlated drift and sensor noise. The generator seed is four thousand one hundred plus the person identifier. This makes the exact benchmark reproducible. It remains a simplified mathematical generator, not a clinically validated physiological simulator.

The features include the current reading, recent mean, recent change, variability, the record fields, clock phase, and decaying contributions from already logged meals. Future meals are excluded even though they exist later in the fixture. Four regression heads predict thirty, sixty, ninety and one hundred and twenty minutes ahead. Training-only means and standard deviations standardize the inputs. The ridge penalty is eight and the intercept remains unpenalized.

This is intentionally a transparent baseline model. The fixed penalty was not selected by repeatedly inspecting the test group. More complicated models could be compared later, but model complexity alone would not fix the absence of real-world validation or make an unannounced future meal observable.

## 06. Evaluation

The benchmark compares Glyra with persistence, which predicts that the future value will equal the current reading. This is a useful baseline because a forecast should justify its complexity against a simple alternative. The displayed values come directly from the generated benchmark JSON.

At thirty minutes, Glyra's mean absolute error is six point four eight milligrams per deciliter, compared with ten point three five for persistence. At sixty minutes, the values are thirteen point five three and eighteen point four eight. At ninety minutes, they are eighteen point zero three and twenty five point zero nine. At one hundred and twenty minutes, Glyra records nineteen point six four, compared with twenty nine point seven nine for persistence. The two-hour root mean squared error is twenty five point three eight, which reflects the influence of larger errors.

For the nominal ninety percent pointwise intervals, empirical coverage on the held-out synthetic test windows is about ninety percent at every horizon. At two hours it is eighty nine point eight percent. This does not mean that a real patient's entire future trajectory has a ninety percent guarantee. The windows are correlated within people, the generator simplifies biology, and deployment data could differ substantially.

The test people were not used for training or interval calibration. That separation is meaningful evidence of synthetic generalization, but its scope must remain clear. The benchmark demonstrates that the supplied pipeline runs, compares against a baseline, and reports its limitations. It does not establish clinical accuracy or treatment benefit.

## 07. Data provenance and import

Both input streams have explicit provenance. The health record is labelled synthetic and identifies the fields used by inference. The glucose stream consists of minute indexes and measured values. Meal records include their time, carbohydrate amount and a descriptive label. The model only sees meals whose timestamps precede or equal the replay cursor.

The Data Studio allows a reviewer to inspect the most recent readings at that cursor. It can download the full current series as CSV. A local import accepts the exact header minute comma glucose, with at least thirteen rows in increasing five-minute intervals. It rejects nonnumeric entries, duplicate timestamps, missing values, irregular intervals and readings outside the supported range. The import is limited to five thousand rows and five hundred kilobytes.

Imported readings remain in browser memory. They disappear on reload. There is no upload endpoint for these readings, and the application does not infer meal events from a CSV. Importantly, the imported series pairs with the currently selected demo health record. That pairing is visible and must not be mistaken for a validated real patient twin. Only synthetic or appropriately anonymized data should be used for experimentation.

The design gives an evaluator a practical way to probe the data contract. They can download a valid fixture, inspect it, try an invalid row and observe the rejection. They can also restore the seeded fixtures. Keeping these operations local makes the demonstration reproducible without requiring sensor hardware, external patient access or inference-service credentials.

## 08. Withholding a forecast

The application includes explicit demonstrations of missing and stale data. In the shown example, a simulated missing reading causes the forecast to disappear. The summary cards use dashes for unavailable forecasts, the twin status changes, and the chart area explains the failed check. The observed current value remains visible as part of the record, but the model does not fill the forecast with a made-up substitute.

The recent window normally contains thirteen samples over sixty minutes. The gate checks the count, finite glucose values, ordering and compatible spacing. It also checks the latest reading's age against the current replay time. The stale-sensor demonstration advances the assessment clock by twenty five minutes without pretending a new sensor measurement arrived. That causes the freshness check to fail.

Record fields have supported ranges because the model was trained on a bounded generator. A record far outside those bounds should not silently receive an apparently trustworthy forecast. The engine returns understandable reasons, and the same logic serves the dashboard and exported review. Tests cover invalid values, out-of-order timestamps, insufficient history, stale inputs and unsupported record values.

These checks establish compatibility with the prototype's assumptions. They are not a complete clinical safety system. For example, they do not establish that a plausible sensor reading is accurate, detect every distribution shift, or prove that a reviewer will interpret an interval correctly. Those limitations are part of the model card and research roadmap.

## 09. Scenario comparison

The scenario dialog illustrates model sensitivity while preserving the original record. A reviewer can move the sleep or activity slider and see how the two-hour prediction changes while glucose history stays fixed. The interface presents the original forecast, edited forecast and numerical difference together. Closing the dialog leaves the underlying demo patient unchanged.

This interaction is useful for explaining that the historical record contributes to the model, rather than serving as decorative context beside an unrelated chart. It also exposes a boundary that matters in health applications. Changing an input to a predictive model is not equivalent to performing an intervention on a person. If a slider change lowers a prediction, that does not prove that the same behavioural change would produce that glucose reduction in a patient.

The synthetic generator explicitly includes sleep and activity terms. A regression can learn their associations inside that constructed world. Human physiology has confounding factors, treatment history and measurement processes that this generator does not represent. The dialog therefore labels the comparison exploratory and gives it no treatment interpretation.

The interval calibration also belongs to the original simulated distribution. It does not guarantee coverage for arbitrary edited records. The application states that limitation next to the controls. This makes the scenario feature an inspectable modelling tool, rather than an unsupported recommendation engine. A future clinical study would need a different design and evidence before making claims about intervention effects.

## 10. Limitations and failure cases

The most important failure case is an unobserved future event. A person may eat a meal after the forecast begins without logging it in advance. The target glucose series then changes, even though the model's input history contains no information about that meal. Glyra's generator includes this situation. It is one reason long-horizon errors grow and uncertainty bands widen.

The test results also vary across synthetic people. At two hours, mean absolute error by person ranges from twelve point two one to twenty six point four three milligrams per deciliter. Reporting an overall mean should not hide that variation. The source benchmark includes the range, error measures, baseline and interval coverage so reviewers can inspect more than a single favourable number.

Other limitations follow from the prototype's scope. The generator omits many physiological processes. The data contain no actual people, devices or clinical workflows. Overlapping windows create within-person dependence. A pointwise marginal interval does not guarantee simultaneous coverage of the plotted trajectory, and an unfamiliar real population could have a very different error distribution.

The project therefore claims a working, reproducible engineering pipeline with a clear review interface. It does not claim regulatory readiness, hospital deployment, validated alarms or improved health outcomes. The next credible evidence would come from an independently governed retrospective dataset and clinician usability review. Those studies should test external performance, subgroup behaviour, missingness, calibration and human interpretation before anyone considers clinical use.

## 11. Impact and roadmap

Glyra's intended practical value is to reduce the effort of reconstructing a patient's recent context across separate views. The proposed workflow brings the relevant history beside the forecast and makes the system's limits visible at the moment of review. Whether this improves review time or decision quality remains a hypothesis. No clinician interviews, hospital pilot, adoption or commercial revenue are claimed.

A feasible next step is a supervised usability study using synthetic cases. Reviewers could compare the interface with a simpler baseline, explain what they infer from the uncertainty band, and identify confusing language or missing context. The study should measure task completion and interpretation, not merely ask whether the dashboard looks attractive.

Independent retrospective evaluation would follow only with suitable data access and governance. It should preserve person-level separation, specify horizons and metrics in advance, compare strong baselines and examine subgroup errors. A supervised research pilot would depend on the results and appropriate partners. The current prototype offers a starting point for that work, not a substitute for it.

The commercial idea is a possible clinic subscription after validation. Pricing, demand and economic benefit are untested. Technically, browser-local inference keeps the initial demonstration inexpensive to run: there are no recurring language-model calls, no required sensor purchase and no secret API key. Future infrastructure choices should follow actual workflow and evidence needs. The roadmap prioritizes validation before expanding the model's clinical claims or adding automatic actions.

## 12. Reproducibility and closing

The repository is organized so an evaluator can reproduce the core work. The browser application lives in the dist folder. The engine module contains feature construction, prediction, quality gates and CSV validation. The Python training script generates the population, fits the model, calibrates intervals and exports fixtures and results. Model coefficients and benchmark JSON files are committed so the demonstration also runs without retraining.

The test suite verifies agreement between Python-generated inference values and JavaScript predictions. It checks that changing future readings or future meal logs cannot leak information into a forecast. It exercises withholding behaviour and malformed CSV input, and checks that training, calibration and testing people remain disjoint. Separate browser checks exercise desktop and mobile views, the scenario dialog, missing-data behaviour, evidence screen and Data Studio.

The presentation and architecture diagram accompany the source in editable PowerPoint and PDF formats. The license is MIT. Research references and their practical implications appear in the research brief, with source links in the relevant slide notes. Codex assistance is disclosed. Sanjay should review the implementation and be ready to explain the modelling choices, data assumptions, benchmark and limitations during any live evaluation.

Glyra demonstrates a specific principle: a forecast becomes easier to assess when the interface exposes its inputs, baseline, uncertainty and failure conditions. The project provides a functioning software prototype of that principle, with synthetic evidence and an explicit route toward stronger validation. Thank you for reviewing the work.