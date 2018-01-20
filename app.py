#!/usr/bin/python3
import flask
from shelljob import proc

app = flask.Flask(__name__)
g = proc.Group()
p = g.run( [ "rtl_433", "-G" ] )

@app.route( '/' )
def index():
    html_header = """ <!DOCTYPE html>
	<html>
	<head>
	<title>433.92 MHz Live Stream</title>
	<style>
	body { background-color: #111; color: #eee; }
	h1 { color: #ffe; }
	pre {
	font: Consolas, monospace;
	font-size: 13px;
	}
	</style>
	</head>
	<body>
        <h1>rtl_433 Live Webstream</h1>
	<pre>"""

    def read_process():
        yield html_header
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return flask.Response( read_process(), mimetype='text/html' )

app.run(debug=True, port=5000, host='0.0.0.0')
