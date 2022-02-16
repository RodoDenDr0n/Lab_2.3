# Lab_2.3
## About the project
This project was about creating the web-app based on Twitter API that would be able to search location of user's friends. The project would help those who want to know the hometown of their friends in Twitter.
## Functions used in the project
- get_information()
- get_location()
- locate_place()
- create_map()
- main()
- open_main_page()
- form_post()
- add_header()
## get_information()
This function gets information about the user by using a bearer token and returns the dictionary with user friends in Twitter
```python
def get_information():
    ...
    try:
        return response.json()["users"]
    except KeyError:
        return False
```
Exception is raised in case user has no friends
## get_location()
This function take the value of data - a dictionary with information about user's friends. This function creates a list with locations that consists of tuples with information about friend's name and the location of friend. The ocation is found with the help of called ```locate_place()``` function (see ```locate_place()``` function description).
```python
def get_location():
    ...
    else:
        location = locate_place(element['location'])
        location_list.append((element['screen_name'], location))
    return location_list
```
## locate_place()
This function takes the value of place and seaches it
```python
def locate_place(place):
    place_locator = Nominatim(user_agent="place_locator")

    try:  # if place is not found rises exception
        location = place_locator.geocode(place)
    except:
        location = None

    if location is None:  # if location exists returns coordinates
        return None
    else:
        return location.latitude, location.longitude
```
If the place is not found raises the exception
## create_map()
This function takes the value of friends' location and is responsible for creating the map with markers of friends' location and usernames
```python
def create_map(friends_location):
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
```
Exception is raised if friend's location does not exist
## main()
This function gets the value of friends' username is responsible for defining data about friends' accounts and, thus, location and creates map with friends' locations
```python
def main(username):
    data = get_information(username)  # gets information about specific user followers
    friends_location = get_location(data)  # gets name and location of friends
    create_map(friends_location)  # creates a map with friends_location info
```
## open_main_page()
This function is responsible for opening the main page where the entry field and button will be found
```python
@app.route('/')
def open_main_page():
    """
    Opens main page
    """
    return render_template('index.html')
```
## form_post()
This function is responsible for defining the entered in the entry form username
```python
@app.route('/display_map', methods=['POST'])
def form_post():
    """
    Posting the information in the form
    """
    username = request.form['nickname']
    main(username)
    return render_template("map.html")
```
## add_header()
This function is responsible for adding the header to the app and controlling cache
```python
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
```
## Web Page
http://rododendr0n.pythonanywhere.com/

<!> Web page is valid until May 16th
