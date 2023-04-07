from flask import Flask, request, render_template, send_file
from gpt3_request import ask_gpt
from music import generate_music
import os

app = Flask(__name__)

response = []
filepath = ''
rhyme = ''

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')
    
@app.route("/choices", methods=['GET', 'POST'])
def options():
    global response
    global rhyme
    rhyme = request.form['nursery_rhyme']
    topic = request.form['topic']
    keywords = request.form['keywords'].split(",")
    response = ask_gpt(rhyme, topic, keywords)

    return render_template('intermediate.html', response=response, seq=[i for i in range(len(response))])
    
@app.route("/audio", methods=['GET', 'POST'])
def audio():
    global response
    global filepath
    global rhyme
    num = request.form["which_one"] # which option of the 5 song variants
    final_rhyme = response[int(num)] 
    # print(final_rhyme)

    filepath = generate_music(final_rhyme, rhyme)
    # nfilepath = os.path.join('..', filepath)
    # print('filepath:')
    # print(nfilepath)


    return render_template('download.html', final_rhyme=final_rhyme)

@app.route("/download", methods=['GET', 'POST'])
def serve():
    global filepath

    return send_file(filepath, as_attachment=True)

if __name__=="__main__":
    app.run()