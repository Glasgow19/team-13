from flask import Flask, render_template, request, redirect

# setup flask
app = Flask(__name__)

@app.route('/')
def calender():
	return render_template('calendar.html', test="testing")

if __name__ == "__main__":
	# start server
	app.run(port=8000, debug=False)
