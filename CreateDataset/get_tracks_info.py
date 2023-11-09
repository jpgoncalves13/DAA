import base64
from requests import post,get
import json
import csv

client_id = ""
client_secret = ""

playlists_ids = [ "37i9dQZF1DXcBWIGoYBM5M", "37i9dQZF1DX0XUsuxWHRQd", "37i9dQZF1DX1lVhptIYRda","37i9dQZF1DX4JAvHpjipBk" ]

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_track_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    header = get_auth_header(token)
    result = get(url, headers=header)
    json_result = json.loads(result.content)
    fields_to_remove =[" analysis_url", "id", "track_href", "type", "uri"]
    new_data = {key: value for key, value in json_result.items() if key not in fields_to_remove}
    return new_data

def get_track_fields(track_object):
    popularity = track_object["popularity"]
    name = track_object["name"]
    artists = []
    for artist in track_object["artists"]:
        artists.append(artist["name"])        
    data = track_object["album"]["release_date"]
    data_presicion = track_object["album"]["release_date_precision"]
    id = track_object["id"]
    return (id, popularity, name, artists, data, data_presicion)


def create_music_obj(item, token):
    id, popularity, name, artists, data, data_presicion = get_track_fields(item["track"]) 
    audio["popularity"] = popularity
    audio = get_track_audio_features(token, id)
    audio["name"] = name
    audio["artists"] = artists
    audio["data"] = data
    audio["data_presicion"] = data_presicion
    audio["id"] = id
    return audio

def read_items_playlist(url, token):
    header = get_auth_header(token)
    result = get(url, headers=header)
    json_result = json.loads(result.content)
    musics = []
    
    for item in json_result["items"]:
        music = create_music_obj(item, token)
        musics.append(music)
    
    if json_result["next"] is not None:
        musics += read_items_playlist(json_result["next"], token)
    
    return musics
    
tok = get_token()

total = []

for playlist_id in playlists_ids:
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    musics = read_items_playlist(url, tok)       
    total += musics


csv_file = 'data.csv'
field_names =  total[0].keys()

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)

    # Write the header row to the CSV file
    writer.writeheader()

    # Write the JSON data to the CSV file
    for json_obj in total:
        writer.writerow(json_obj)

    
