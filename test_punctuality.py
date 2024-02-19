from punctuality import join_df, calc_punctuality, time_diff
import unittest
import pandas as pd


class Test_join_df(unittest.TestCase):
    def setUp(self):
        self.bus_df = pd.DataFrame({
            'Lat': [52.1, 52.2, 52.3],
            'Lon': [21.1, 21.2, 21.3],
            'Lines': ['1', '2', '3'],
            'Time': ['2022-01-01 12:00:00', '2022-01-01 12:10:00', '2022-01-01 12:20:00'],
            'Brigade': ['1', '2', '3']
        })
        self.time_df = pd.DataFrame({
            'Brigade': ['1', '2', '3'],
            'Lines': ['1', '2', '3'],
            'Time': ['2022-01-01 12:00:00', '2022-01-01 12:10:00', '2022-01-01 12:20:00']
        })
        self.speed = pd.Series([[30, 52.1, 21.1, '1', '2022-01-01 12:00:00'],
                                [35, 52.2, 21.2, '2', '2022-01-01 12:10:00'],
                                [40, 52.3, 21.3, '3', '2022-01-01 12:20:00']])

    def test_join_df(self):
        result = join_df(self.bus_df, self.time_df, self.speed)
        self.assertEqual(len(result), 3)

    def test_calc_punctuality(self):
        sample_row = {'Time_diff': 0.4, 'Lat_stop': 52.1, 'Lon_stop': 21.1, 'Lat_bus': 52.2, 'Lon_bus': 21.2, 'Velosity': 30}
        result = calc_punctuality(pd.Series(sample_row))
        self.assertTrue(result)

    def test_time_diff(self):
        sample_row = {'Time_stop': pd.to_timedelta('12:00:00'), 'Time_bus': pd.to_datetime('2022-01-01 12:30:00')}
        result = time_diff(pd.Series(sample_row))
        self.assertAlmostEqual(result, 0.5)


if __name__ == '__main__':
    unittest.main()
