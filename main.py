from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import openai
openai.api_key = "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"
app = Flask(__name__)
from datetime import date, datetime
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///chat.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chat(db.Model):
    sno = db.Column(db.Integer,primary_key = True )
    user = db.Column(db.String(200), nullable = False)
    gpt = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.Integer, default=datetime.utcnow)

db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def hello():
    text = ""
    prompt = ""
    allChat=""
    if request.method == "POST":
        # helloworld = request.form["userInput"]
        prompt = request.form["userInput"]  
        response = openai.Completion.create(
        engine="ada",
        prompt=prompt,
        max_tokens=20, #Limited the Max Tokens to 20, Because of the Free Plan
        n=1,
        stop=None,
        temperature=0.5
        )
        text = response.choices[0].text
        print(prompt)

        userChat = Chat(user = prompt,gpt = text)
        db.session.add(userChat)
        db.session.commit()
        allChat = Chat.query.all() 

        
    return render_template('index.html',allChat=allChat)



if __name__ =='__main__':
    app.run(debug=True,port=5001)