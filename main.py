from flask import Flask, render_template, flash, redirect,request
from flask_restful import Resource, Api, reqparse
# from exp.nb_Copy import *
from model import make_model, translate
import torch
from os import listdir, environ
import pickle

app = Flask(__name__)

api = Api(app)

path = "model_s/new_model.pt"

model_pt = torch.load(path,map_location=torch.device('cpu'))

src = pickle.load( open( 'model_s/src.pkl', "rb" )) 
trg = pickle.load( open( 'model_s/trg.pkl', "rb" ))

modelp = make_model(src.n_words,trg.n_words,N=6)
modelp.load_state_dict(model_pt)

@app.route("/")
def home():
    return render_template("home.html")

class Translate(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str)

        args = parser.parse_args()
        text = args["text"]

        r_text = translate(text,modelp,src,trg)
        return r_text

api.add_resource(Translate,'/translate')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))