# The Taobao Effect — analysis

Reproducible price comparisons and illustrative monthly budgets for Chengdu and Houston. Research inputs were frozen on 24 September 2026; numerical and PPP review on 27 September 2026. Prices mix dated 2025–26 offers and estimates, not a simultaneous live market survey.

## Read or reproduce

- [Article appendix](article/appendix.md), ready to adapt for Substack.
- [Raw LaTeX blocks](article/latex-blocks.txt). In Substack use **More → LaTeX**, insert each formula, and preview. Pasting Markdown dollar-sign delimiters into ordinary prose does not guarantee equation rendering. [Substack instructions](https://support.substack.com/hc/en-us/articles/12291042958996-How-do-I-add-equations-to-my-Substack-post).
- [Excel workbook](workbooks/local-life-budget.xlsx): download to use the formulas.
- [Source notes](data/source-notes.csv) and [source link index](data/sources.csv).
- [Monthly contribution ledger](results/default-monthly-contributions.csv) and [all results](results/analysis.json).

Python 3.9 or later; no packages or network access required:

```sh
python3 analysis.py
```

The script reproduces four budgets and checks them, catalogue statistics, lifetime cases and joint price stress tests against the saved original workbook results. It also checks that category weights reproduce the total ratio. It writes the two files in `results/`. The reference checks deliberately fail if you change the inputs without also revising the expected results. For exploratory calculations after editing assumptions, import `analysis` and call `calculate()` or `budget()` directly; do not replace the baseline reference merely to silence a failed check.

## Headline

| Quantity | Result |
|---|---:|
| Default covered Chinese monthly cost | RMB3,778.13 |
| Chinese cost at reference FX | US$528.94 |
| Default covered American monthly cost | US$2,004.72 |
| Ratio of monthly costs | 3.7901× |
| Basket-implied RMB per dollar | 1.8846 |
| 2025 national consumption PPP input | 3.46 |
| National PPP factor / basket factor | 1.8359× |
| Additional purchasing power relative to that PPP benchmark | 83.59% |

The FX input is the 2025 annual average of RMB7.1429 per dollar, not current spot. Official PPP is a rounded national household/NPISH consumption factor. This local, selected basket differs in goods, locations, dates, quality matching and weights. The comparison does **not** isolate national PPP measurement error, measure national average living standards or establish a causal policy effect.

The unweighted mean of 22 catalogue ratios is 3.7825×, coincidentally close to the budget result. The headline uses the ratio of monthly totals, not that mean. Catalogue prices mix purchase/month/year periods and mutually exclusive alternatives and must not be summed.

## Default and alternatives

Default: one adult rents, uses transit/taxis, entry phone/laptop and a basic TV. Major appliances are provided with rent; China is furnished and the US includes a furniture provision. Eight bought meals replace eight home-cooked meals, so assumed ingredients are removed from groceries. The MiniLED TV is a separate comparison, not the default budget's TV. Car, bike, basketball shoes and home purchase are alternatives. Utilities, communications, travel, children and medical risk are not comprehensively covered.

Cases 1–4: default; premium devices; renter with EV/hobbies; owner with EV/hobbies. `covered` includes specified purchases; `expanded` adds an assumed RMB400/US$250 routine allowance. Owner cash flows include mortgage principal and exclude the down payment. Upfront baskets are separate views; adding them to monthly replacement budgets would double count.

Replacement periods, residual values, running allowances and avoided grocery ingredients are explicit planning assumptions, not observed average household behaviour. Range endpoints are stress-test scenarios, not confidence limits. Product notes identify differences such as size, warranty, test standards, included services and source dates; this is not a claim that every pair is identical.

## Files and data format

- `analysis.py`: portable calculation and verification script.
- `data/prices.json`: original 22-row catalogue and reference FX. Each row has: name, period, China central (RMB), US central (USD), China low, China high, US low, US high, replacement years, scope note, legacy audit identifier, China primary URL, US primary URL. The legacy audit identifier is retained for provenance, not a link to a file in this repository. Use `source-notes.csv` for published audit notes.
- `data/assumptions.json`: scenario drivers, basic TV alternative, salary and PPP inputs, source URLs and qualifications. Country pairs are China then US, in local currencies unless dimensionless.
- `data/source-notes.csv`: detailed 28-row table export with comparison assumptions and linked evidence, including alternative scenarios.
- `data/sources.csv`: 92 source-link entries extracted from those notes; repeat sources may support several comparisons.
- `data/workbook-reference-results.json`: frozen numerical cross-check, including the original allowance-inclusive weight/sensitivity outputs.
- `results/analysis.json`: all four covered/expanded scenarios, capital baskets, PPP bridge, default-basket sensitivity checks, catalogue statistics and optional hours estimates.
- `results/default-monthly-contributions.csv`: China budget shares and contributions to the weighted headline. Furniture is grouped with housing so every active category has a positive denominator.

## Workbook map and verification

The workbook is preserved from the original analysis. It has 453 formulas with cached results, no cached formula errors and no missing formula caches at publication.

- `Prices and assumptions!B4`: case (1–4); `B5`: central/joint stress selection (1–3); `B6`: RMB per USD; `B7`: durable-life multiplier.
- `Prices and assumptions!B41:C55`: scenario drivers.
- `Summary!B8:D8`: China RMB total, US USD total and covered ratio.
- `Summary!B9:D9`: allowance-inclusive version.
- `Monthly build!C33:D33`: covered totals; `C35:D35`: allowance-inclusive totals.

**Scope distinction:** the original workbook's weighting/sensitivity summaries use the allowance-inclusive budget. The new Python `default_weights` and `sensitivities_default_basis` consistently use the covered default. Both headline totals are reproduced. The PPP and optional hours calculations are in Python, not separate workbook sheets.

## Optional work-hours estimate

`results/analysis.json` includes a supplementary calculation: monthly cost divided by a crowdsourced after-tax monthly salary, multiplied by a standard 174-hour month. The result is 75.50 hours for Chengdu and 79.57 for Houston. If the employee health contribution was already deducted from the reported salary, the corresponding values are 73.10 and 74.81. These use dated Numbeo means, not city medians, and a common assumed working month, not actual hours worked. They should not be presented as measured national worker outcomes. Sources and unresolved deduction treatment are recorded in `assumptions.json`.

## Main external references

- [China 2025 annual exchange rate, National Bureau of Statistics](https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html).
- [World Bank private consumption PPP conversion factor](https://data.worldbank.org/indicator/PA.NUS.PRVT.PP?locations=CN).
- All item-level sources: [source index](data/sources.csv), with rationale and qualifications in [source notes](data/source-notes.csv).

These files contain research inputs and calculation assumptions. Source links may change; the frozen numerical inputs preserve reproducibility of this version.
