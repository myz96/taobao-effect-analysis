## Appendix: The Maths

The comparison uses a specified monthly basket for one adult in Chengdu and Houston. It brings together dated prices and estimates from 2025–26. It is a worked example of what these purchases cost in each place, rather than a survey of the average household. The [row-by-row notes](https://github.com/myz96/taobao-effect-analysis/blob/main/data/source-notes.csv) explain the products, quantities, taxes, sources and differences behind each comparison.

**What goes into the monthly total?**

The default includes rent and fixed fees, a gym, public transport and taxis, groceries, eight bought meals, an employee health contribution, a small allowance for routine medical visits, clothing, running shoes and replacement provisions for a phone, laptop and TV. It uses the entry phone and laptop and a basic TV. The MiniLED TV in the comparison table is a separate product comparison; the default budget uses the cheaper TV specified in the workbook.

The rental assumptions include major appliances. The Chinese apartment is furnished; the American budget includes a furniture replacement provision. The car, road bike, basketball shoes and home purchase belong to alternative scenarios, not the default total. Utilities, communications, travel, children and comprehensive medical costs are not fully covered. This is therefore a total for the listed purchases, not a complete cost-of-living budget.

Eight bought meals replace eight home-cooked meals. To avoid counting both, I subtract RMB60 from the Chinese grocery allowance and $36 from the American allowance before adding the bought meals. Those avoided ingredient costs are budgeting assumptions.

**Converting prices**

I use RMB7.1429 per US dollar, China's reported average exchange rate for 2025. This is a fixed reference rate, not the current spot rate. [Source: National Bureau of Statistics](https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html).

$$
P_{China,USD}=\frac{P_{China,RMB}}{7.1429}
$$

Each row's multiple divides the American price by the Chinese price expressed in dollars. A result of 3 means the American option costs three times as much.

$$
r_i=\frac{P_{US,i}}{P_{China,i}/7.1429}
$$

**Turning purchases into monthly amounts**

For goods bought occasionally, I spread their purchase price over an assumed replacement period. This is money set aside for replacement, not a loan repayment or a measured monthly purchase.

$$
\text{Monthly provision}=\frac{\text{Purchase price}}{12\times\text{Replacement period in years}}
$$

The assumptions are three years for phones, five for laptops, seven for TVs and furniture, eight for dishwashers, washing machines and bikes, and ten for fridges and cars. The car scenarios allow a 20% resale value; other goods assume none. Clothing and running shoes use annual provisions. For example, the RMB999 entry phone contributes RMB27.75 a month: 999 divided by 36. These periods are assumptions that can be changed in the workbook.

**The headline calculation**

Adding the included monthly amounts gives RMB3,778.13 in China and $2,004.72 in America. At the reference exchange rate, the Chinese total is $528.94. Calculations use unrounded inputs; the amounts here are rounded for readability. [Full monthly breakdown](https://github.com/myz96/taobao-effect-analysis/blob/main/results/default-monthly-contributions.csv).

$$
\text{Monthly price multiple}=\frac{2{,}004.72}{3{,}778.13/7.1429}\approx3.79
$$

In other words, the American version of this basket costs about 3.8 times as much. Equivalently, the Chinese version costs about 73.6% less. This is a price comparison for the chosen basket, not a finding that the average person's whole life is 3.8 times better.

This total gives expensive categories more weight. Let C_i be each category's Chinese monthly cost in RMB, U_i its American monthly cost in dollars, and w_i its share of the Chinese budget. Then the ratio of the totals is also a weighted average of the category ratios:

$$
w_i=\frac{C_i}{\sum_j C_j},\qquad M=\frac{7.1429\sum_i U_i}{\sum_i C_i}=\sum_i w_i\frac{7.1429U_i}{C_i}
$$

Housing and furniture are grouped together for this calculation. The [weighting ledger](https://github.com/myz96/taobao-effect-analysis/blob/main/results/default-monthly-contributions.csv) shows every category's contribution.

For comparison, the simple average of the 22 individual price ratios is 3.78, the geometric average is 2.26 and the median is 1.77. The simple average happens to be close to the monthly result, but it is not how the headline is calculated. It gives a medical visit the same weight as a home and includes alternative device tiers. Excluding the two healthcare comparisons reduces that simple average to 2.13. Raw purchase, monthly and annual prices should not be added together.

**Comparing the basket with PPP**

The basket implies an exchange rate of about RMB1.88 per dollar: that is how many yuan buy the Chinese version of what one dollar buys in the American version.

$$
\text{Basket exchange rate}=\frac{3{,}778.13}{2{,}004.72}\approx1.8846
$$

For comparison, the World Bank's 2025 household consumption PPP factor for China is approximately RMB3.46 per international dollar. I use consumption PPP because this exercise concerns household purchases. [Source: World Bank, private consumption PPP conversion factor](https://data.worldbank.org/indicator/PA.NUS.PRVT.PP?locations=CN).

$$
\text{Basket advantage relative to PPP}=\frac{3.46}{1.8846}\approx1.836
$$

$$
\text{Additional purchasing power}=(1.836-1)\times100\%\approx83.6\%
$$

That is the basis for saying this basket shows about 84% more purchasing power than the national consumption PPP factor would imply. It is not another multiplier to apply on top of 3.79. The two measures describe the same prices against different benchmarks.

The comparison also has limits: our basket uses selected local prices, products and spending weights, while official PPP covers a much broader national range of purchases. The gap does not, by itself, establish that national PPP is wrong by 84% or that the result applies to every Chinese household.

**How much do the assumptions matter?**

Using the same default basket as the starting point:

- Removing housing and household setup reduces the multiple from 3.79 to 3.48.
- Removing the two healthcare components reduces it to 3.65.
- Raising the Chinese grocery allowance to RMB900 and lowering the American one to $330 reduces it to 3.43, with the same deduction for replaced meals.
- Making durable replacement periods 25% shorter gives 3.77; making them 50% longer gives 3.81.
- Choosing all the higher Chinese and lower American price estimates together gives 2.61. Choosing the opposite endpoints gives 5.44. These are stress tests, not a statistical confidence interval.
- Adding a separate routine-expense allowance of RMB400 and $250 gives 3.85. Those allowances are assumptions, not additional sourced bills.

The alternative monthly scenarios give 3.67 for premium devices, 3.20 with an EV and hobbies, and 4.48 for an owner with an EV and hobbies. The owner case includes mortgage principal in monthly cash outflows and excludes the initial down payment, so it is not a pure consumption-cost measure. Upfront purchase totals are shown separately in the results and should not be added to budgets that already contain replacement provisions. [All scenarios and sensitivity results](https://github.com/myz96/taobao-effect-analysis/blob/main/results/analysis.json).

## Workbooks

The complete analysis is available in the public [Taobao Effect analysis repository](https://github.com/myz96/taobao-effect-analysis).

- [Excel workbook](https://github.com/myz96/taobao-effect-analysis/blob/main/workbooks/local-life-budget.xlsx): price inputs, replacement assumptions and four monthly scenarios. Download the file to use the formulas.
- [Reproducible Python script](https://github.com/myz96/taobao-effect-analysis/blob/main/analysis.py): recreates the budgets, weighted comparison, PPP calculation and sensitivity checks using Python's standard library.
- [Price inputs and assumptions](https://github.com/myz96/taobao-effect-analysis/tree/main/data): the frozen inputs used for these calculations, including a [source list](https://github.com/myz96/taobao-effect-analysis/blob/main/data/sources.csv) and [detailed comparison notes](https://github.com/myz96/taobao-effect-analysis/blob/main/data/source-notes.csv).
- [Calculated results](https://github.com/myz96/taobao-effect-analysis/tree/main/results): the monthly contribution ledger and all alternative scenarios.

The workbook's headline sits in Summary row 8. Its separate allowance-inclusive total is in row 9. The original workbook's weighting and sensitivity summaries use the allowance-inclusive version; the Python results and sensitivity figures above consistently use the default basket unless explicitly labelled otherwise.
