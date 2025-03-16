from flask import Flask, render_template, Response
from webcam import webcam

app = Flask(__name__, template_folder="./templates", static_folder='./static', static_url_path='')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/video')
def video():
    return Response(webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
