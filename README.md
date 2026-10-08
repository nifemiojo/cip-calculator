# FX Forward Pricing & Scenario Analysis

A small Python toolkit for calculating FX forward rates from covered interest parity and exploring how interest-rate changes affect a forward curve.

**What exchange rate makes a domestic deposit and a currency-hedged foreign deposit produce the same payoff?** The project turns that no-arbitrage relationship into reusable calculations, visual examples and premium/discount interpretation.

## What it does

- Calculates an implied forward rate for a chosen spot rate, tenor and pair of interest rates.
- Builds simplified forward curves across multiple maturities.
- Compares a base curve with a domestic interest-rate shock.
- Reports forward points and forward premium/discount, including an annualised comparison.
- Checks equality of the domestic and hedged foreign payoffs.

## Start here

| Material | Focus |
|---|---|
| [Cash-flow calculation](cip_calculator.ipynb) | Build the forward rate from deposit payoffs |
| [Forward curve](cip-forward-curve.ipynb) | Compare maturities and interpret the forward against spot |
| [Rate-shock scenarios](cip_forward_curve_shocks.ipynb) | See how a change in domestic rates moves the curve |
| [Pricing functions](cip.py) | Reusable single/multiple-tenor calculations and payoff check |
| [Interpreter](cip_interpreter.py) | Premium/discount and forward-point calculations |

## Quick example

Run from the cloned repository root. The core calculation uses only the Python standard library:

```python
from cip import calculate_forward_rate, does_cip_equality_hold

# Quote: domestic currency units per 1 foreign currency unit.
# Annual rates are decimals; the function uses ACT/360.
forward = calculate_forward_rate(
    domestic_rate_annual=0.06,
    foreign_rate_annual=0.02,
    days_to_maturity=90,
    spot_rate=1.32,
)

print(f"{forward:.6f}")  # 1.333134
assert does_cip_equality_hold(forward, 0.06, 0.02, 90, 1.32)
```

Here, one foreign currency unit costs 1.32 domestic units at spot and approximately 1.333134 for delivery in 90 days. This is a model-implied forward price, not a prediction of the future spot rate.

## Run the notebooks

Use Python 3.9+:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas plotly jupyter
jupyter notebook
```

On Windows, activate with `.venv\Scripts\activate`. Open notebooks from the repository root so local module imports resolve. Dependency versions are not pinned.

## Assumptions and conventions

The model uses simple interest, constant annual rates across tenors and frictionless covered interest parity. It does not calibrate market yield curves or incorporate bid/ask spreads, funding differences or cross-currency basis.

`cip.py` and the curve notebooks use **ACT/360**; the standalone cash-flow notebook uses **ACT/365**. Use the same convention when comparing results. The interpreter assumes one pip is `0.0001`, which does not suit every currency pair. Some function docstring examples are stale; the executable example above reflects the current implementation.
