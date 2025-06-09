#!/usr/bin/python3

import time
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import logging

class Server:
    outputs = []

    def __init__(self, outputs : [], armAction, disarmAction, resetAction):
        outputs = [output for output in outputs if output.name() != 'unused']

        self.outputs = outputs
        app = Flask(__name__)
        app.config['TEMPLATES_AUTO_RELOAD'] = True # auto reload template

        @app.route('/')
        def index():
            return render_template('index.html', outputs=outputs)

        def determine_output(outputName):
            found = False
            for o in outputs:
                if outputName == o.name():
                    return o
            return None

        @app.route('/outputs/', methods=['GET'])
        def output_list():
            logging.debug(f"Requested URL: {request.url}")

            status = {}
            for output in outputs:
              status[output.name()] = output.is_on()
            
            return make_response(jsonify(status))

        @app.route('/outputs/<outputName>/<action>', methods=['GET'])
        def output_get(outputName: str, action: str):
            output = determine_output(outputName)
            if not output:
              return jsonify({"error": f"No output found for {outputName}"}), 400
            
            logging.debug(f"Requested URL: {request.url}")

            if action == "get":
              return jsonify({"status": output.is_on()}), 200
            elif action == "on":
              output.on()
              return '', 200
            elif action == "off":
              output.off()
              return '', 200
            elif action == "toggle":
              output.toggle()
              return '', 200
            
            return jsonify({"error": f"Invalid action '{action}'"}), 400

        
        @app.route('/armDisarm/<action>', methods=['POST'])
        def arm_disarm(action):
            logging.debug(f"Requested URL: {request.url}")
            if action == 'ARM':
              armAction()
            elif action == 'DISARM':
              disarmAction()
            elif action == 'RESET':
              resetAction()
            
            return jsonify({"status": "ok"})

        #app.run(debug=False, host='0.0.0.0', port=8080)
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)