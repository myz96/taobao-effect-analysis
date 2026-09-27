#!/usr/bin/env python3
"""Reproduce the Taobao Effect budget, PPP bridge and scenario calculations.

Python 3.9+; standard library only. Run from any directory. No network access.
Prices are dated research inputs, not live offers. See README.md for scope.
"""
import csv
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'data/prices.json').read_text())
A = json.loads((ROOT / 'data/assumptions.json').read_text())
FX = DATA['fx']
ROWS = DATA['rows']


def budget(case=1, stress=1, lifetime=1, overrides=None):
    """Return local-currency monthly contributions, excluding routine allowance.

    Cases: 1 default, 2 premium devices, 3 car/hobbies, 4 owner/car/hobbies.
    Stress: 1 central, 2 higher China/lower US, 3 lower China/higher US.
    """
    overrides = overrides or {}
    owner, premium, motor = case == 4, case > 1, case > 2
    countries = []
    for k in range(2):
        idx = [(2, 3), (5, 6), (4, 7)][stress - 1][k]
        p = [overrides.get((i, k), row[idx]) for i, row in enumerate(ROWS)]
        life = lambda i: ROWS[i][8] * 12 * lifetime
        rate = A['mortgage_rate'][k] / 12
        principal = p[0] * (1 - A['down_payment_fraction'])
        months = A['mortgage_years'] * 12
        mortgage = principal * rate / (1 - (1 + rate) ** -months)
        carrying = (p[0] * A['property_tax_rate'][k] / 12
                    + A['home_insurance_annual'][k] / 12
                    + A['management_monthly'][k] + A['repairs_annual'][k] / 12)
        contributions = {
            'Housing and household setup': (mortgage + carrying if owner else p[1])
                + (p[17] / life(17) if owner or k == 1 else 0)
                + (sum(p[i] / life(i) for i in (14, 15, 16)) if owner else 0),
            'Car incl running': p[2] * (1 - A['car_residual_fraction']) / life(2)
                + A['car_running_monthly'][k] if motor else 0,
            'Gym': p[3],
            'Transit and taxis': 0 if motor else p[4],
            'Groceries': max(0, p[5] - A['meals_out'] * A['ingredients_avoided_per_meal'][k]),
            'Prepared meals': p[6] * A['meals_out'] / 8,
            'Employee health premium': p[7],
            'Routine medical basket': p[8] / 12,
            'Phone': p[9 if premium else 10] / life(9 if premium else 10),
            'Laptop': p[11 if premium else 12] / life(11 if premium else 12),
            'TV': (p[13] if premium else A['basic_tv'][k]) / life(13),
            'Clothing': p[18] / 12,
            'Running shoes': p[19] / (ROWS[19][8] * 12),
            'Basketball shoes': p[20] / (ROWS[20][8] * 12) if motor else 0,
            'Road bike': p[21] / life(21) if motor else 0,
        }
        countries.append(contributions)
    cn, us = (sum(c.values()) for c in countries)
    return {'case': case, 'coveredCN': cn, 'coveredUS': us,
            'coveredMultiple': us * FX / cn,
            'expandedCN': cn + A['routine_allowance'][0],
            'expandedUS': us + A['routine_allowance'][1],
            'expandedMultiple': (us + A['routine_allowance'][1]) * FX / (cn + A['routine_allowance'][0]),
            'contributions': {n: {'china_RMB': countries[0][n], 'us_USD': countries[1][n]}
                              for n in countries[0]}}


def calculate():
    profiles = [budget(i) for i in range(1, 5)]
    default = profiles[0]
    cn, us = default['coveredCN'], default['coveredUS']
    factor = cn / us
    ratios = [row[3] * FX / row[2] for row in ROWS]
    ex_health = [v for i, v in enumerate(ratios) if i not in (7, 8)]
    weights = []
    for name, c in default['contributions'].items():
        if c['china_RMB']:
            ratio = c['us_USD'] * FX / c['china_RMB']
            weight = c['china_RMB'] / cn
            weights.append({'category': name, **c, 'china_weight': weight,
                            'multiple': ratio, 'weighted_contribution': weight * ratio})
    sensitivities = [{'label': 'Default', 'multiple': default['coveredMultiple']}]
    for label, cats in [('Exclude housing/setup', ['Housing and household setup']),
                        ('Exclude food', ['Groceries', 'Prepared meals']),
                        ('Exclude healthcare', ['Employee health premium', 'Routine medical basket'])]:
        cc = cn - sum(default['contributions'][n]['china_RMB'] for n in cats)
        uu = us - sum(default['contributions'][n]['us_USD'] for n in cats)
        sensitivities.append({'label': label, 'multiple': uu * FX / cc})
    for label, result in [
        ('Food: China RMB900 / US$330', budget(overrides={(5, 0): 900, (5, 1): 330})),
        ('Durable lives 25% shorter', budget(lifetime=.75)),
        ('Durable lives 50% longer', budget(lifetime=1.5)),
        ('Joint stress: higher China / cheaper US', budget(stress=2)),
        ('Joint stress: cheaper China / higher US', budget(stress=3)),
    ]:
        sensitivities.append({'label': label, 'multiple': result['coveredMultiple']})
    sensitivities.append({'label': 'Add routine allowance', 'multiple': default['expandedMultiple']})
    goods = (2, 9, 11, 13, 14, 15, 16, 17, 21)
    capital = []
    for label, inds in [('Selected goods', goods), ('Selected goods plus home', (0,) + goods)]:
        c, u = sum(ROWS[i][2] for i in inds), sum(ROWS[i][3] for i in inds)
        capital.append({'label': label, 'china_RMB': c, 'us_USD': u, 'multiple': u * FX / c})
    return {
        'as_of': A['as_of'], 'fx_RMB_per_USD': FX,
        'profiles': profiles, 'capital_baskets': capital, 'default_weights': weights,
        'headline': {'china_RMB': cn, 'china_USD': cn / FX, 'us_USD': us,
                     'market_FX_multiple': us * FX / cn, 'basket_RMB_per_dollar': factor,
                     'consumption_PPP_RMB_per_international_dollar': A['consumption_ppp'],
                     'basket_vs_PPP_multiple': A['consumption_ppp'] / factor,
                     'additional_purchasing_power_percent': (A['consumption_ppp'] / factor - 1) * 100,
                     'china_saving_vs_US_percent': (1 - cn / FX / us) * 100},
        'catalogue': {'arithmetic_mean': statistics.mean(ratios),
                      'geometric_mean': math.exp(statistics.mean(map(math.log, ratios))),
                      'median': statistics.median(ratios),
                      'arithmetic_excluding_healthcare': statistics.mean(ex_health),
                      'geometric_excluding_healthcare': math.exp(statistics.mean(map(math.log, ex_health)))},
        'hours': {'china': cn / A['after_tax_salary_monthly'][0] * A['standard_monthly_hours'],
                  'us': us / A['after_tax_salary_monthly'][1] * A['standard_monthly_hours'],
                  'china_if_health_already_deducted': (cn - ROWS[7][2]) / A['after_tax_salary_monthly'][0] * A['standard_monthly_hours'],
                  'us_if_health_already_deducted': (us - ROWS[7][3]) / A['after_tax_salary_monthly'][1] * A['standard_monthly_hours']},
        'sensitivities_default_basis': sensitivities,
    }


def verify(result):
    """Cross-check against independent saved workbook results before writing."""
    original = json.loads((ROOT / 'data/workbook-reference-results.json').read_text())
    for actual, expected in zip(result['profiles'], original['profiles']):
        for key in ('coveredCN', 'coveredUS', 'coveredMultiple', 'expandedCN', 'expandedUS', 'expandedMultiple'):
            assert math.isclose(actual[key], expected[key], rel_tol=1e-11, abs_tol=1e-8), (actual['case'], key)
    stats = ('arithmetic_mean', 'geometric_mean', 'median', 'arithmetic_excluding_healthcare', 'geometric_excluding_healthcare')
    for key, expected in zip(stats, original['catalogueStats']):
        assert math.isclose(result['catalogue'][key], expected['value'], rel_tol=1e-11), key
    weighted = sum(r['weighted_contribution'] for r in result['default_weights'])
    assert math.isclose(weighted, result['headline']['market_FX_multiple'], rel_tol=1e-11)
    for stress, expected in zip((1, 2, 3), original['stress']):
        assert math.isclose(budget(stress=stress)['coveredMultiple'], expected['coveredMultiple'], rel_tol=1e-11)
    for multiplier, expected in zip((.75, 1, 1.5), original['lifetime']):
        assert math.isclose(budget(lifetime=multiplier)['coveredMultiple'], expected['coveredMultiple'], rel_tol=1e-11)


if __name__ == '__main__':
    result = calculate()
    verify(result)
    target = ROOT / 'results'
    target.mkdir(exist_ok=True)
    (target / 'analysis.json').write_text(json.dumps(result, indent=2) + '\n')
    with (target / 'default-monthly-contributions.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(result['default_weights'][0]))
        writer.writeheader()
        writer.writerows(result['default_weights'])
    print('Verified all four budgets, catalogue statistics, stress/lifetime cases and weighted identity.')
    print(json.dumps(result['headline'], indent=2))
