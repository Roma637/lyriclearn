from flask import Flask, request, render_template, send_file
from gpt3_request import ask_gpt
from music import generate_music

app = Flask(__name__)

response = []
filepath = ''

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')
    
@app.route("/choices", methods=['GET', 'POST'])
def options():
    global response
    rhyme = request.form['nursery_rhyme']
    topic = request.form['topic']
    keywords = request.form['keywords']
    response = ask_gpt(rhyme, topic, keywords)

    return render_template('intermediate.html', response=response, seq=[i for i in range(len(response))])
    
@app.route("/audio", methods=['GET', 'POST'])
def audio():
    global response
    global filepath
    num = request.form["which_one"]
    final_rhyme = response[int(num)]
    print(final_rhyme)

    filepath = generate_music(final_rhyme, num)

    return render_template('download.html')

@app.route("/download")
def serve():
    global filepath
    return send_file(filepath, as_attachment=True)

if __name__=="__main__":
    app.run()