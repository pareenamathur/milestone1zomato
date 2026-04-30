import unittest
from src.milestone_1.phase_2_preferences.schema import RestaurantRecord, UserPreferences, BudgetPreference
from src.milestone_1.phase_3_candidates.filter import apply_filters
from src.milestone_1.phase_3_candidates.ranker import rank_candidates
from src.milestone_1.phase_2_preferences.parser import parse_preferences

class TestPipelineComponents(unittest.TestCase):
    def setUp(self):
        self.restaurants = [
            RestaurantRecord(id="1", name="R1", location="delhi", cuisines=["italian"], rating=4.0, cost=500, price_category="low"),
            RestaurantRecord(id="2", name="R2", location="delhi", cuisines=["chinese"], rating=3.5, cost=1000, price_category="medium"),
            RestaurantRecord(id="3", name="R3", location="mumbai", cuisines=["italian"], rating=4.5, cost=1500, price_category="high"),
        ]

    def test_filter_logic(self):
        prefs = UserPreferences(
            location="Delhi",
            cuisines=["italian"],
            budget=BudgetPreference(mode="category", category="low"),
            min_rating=3.0
        )
        filtered = apply_filters(self.restaurants, prefs)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "1")

    def test_parser_logic(self):
        data = {
            "location": "Bangalore",
            "cuisines": "Indian, Thai",
            "budget_mode": "range",
            "min_cost": 500,
            "max_cost": 1500,
            "min_rating": 4.2
        }
        prefs = parse_preferences(data)
        self.assertEqual(prefs.location, "Bangalore")
        self.assertEqual(prefs.cuisines, ["indian", "thai"])
        self.assertEqual(prefs.budget.mode, "range")
        self.assertEqual(prefs.budget.min_cost, 500)
        self.assertEqual(prefs.min_rating, 4.2)

    def test_ranker_logic(self):
        prefs = UserPreferences(
            location="Delhi",
            cuisines=["italian", "chinese"],
            budget=BudgetPreference(mode="category", category="medium"),
            min_rating=0
        )
        candidate_set = rank_candidates(self.restaurants, prefs, top_k=2)
        self.assertEqual(len(candidate_set.candidates), 2)
        # R3 has 4.5, R1 has 4.0, R2 has 3.5. So R3 and R1 should be top 2.
        self.assertEqual(candidate_set.candidates[0].id, "3")
        self.assertEqual(candidate_set.candidates[1].id, "1")

if __name__ == "__main__":
    unittest.main()
