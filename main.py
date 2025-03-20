from flask import Flask, render_template, Response
from webcam import webcam

app = Flask(__name__, template_folder="./templates", static_folder='./static', static_url_path='')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dicas.html')
def dicas():
    return render_template('dicas.html')

@app.route('/dicas2.html')
def dicas2():
    return render_template('dicas2.html')

@app.route('/video')
def video():
    return Response(webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
