from flask import Flask, request, render_template, send_file
from gpt3_request import ask_gpt
from music import generate_music
import os

app = Flask(__name__)

#these are global variables, so define them here
response = []
filepath = ''
rhyme = ''

#the home page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html') #the initial form

#this is when you are presented with 5 possible options
@app.route("/choices", methods=['GET', 'POST'])
def options():
    #import these two
    global response
    global rhyme
    
    rhyme = request.form['nursery_rhyme']
    topic = request.form['topic']
    keywords = request.form['keywords'].split(",")
    
    #making the actual request to gpt
    response = ask_gpt(rhyme, topic, keywords)

    #intermediate.html renders the list of 5 options
    return render_template('intermediate.html', response=response, seq=[i for i in range(len(response))])
    
#the last page to visit
@app.route("/audio", methods=['GET', 'POST'])
def audio():
    #import these
    global response
    global filepath
    global rhyme
    
    # which option of the 5 song variants
    num = request.form["which_one"] 
    final_rhyme = response[int(num)] 

    filepath = generate_music(final_rhyme, rhyme)

    return render_template('download.html', final_rhyme=final_rhyme)

#actually serves the file to the user
@app.route("/download", methods=['GET', 'POST'])
def serve():
    global filepath
    return send_file(filepath, as_attachment=True)

if __name__=="__main__":
    app.run()
