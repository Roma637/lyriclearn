from flask import Flask, request, render_template
from gpt3_request import ask_gpt

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        rhyme = request.form['nursery_rhyme']
        topic = request.form['topic']
        keywords = request.form['keywords']
        response = ask_gpt(rhyme, topic, keywords)
        return(response)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run()