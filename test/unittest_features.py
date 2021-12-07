from features import *
from playlistid import *
from auth import *
import unittest
import sys
import os
sys.path.insert(0, os.getcwd())


class Test_features(unittest.TestCase):
    TOKEN = None

    def setUpClass():
        Test_features.TOKEN = get_token()

    def test_playlist_id_cleaner(self):
        self.assertEqual(playlist_id_cleaner(
            "https://open.spotify.com/playlist/3SupZyS989AAZUZI3pOWla?si=b6bf742b829146b8"), "3SupZyS989AAZUZI3pOWla")
        self.assertEqual(playlist_id_cleaner(" "), "Invalid playlist link")

    def test_playlist_name(self):
        result_one = playlist_name(
            "3SupZyS989AAZUZI3pOWla", Test_features.TOKEN)
        result_two = playlist_name(
            "7eD93U5m3ghZuXKdYVtOR8", Test_features.TOKEN)
        result_three = get_api_features("g54g23", Test_features.TOKEN)
        self.assertEqual(result_one, {'name': 'Casual993'})
        self.assertEqual(result_two, {'name': "House Relax"})
        self.assertIsNone(result_three)

    def test_get_api_artist(self):
        result_one = get_api_artist(
            "6XyY86QOPPrYVGvF9ch6wz", Test_features.TOKEN)
        result_two = get_api_artist(
            "6M2wZ9GZgrQXHCFfjv46we", Test_features.TOKEN)
        result_three = get_api_artist("911", Test_features.TOKEN)
        self.assertListEqual(
            result_one, ['alternative metal', 'nu metal', 'post-grunge', 'rap metal'])
        self.assertListEqual(result_two, ['dance pop', 'pop', 'uk pop'])
        self.assertIsNone(result_three)

    def test_get_api_features(self):
        result_one = get_api_features(
            "30bqVoKjX479ab90a8Pafp", Test_features.TOKEN)
        result_two = get_api_features(
            "4oWDaJpusSH1lqIQQkEHsS", Test_features.TOKEN)
        result_three = get_api_features("666", Test_features.TOKEN)
        self.assertEqual(result_one['danceability'], 0.585)
        self.assertEqual(result_two['danceability'], 0.609)
        self.assertIsNone(result_three)

    def test_convertMillis(self):
        result_one = convertMillis(1056045)
        result_two = convertMillis(626949)
        self.assertEqual(result_one, 17.36)
        self.assertEqual(result_two, 10.26)


if __name__ == "__main__":
    unittest.main()