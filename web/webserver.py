#!/usr/bin/python3

import time
from flask import Flask, render_template, request, redirect, url_for, make_response

class Server:
    
    outputs = []

    def __init__(self, outputs=[]):
        self.outputs = outputs
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template('index.html', outputs=outputs)

        @app.route('/<outputName>', methods=['POST'])

        def reroute(outputName):
            found = False
            for o in outputs:
                if outputName == o.name():
                    o.toggle()
                    found = True
               
            if not found:
                [ o.off() for o in outputs ]
            
            response = make_response(redirect(url_for('index')))
            
            return(response)

        #app.run(debug=False, host='0.0.0.0', port=8080)
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)