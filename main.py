"""TASK 3"""
import folium
import requests
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim


def get_information(username):
    """
    Gets information about a specific user's followers
    """
    bearer_token = \
'AAAAAAAAAAAAAAAAAAAAAJ32ZAEAAAAA%2B5H%2BzF8MAfxahMPXdBrlbutKW30%3D6Vh4exUrn2x8RcsydpXnRQA7g5H3SmKqR1ouiOF1UQypZLNobl'
    headers = {'Authorization': f'Bearer {bearer_token}'}
    params = {'screen_name': username, 'count': 20}

    response = requests.get('https://api.twitter.com/1.1/friends/list.json',
                            headers=headers,
                            params=params)
    try:
        return response.json()["users"]  # returns dictionary
    except KeyError:
        return False


def get_location(data):
    """
    This function gets friends' locations list
    """
    location_list = []
    for element in data:
        if element['location'] == "":
            continue
        else:
            location = locate_place(element['location'])
            location_list.append((element['screen_name'], location))
    return location_list


def locate_place(place):
    """
    This function locates the place and
    returns coordinates of it
    """
    place_locator = Nominatim(user_agent="place_locator")

    try:  # if place is not found rises exception
        location = place_locator.geocode(place)
    except:
        location = None

    if location is None:  # if location exists returns coordinates
        return None
    else:
        return location.latitude, location.longitude


def create_map(friends_location):
    """
    This function adds location of the group to the map
    """
    map_object = folium.Map(location=[20, 0], zoom_start=2, control_scale=True)
    friend_location = folium.FeatureGroup()
    for friend in friends_location:
        try:
            friend_location.add_child(folium.Marker(location=[friend[1][0], friend[1][1]],
                                                    popup=f"{friend[0]}",
                                                    icon=folium.Icon()))
        except TypeError:
            continue
    map_object.add_child(friend_location)
    map_object.save("templates/map.html")


def main(username):
    data = get_information(username)  # gets information about specific user followers
    friends_location = get_location(data)  # gets name and location of friends
    create_map(friends_location)  # creates a map with friends_location info


app = Flask(__name__)


@app.route('/')
def open_main_page():
    """
    Opens main page
    """
    return render_template('index.html')


@app.route('/display_map', methods=['POST'])
def form_post():
    """
    Posting the information in the form
    """
    username = request.form['nickname']
    main(username)
    return render_template("map.html")


app.run()


app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
