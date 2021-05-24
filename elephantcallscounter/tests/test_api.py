import ast
import requests


class TestApi:
    def test_add_elephants_count(self):
        URL = "http://0.0.0.0:5000/elephants/add_elephant_count/"
        r = requests.get(
            url=URL,
            params={
                "latitude": "20",
                "longitude": "30",
                "start_time": "2020-01-10 06:30:23",
                "end_time": "2021-01-11 06:30:23",
                "device_id": 1,
                "number_of_elephants": 1,
            },
        )
        assert ast.literal_eval(r.text) == {"message": "new elephant added"}
