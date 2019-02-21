

from flask import Flask, render_template , request , redirect, url_for, make_response, abort
from pprint import pprint
import os
import json
import requests

app = Flask(__name__) #app is flask object, we pass in name to help out flask    



# url
def _url(path):
    return 'https://hunter-todo-api.herokuapp.com/' + path

@app.route('/') 
def login():
	return render_template('login.html')

#Personal page
@app.route('/profile') 
def profile():
	return render_template('profile.html')

# 1 Create a User
@app.route('/login/post', methods=['POST']) 
def create_user():
	newUsername = request.form['newUsername']
	if (newUsername ==""):
		return make_response("Please enter a username" '<a href ="/"> Home</a>')
	requests.post(_url('user'), json= {'username' : newUsername})
	resp = make_response("You were able to register!" '<a href ="/"> Home</a>')
	return resp

#2 authenticate user
@app.route("/auth", methods=['POST'])
def authenticate_Username():
    authUsername = request.form['authUsername']
    if (authUsername == ""):
        return make_response("Please enter a username "'<a href="/">Home</a>')
    req = requests.post(_url('auth'), json={'username': authUsername})
    json_data = req.json()
    try:
        token = json_data['token']
    except:
        token = ""
    if (token == ""):
        return make_response("Please try again. The username wasn't found "'<a href="/"> Home</a>')
    redirect_to_root = redirect('/')
    resp = make_response("You successfully logged in!" '<a href="/">Home</a>')
    resp.set_cookie('sillyauth', value=token)
    return resp

#3 Create a New Item
@app.route("/create_item", methods=['POST'])
def create_item():
    cookies = request.cookies
    newItem = request.form['newItem']
    if (newItem == ""):
        return make_response("Please try again. Input is empty"
                             '<a href="/">Home</a>')
    requests.post(
        _url('todo-item'), cookies=cookies, json={'content': newItem})
    return make_response("Item was successfully created. " '<a href="/">Home</a>')


 #4 View all items for a user

@app.route("/get_items_id")
def get_items_id():
    cookies = request.cookies
    resp = requests.get(_url('todo-item'), cookies=cookies)
    return resp.text

#5 Change some data on an item
@app.route("/change_item", methods=['POST'])
def change_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    newItem = request.form['newItem']
    if (itemID == "" or newItem == ""):
        return make_response("Please try again.Input is empty "
                             '<a href="/">Home</a>')
    data = '{"content": "' + newItem + '"}'
    requests.put(_url('todo-item/') + itemID, cookies=cookies, data=data)
    return make_response("Item successfully changed. " '<a href="/">Home</a>')

# 6 Delete an item
@app.route("/delete_item", methods=['POST'])
def delete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Input is empty. Please try again. "
                             '<a href="/">Home</a>')
    requests.delete(_url('todo-item/') + itemID, cookies=cookies)
    return make_response("Item successfully deleted. " '<a href="/">Home</a>')


#7 Mark an item as completed
@app.route("/complete_item", methods=['POST'])
def complete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Input is empty. Please try again. "
                             '<a href="/">Home</a>')
    requests.put(
        _url('todo-item/') + itemID, cookies=cookies, json={'completed': True})
    # if(itemID !=)
    return make_response("Item successfully marked as completed. "
                         '<a href="/">Home</a>')

# Logout
@app.route("/logout")
def logout():
    resp = make_response("You've successfully logged out. "
                        '<a href="/">Home</a>')
    resp.set_cookie('sillyauth', expires=0)
    return resp





if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True, debug=True)





