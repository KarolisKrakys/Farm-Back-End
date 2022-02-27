from flask import Flask
from flask import request

app = Flask(__name__)

app = Flask(__name__)



@app.route('/', methods =['POST'])
def get_cordinates():
    cordinates = request.form.getlist('cords[]')
if __name__ == '__main__':
    app.run()
