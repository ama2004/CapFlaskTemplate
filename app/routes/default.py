from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/formsyoungpeople')
def formsyoungpeople():
    return render_template('formsyoungpeople.html')  

@app.route('/formsorganizations')
def formsorganizations():
    return render_template('formsorganizations.html')  

@app.route('/stemresources')
def stemresources():
    return render_template('stemresources.html')  