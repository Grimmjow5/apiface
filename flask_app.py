from flask import Flask,request,render_template,flash
from flask_wtf.csrf import generate_csrf
from app.routes import simple_page
from flask_cors import CORS
from app.routesImage import verificate
apps = Flask(__name__)
cors = CORS(apps,supports_credentials=True)
#apps.config['SECRET_KEY'] = 'tu_clave_secreta'
apps.config['UPLOAD_FOLDER'] = "videos"
apps.register_blueprint(simple_page)
apps.register_blueprint(verificate)

'''
@apps.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return {'csrf_token': csrf_token}
'''


@apps.route('/', methods=['POST','GET'])
def index():
  if request.method == 'GET':
    return render_template('hello.html', msg = 'Hello World')

if __name__ == '__main__':
   apps.run(debug=True,host='0.0.0.0')
   '''
   from waitress import serve
   serve(apps, host='0.0.0.0', port=8000)
   '''
