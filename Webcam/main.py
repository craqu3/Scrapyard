from flask import Flask, render_template, Response
from webcam import webcam

app = Flask(__name__, template_folder="./templates",static_folder='./static')

@app.route('/')
def index():
    return render_template('home.html')

g = webcam()

@app.route('/video')
def video():
    return Response(g, mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
