from flask import Flask,request,render_template,flash
from flask_wtf.csrf import generate_csrf
from app.routes import simple_page
from flask_cors import CORS
from app.routesImage import verificate
app = Flask(__name__)
CORS(app)
#app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['UPLOAD_FOLDER'] = "videos"
app.register_blueprint(simple_page)
app.register_blueprint(verificate)

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return {'csrf_token': csrf_token}



@app.route('/', methods=['POST','GET'])
def index():
  if request.method == 'GET':
    return render_template('hello.html', msg = 'Hello World')
'''
if __name__ == '__main__':
   from waitress import serve
   serve(app, host='127.0.0.1', port=80)
'''