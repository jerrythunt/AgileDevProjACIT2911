import unittest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import datetime as dt, timedelta

from sproutware.models.seed import Seed
from sproutware.models.time import Time
# make a unit test that only tests that when you run the add_xp function the attribute (self.growth) changes accordingly

class TestSeedMethods(unittest.TestCase):
    def test_add_hp(self):
        seed = Seed(hp=0)
        seed.add_hp()
        self.assertEqual(seed.hp, 20)

    def test_add_hp_cap(self):
        seed = Seed(hp=100)
        seed.add_hp()
        self.assertEqual(seed.hp, 100)

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

    def test_time_until_waterable(self):
        pass

    @patch('sproutware.models.seed.db.session')
    @patch('sproutware.models.seed.dt')
    def test_decay_hp_no_watering_time(self, mock_dt, mock_session):
        seed = Seed(hp=10)
        seed.time_of_watering = None
        seed.dead_plant = Mock()
        seed.decay_hp
        self.assertEqual(seed.hp, 10)
        seed.dead_plant.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch('sproutware.models.seed.db.session')
    @patch('sproutware.models.seed.dt')
    def test_decay_hp(self, mock_dt, mock_session):
        seed = Seed(hp=10, decay_amount=2, decay_interval=timedelta(hours=1))
        seed.time_of_watering = seed.time_of_watering = dt(2025, 5, 15, 9, 0, 0)

        # mock dt.now()
        mock_dt.now.return_value = dt(2025, 5, 15, 12, 0, 0)

        seed.dead_plant = Mock()

        seed.decay_hp()

        self.assertEqual(seed.hp, 4)
        seed.dead_plant.assert_not_called()
        mock_session.commit.assert_called_once()

    @patch('sproutware.models.seed.db.session')
    @patch('sproutware.models.seed.dt')
    def test_decay_hp_dead_plant(self, mock_dt, mock_session):
        seed = Seed(hp=5, decay_amount=3, decay_interval=timedelta(hours=1))
        seed.time_of_watering = seed.time_of_watering = dt(2025, 5, 15, 9, 0, 0)

        # mock dt.now()
        mock_dt.now.return_value = dt(2025, 5, 15, 12, 0, 0)

        seed.dead_plant = Mock()

        seed.decay_hp()

        self.assertEqual(seed.hp, 0)
        seed.dead_plant.assert_called_once()
        mock_session.commit.assert_called_once()


    @patch('sproutware.models.seed.db.session')
    @patch('builtins.print')
    def test_dead_plant_zero(self, mock_print, mock_session):
        seed = Seed(name='Sunflower', hp=0)
        mock_seed = Mock()
        mock_scalar = Mock(return_value=mock_seed)
        mock_execute_result = Mock(scalar=mock_scalar)
        mock_session.execute.return_value = mock_execute_result

        seed.dead_plant()
        mock_print.assert_called_once_with("Sunflower has reached 0 HP and has died! Poor thing... Don\'t forget to water!")

        mock_session.execute.assert_called_once()
        mock_scalar.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_seed)
        mock_session.commit.assert_called_once()

    @patch('sproutware.models.seed.db.session')
    @patch('builtins.print') 
    def test_dead_plant_pos(self,mock_print, mock_session):
        seed = Seed(hp=1)
        seed.dead_plant()
        mock_session.execute.assert_not_called()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_print.assert_not_called()



    

if __name__ == '__main__':
    unittest.main()