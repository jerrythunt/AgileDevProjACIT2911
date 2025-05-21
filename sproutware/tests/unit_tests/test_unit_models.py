import unittest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import datetime as dt, timedelta
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

def test_time_until_waterable():
    seed = Seed(is_watered=True)
    seed.time_of_watering = dt.now() - timedelta(seconds=10)
    seed.water_retention = timedelta(seconds=5)

    with patch("sproutware.models.seed.Seed.reset_is_watered") as mock_reset:
        mock_reset.return_value = "Reset successful"
        result = seed.time_until_waterable()

        assert mock_reset.called or "seconds" in result

    

if __name__ == '__main__':
    unittest.main()