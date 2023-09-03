from flask import Flask, request, render_template
import pickle as pk
import models #Models.py written for models
import helper # Helper.py written to help with functions to make code cleaner 

app = Flask(__name__)
ADMIN_PASSWORD = "admin"

@app.route("/")
@app.route("/home")
def auth_index():
    return render_template("index.html")

@app.route('/admin', methods = ["POST", "GET"])
def admin_page():
    if request.method == 'POST':
        verification = request.form.get('admin_password')
        if verification == ADMIN_PASSWORD:
            db_list = helper.admin_load("db.pk")
            return render_template('admin.html', my_dict=db_list)
        else:
            return "Access denied"
    else:
        return '''
        <form method="POST">
            <label for="admin_password">ENTER ADMIN PASSWORD: </label>
            <input type="text" id="admin_password" name="admin_password">
            <input type="submit" value="Submit">
        </form>
        '''

BASE_IMG = None
CURR_USER = None
AUTH_SCOPE = None

@app.route('/authenticate_one', methods = ["POST"])
def authenticate_one():
    global AUTH_SCOPE
    creds = request.form.to_dict()
    username = creds['username']
    #print(username)
    password = creds['password']
    AUTH_SCOPE = creds['authscope']
    with open('db.pk', "rb") as f:
        creds_db = pk.load(f)
        user_list = [d['username'] for d in creds_db]
        if username not in user_list:
            return render_template("index.html", invalid = True)
        elif creds_db[user_list.index(username)]['password'] != password:
            return render_template("index.html", invalid = True)
        else:
            #print(creds_db)
            global BASE_IMG 
            BASE_IMG = creds_db[user_list.index(username)]['img']
            return render_template("camera-img.html", username = username)

@app.route('/image_upload', methods = ["POST", "GET"])
def upload_img():
    global CURR_USER
    if request.method == 'POST':
        data = request.files['image']
        CURR_USER = request.form['username']
        #print(CURR_USER)
        data.save('image.jpg')
        return "Upload successful"
    
@app.route('/authenticate_two')
def success():
    global CURR_USER
    global BASE_IMG
    if str(BASE_IMG) == 'None':
        return render_template("index.html", restart = True)
    #print(CURR_USER)
    if AUTH_SCOPE == 'hist':
        granted = models.hist_classify("image.jpg", BASE_IMG)
    elif AUTH_SCOPE == 'sift':
        granted = models.sift_classify("image.jpg", BASE_IMG)
    else:
        granted = models.siamese_classify("image.jpg", BASE_IMG)

    if granted:
        #helper.update_db(access_nature="granted", db = "db.pk", username=CURR_USER)
        return render_template("result.html", access = "Granted", username = CURR_USER)
    else:
        #helper.update_db(access_nature="denied", db = "db.pk", username=CURR_USER)
        return render_template("result.html", access = "Denied", username = CURR_USER)


