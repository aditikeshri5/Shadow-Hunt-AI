
class FuzzyController:
    """
    Fuzzy logic controller for Shadow Hunt AI.

    Inputs:
        distance: Manhattan distance between hunter and player
        crystals_collected: number of crystals collected

    Output:
        aggression: a score from 0 to 100
    """

    @staticmethod
    def triangular(x, a, b, c):
        """Triangular membership function."""
        if x < a or x > c:
            return 0.0

        if x == b:
            return 1.0

        if x < b:
            return (x - a) / (b - a) if b != a else 1.0

        return (c - x) / (c - b) if c != b else 1.0

    @staticmethod
    def trapezoidal(x, a, b, c, d):
        """Trapezoidal membership function."""
        if x < a or x > d:
            return 0.0

        if a == b and x <= b:
            return 1.0

        if c == d and x >= c:
            return 1.0

        if x < b:
            return (x - a) / (b - a)

        if x <= c:
            return 1.0

        return (d - x) / (d - c)

    def calculate_aggression(
        self,
        distance,
        crystals_collected,
        total_crystals=5
    ):
        """Return the fuzzy aggression score from 0 to 100."""

        # Normalize crystal progress to a value between 0 and 1.
        if total_crystals > 0:
            progress = crystals_collected / total_crystals
        else:
            progress = 0.0

        progress = max(0.0, min(1.0, progress))
        distance = max(0.0, float(distance))

        # Input 1: distance membership values.
        near = self.trapezoidal(distance, 0, 0, 3, 6)
        medium = self.triangular(distance, 3, 7, 11)
        far = self.trapezoidal(distance, 8, 12, 40, 30)

        # Input 2: crystal progress membership values.
        few = self.trapezoidal(progress, 0, 0, 0.2, 0.45)
        some = self.triangular(progress, 0.2, 0.5, 0.8)
        almost_all = self.trapezoidal(
            progress, 0.55, 0.8, 1, 1
        )

        # Rule outputs:
        #                 Few   Some   Almost all
        rules = [
            (near, few, 75),
            (near, some, 88),
            (near, almost_all, 100),

            (medium, few, 50),
            (medium, some, 65),
            (medium, almost_all, 82),

            (far, few, 25),
            (far, some, 38),
            (far, almost_all, 55),
        ]

        # Sugeno-style weighted average defuzzification.
        weighted_total = 0.0
        strength_total = 0.0

        for distance_membership, progress_membership, output in rules:
            # AND operator: minimum of the two memberships.
            strength = min(
                distance_membership,
                progress_membership
            )

            weighted_total += strength * output
            strength_total += strength

        if strength_total == 0:
            return 50.0

        aggression = weighted_total / strength_total

        return round(max(0.0, min(100.0, aggression)), 2)
