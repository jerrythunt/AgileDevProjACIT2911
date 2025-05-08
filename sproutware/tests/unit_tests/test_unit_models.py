import unittest
from unittest.mock import Mock
from unittest.mock import patch

from sproutware.models.seed import Seed
from sproutware.models.time import Time
# make a unit test that only tests that when you run the add_xp function the attribute (self.growth) changes accordingly

class TestSeedMethods(unittest.TestCase):
    # Check general increase
    def test_add_xp_inc(self):
        seed = Seed(xp=0)
        seed.add_xp()
        self.assertEqual(seed.xp, 20)

    # Check if > 100
    def test_add_xp_cap(self):
        seed = Seed(xp=100)
        seed.add_xp()
        self.assertEqual(seed.xp, 100)

    def test_reset_is_watered(self):
        seed = Seed(name="cactus", is_watered=1)
        # Created mock db for session.commit
        with patch("sproutware.models.seed.db.session.commit") as mock_commit:
            result = seed.reset_is_watered()
            self.assertFalse(seed.is_watered)
            self.assertEqual(result, 'cactus needs to be watered!')
            mock_commit.assert_called_once()

    def test_is_waterable_check(self):
        seed = Seed(is_watered=1)

        # Create mock for the reset_is_watered
        with patch("sproutware.models.seed.Seed.reset_is_watered") as mock_reset_is_watered:
            # mimic what reset_is_watered would do
            seed.is_watered = 0
            result = seed.is_waterable_check()

            self.assertEqual(result, True)
            mock_reset_is_watered.assert_called_once()


    

if __name__ == '__main__':
    unittest.main()