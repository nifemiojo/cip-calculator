from typing import List

def calculate_forward_rate(
        domestic_rate_annual: float,
        foreign_rate_annual: float,
        days_to_maturity: int,
        spot_rate: float
) -> float:
    """
    Compute forward rate.

    Parameters
    ----------
    domestic_rate_annual : float
        Annual domestic rate e.g. 0.05 for 5%.
    foreign_rate_annual : float
        Annual foreign rate e.g. 0.02 for 2%.
    days_to_maturity : int
        Number of days to maturity.
    spot_rate : float
        Spot rate at time t.

    Returns
    -------
    float
        Forward rate at time t.

    Examples
    --------
    >>> calculate_forward_rate(0.05, 0.02, 365, 1.0)
    1.0074
    """
    # Assume ACT/365
    tenor_years = days_to_maturity / 365 

    # Domestic payoff (in domestic currency)
    domestic_rate_scaled = domestic_rate_annual * tenor_years
    domestic_payoff = (1 + domestic_rate_scaled)

    # Foreign payoff (in foreign currency)
    foreign_rate_scaled = foreign_rate_annual * tenor_years
    foreign_payoff_in_foreign_currency = (1 + foreign_rate_scaled) * (1 / spot_rate)

    # Forward rate: domestic currency per 1 unit of foreign currency
    return domestic_payoff / foreign_payoff_in_foreign_currency

def calculate_multiple_forward_rates(
        domestic_rate_annual: float,
        foreign_rate_annual: float,
        tenors_days: List[int],
        spot_rate: float
) -> List[float]:
    """
    Compute multiple forward rates.

    Parameters
    ----------
    domestic_rate_annual : float
        Annual domestic rate e.g. 0.05 for 5%.
    foreign_rate_annual : float
        Annual foreign rate e.g. 0.02 for 2%.
    tenors_days : list[int]
        List of tenors in days.
    spot_rate : float
        Spot rate at time t.

    Returns
    -------
    list[float]
        List of forward rates for each tenor.

    Examples
    --------
    >>> calculate_multiple_forward_rates(0.05, 0.02, [30, 60, 90, 120], 1.0)
    [1.0074, 1.0147, 1.022, 1.0294]
    """
    forward_rates = []

    for tenor_days in tenors_days:
        forward_rates.append(calculate_forward_rate(domestic_rate_annual, foreign_rate_annual, tenor_days, spot_rate))

    return forward_rates

def does_cip_equality_hold(
        forward_rate: float,
        domestic_rate_annual: float,
        foreign_rate_annual: float,
        days_to_maturity: int,
        spot_rate: float
) -> bool:
    """
    Check if CIP payoff equality holds for a given forward rate.

    Parameters
    ----------
    forward_rate : float
        Forward rate at time t.
    domestic_rate_annual : float
        Annual domestic rate e.g. 0.05 for 5%.
    foreign_rate_annual : float
        Annual foreign rate e.g. 0.02 for 2%.
    days_to_maturity : int
        Number of days to maturity.
    spot_rate : float
        Spot rate at time t.

    Returns
    -------
    bool
        True if CIP payoff equality holds, False otherwise.
    """
    # Assume ACT/365
    tenor_years = days_to_maturity / 365 

    # Domestic payoff (in domestic currency)
    domestic_rate_scaled = domestic_rate_annual * tenor_years
    domestic_payoff = (1 + domestic_rate_scaled)

    # Foreign payoff (in foreign currency)
    foreign_rate_scaled = foreign_rate_annual * tenor_years
    foreign_payoff_in_foreign_currency = (1 + foreign_rate_scaled) * (1 / spot_rate)

    return abs(domestic_payoff - (foreign_payoff_in_foreign_currency * forward_rate)) < 1e-10