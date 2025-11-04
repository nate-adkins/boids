from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!doctype html>
<html>
<head>
  <title>My Flask GUI</title>
</head>
<body>
  <h1>Hello from Flask!</h1>
  <button onclick="alert('Button clicked!')">Click Me</button>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
