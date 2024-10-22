from flask import  render_template, request
from . import app
# Define the host and port for the server
host = '0.0.0.0'
port = 5000

# Create the Flask app

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    if request.method == 'POST':
        name = request.form['name']

    return render_template('hello.html', name = (name or 'Meow'))

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)

