class ForwardRateInterpreter:
    def __init__(self, forward_rate: float, spot_rate: float, tenor_days: int) -> None:
        self.forward_rate: float = forward_rate
        self.spot_rate: float = spot_rate
        self.tenor_days: int = tenor_days

    @property
    def forward_spot_ratio(self) -> float:
        return round(self.forward_rate / self.spot_rate, 4)
    
    @property
    def forward_premium_discount(self) -> float:
        """
        Forward premium/discount in percentage terms. E.g. 0.1 for 10%
        """
        return round((self.forward_spot_ratio - 1), 4)
    
    @property
    def annualised_premium_discount(self) -> float:
        """
        Annualised forward premium/discount in percentage terms. E.g. 0.1 for 10%
        Enables comparison of forward premium/discount across different tenors.
        """
        return round((self.forward_spot_ratio - 1) * (1 / (self.tenor_days / 360)), 4)

    @property
    def forward_points(self) -> float:
        # Currently assumes 1 pip is 0.0001 of quoted rate
        return round((self.forward_rate - self.spot_rate) * 10_000, 0)
    
    def get_detailed_interpretations(self) -> list[str]:
        if self.forward_spot_ratio > 1:
            return [
                "The forward rate is greater than the spot rate which implies that domestic rates are higher than foreign rates.",
                "Intuition: If the domestic rates are higher than foreign rates then the forward needs to be higher (foreign currency appreciation) than spot to makeup for higher domestic payoff.",
                "1 unit of foreign currency will buy more domestic currency at time T (today) than it does at today's spot (foreign currency is at a forward premium)",
                "Also means the same amount of domestic currency will buy less foreign currency at time T today than it does today's spot (domestic currency is at a forward discount)",
                f"Domestic currency forward must be {abs((self.forward_spot_ratio - 1) * 100):.2f}% cheaper (relative to spot) to prevent arbitrage.",
                f"Foreign currency forward must be {abs((self.forward_spot_ratio - 1) * 100):.2f}% more expensive (relative to spot) to prevent arbitrage."
            ]
        else:
            return [
                "The forward rate is less than the spot rate which implies that domestic rates are lower than foreign rates.",
                "Intuition: If the domestic rates are lower than foreign rates then the forward needs to be lower (foreign currency depreciation) than spot to makeup for lower domestic payoff.",
                "1 unit of foreign currency will buy less domestic currency at time T (today) than it does at today's spot (foreign currency is at a forward discount)",
                "Also means the same amount of domestic currency will buy more foreign currency at time T today than it does today's spot (domestic currency is at a forward premium)",
                f"Domestic currency must be {abs((self.forward_spot_ratio - 1) * 100):.2f}% more expensive in the forward (relative to spot) to prevent arbitrage.",
                f"Foreign currency must be {abs((self.forward_spot_ratio - 1) * 100):.2f}% cheaper in the forward to prevent arbitrage."
            ]