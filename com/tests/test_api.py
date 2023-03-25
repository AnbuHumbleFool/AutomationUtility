import pytest
import json
import requests
import csv
# import pandas as pd

class WholeAPITest():

    @pytest.fixture
    def test_one(self):
        #  Fetch bearer token
        # /.................................Test Case 1...................................../
        url = 'https://accounts.spotify.com/api/token'
        payload = {'grant_type': 'client_credentials'}
        headers = {
            'Authorization': 'Basic YzE0ZDBiMWFlMjlmNGY5Yjg2ZWNlOGZkMTNhNmYyMjk6NmIyYjBlZDMxNTA3NDYxZTk0ZjIxMzdhMzc5ODZhMjE=',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '__Host-device_id=AQD6B9_lD9MJcRtLUYurVItK60k_EK8KAX9UaG6hW4A80pSf46DQUQXuAn47_BqXOVCoTTdRy-nujG4FWVL4IwqAF2JCWf8HzPA; sp_tr=false'}
        res = requests.post(url, data=payload, headers=headers)
        print(res.content)
        print(res.status_code)
        # print(res.get('access_token'))
        jsonResponse = res.json()
        bearer_token = jsonResponse["access_token"]
        print(bearer_token)
        return bearer_token

    @pytest.fixture
    def test_two(self, bearer_token):
        #  Search for AR Rahman artist
        # /.................................Test Case 2...................................../

        url2 = 'https://api.spotify.com/v1/search?query=A.R.+Rahman&offset=0&limit=20&type=artist'

        headers2 = {'Authorization': 'Bearer ' + bearer_token}
        # payload2 = {'query': 'A.R.+Rahman','offset': '0', 'limit'}

        res2 = requests.get(url2, headers=headers2
                            )
        print(res2.content)
        t2JsonResponse = res2.json()
        # Response - Fetch Artist id
        artist_id = t2JsonResponse["artists"]["items"][0]["id"]
        print(artist_id)
        return artist_id


    # /.................................Test Case 3...................................../
    # Search for his top tracks by using the artist id from the above response
    @pytest.fixture
    def test_three(self, artist_id, headers2):
        url3 = 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks?market=in'
        res3 = requests.get(url3, headers= headers2)
        print(res3.content)
        t3JsonResponse = res3.json()
        track_id = t3JsonResponse["tracks"][0]["id"]
        print(track_id)
        return track_id


    # Fetch any one track from the list above and the respective artists/ artist for that track and store It in CSV/flat file
    # Validation: Search for the track using the track id stored in CSV,
    # /.................................Test Case 4...................................../
    @pytest.fixture
    def test_four(self, track_id, artist_id, headers2):
        url4 = 'https://api.spotify.com/v1/tracks/' + track_id
        res4 = requests.get(url4, headers=headers2)
        print(res4.content)
        t4JsonResponse = res4.json()
        # Fetch Artist  name
        artist_name = t4JsonResponse["artists"][0]["name"]
        print(artist_name)

    # Validation: Search for the track using the track id stored in CSV

        with open("C:/Users/DELL/Desktop/sample.json", "w") as outfile:
            json.dump(t4JsonResponse, outfile)

        with open('C:/Users/DELL/Desktop/sample.json') as json_file:
            data = json.load(json_file)

        print(data)
        employee_data = data['artists']

        # now we will open a file for writing
        data_file = open('C:/Users/DELL/Desktop/data_file.csv', 'w')

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing
        # headers to the CSV file
        count = 0

        for emp in employee_data:
            if count == 0:
                # Writing headers of CSV file
                header = emp.keys()
                csv_writer.writerow(header)
                count += 1

            # Writing data of CSV file
            csv_writer.writerow(emp.values())

        data_file.close()

        # Validation: Search for the track using the track id stored in CSV

        FILE_NAME = 'C:/Users/DELL/Desktop/data_file.csv'

        with open(FILE_NAME, 'rt') as f:
            data_excel = csv.reader(f)
            for row in data_excel:
                if artist_id in row:
                    print(row)
