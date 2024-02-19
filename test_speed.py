from speed import to_meters, join_df, calc_speed, get_speed
import unittest
import pandas as pd


class Test_to_meters(unittest.TestCase):
    def test_to_meters(self):
        self.assertAlmostEqual(to_meters(52.24519592405552, 20.942872147320227, 52.21291862526866, 20.98256003621196), 4480, delta=25)
        self.assertAlmostEqual(to_meters(52.24519592405552, 20.942872147320227, 52.24831592436876, 21.01427970232149), 4850, delta=25)


class Test_join_df(unittest.TestCase):
    def test_join_df(self):
        data = {
            "Lines": ["1", "1", "1", "1", "2", "2", "2", "2"],
            "Lon": [21.160676, 21.123335, 21.116851, 21.115010, 20.873983, 20.905251, 20.938139, 20.952564],
            "VehicleNumber": ["1", "1", "2", "2", "3", "3", "4", "4"],
            "Time": ["2024-02-03 22:29:55", "2024-02-03 22:29:54", "2024-02-03 22:29:52", "2024-02-03 22:29:48", "2024-02-03 23:29:18", "2024-02-03 23:29:18", "2024-02-03 23:29:27", "2024-02-03 23:29:27"],
            "Lat": [52.193755, 52.214915, 52.234741, 52.234919, 52.227821, 52.228340, 52.275085, 52.279385],
            "Brigade": ["1", "1", "2", "2", "3", "3", "4", "4"]
        }
        data = pd.DataFrame(data)
        data = join_df(data)
        data.reset_index(drop=True, inplace=True)
        answer = [
            ["1", 21.123335, "1", "2024-02-03 22:29:54", 52.214915, "1", "1", 21.160676, "1", "2024-02-03 22:29:55", 52.193755, "1"],
            ["1", 21.115010, "2", "2024-02-03 22:29:48", 52.234919, "2", "1", 21.116851, "2", "2024-02-03 22:29:52", 52.234741, "2"],
            ["2", 20.873983, "3", "2024-02-03 23:29:18", 52.227821, "3", "2", 20.905251, "3", "2024-02-03 23:29:18", 52.228340, "3"],
            ["2", 20.938139, "4", "2024-02-03 23:29:27", 52.275085, "4", "2", 20.952564, "4", "2024-02-03 23:29:27", 52.279385, "4"]
        ]
        column = ["Lines_1", "Lon_1", "VehicleNumber_1", "Time_1", "Lat_1", "Brigade_1", "Lines_2", "Lon_2", "VehicleNumber_2", "Time_2", "Lat_2", "Brigade_2"]
        answer = pd.DataFrame(answer, columns=column)
        self.assertTrue(data.equals(answer))


class Test_calc_speed(unittest.TestCase):
    def test_calc_speed_normal(self):
        column = ["Lines_1", "Lon_1", "VehicleNumber_1", "Time_1", "Lat_1", "Brigade_1", "Lines_2", "Lon_2", "VehicleNumber_2", "Time_2", "Lat_2", "Brigade_2"]
        row = [["1", 21.123335, "1", "2024-02-03 22:29:54", 52.214915, "1", "1", 21.160676, "1", "2024-02-03 22:29:55", 52.193755, "1"]]
        row = pd.DataFrame(row, columns=column).iloc[0]
        velosity = to_meters(52.214915, 21.123335, 52.193755, 21.160676) / 1000 * 3600
        ans = [velosity, 52.214915, 21.123335, "1", "2024-02-03 22:29:54"]
        self.assertAlmostEqual(calc_speed(row)[0], ans[0], places=2)
        self.assertEqual(calc_speed(row)[1:], ans[1:])

    def test_calc_speed_zero(self):
        column = ["Lines_1", "Lon_1", "VehicleNumber_1", "Time_1", "Lat_1", "Brigade_1", "Lines_2", "Lon_2", "VehicleNumber_2", "Time_2", "Lat_2", "Brigade_2"]
        row = [["1", 21.123335, "1", "2024-02-03 22:29:55", 52.214915, "1", "1", 21.160676, "1", "2024-02-03 22:29:55", 52.193755, "1"]]
        row = pd.DataFrame(row, columns=column).iloc[0]
        velosity = 0
        ans = [velosity, 52.214915, 21.123335, "1", "2024-02-03 22:29:55"]
        self.assertAlmostEqual(calc_speed(row)[0], ans[0], places=2)
        self.assertEqual(calc_speed(row)[1:], ans[1:])


class Test_get_speed(unittest.TestCase):
    def test_get_speed(self):
        data = {
            "Lines": ["1", "1", "1", "1", "2", "2", "2", "2"],
            "Lon": [21.160676, 21.123335, 21.116851, 21.115010, 20.873983, 20.905251, 20.938139, 20.952564],
            "VehicleNumber": ["1", "1", "2", "2", "3", "3", "4", "4"],
            "Time": ["2024-02-03 22:29:55", "2024-02-03 22:29:55", "2024-02-03 22:29:52", "2024-02-03 22:29:48", "2024-02-03 23:29:18", "2024-02-03 23:29:18", "2024-02-03 23:29:27", "2024-02-03 23:29:27"],
            "Lat": [52.193755, 52.214915, 52.234741, 52.234919, 52.227821, 52.228340, 52.275085, 52.279385],
            "Brigade": ["1", "1", "2", "2", "3", "3", "4", "4"]
        }
        data = pd.DataFrame(data)
        data = get_speed(data)
        data = data.to_list()
        answer = [[114.23027762069891, 52.234919, 21.11501, '1', '2024-02-03 22:29:48']]
        # answer = pd.Series(data=answer)
        # self.assertTrue(data.equals(answer))
        self.assertEquals(data, answer)


if __name__ == '__main__':
    unittest.main()
