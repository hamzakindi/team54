from flask import Flask, request, jsonify
import janus_swi as janus
import os

app = Flask(__name__)

# Load the Prolog file with correct path
prolog_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          'ruleset', 'test_recommendations.pl')
janus.consult(prolog_file)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        probability = data.get('probability', 0)
        
        # Query the Prolog knowledge base
        query = f"get_test_recommendations({probability}, Category, Tests)"
        results = list(janus.query(query))
        
        if results:
            # Get the first result since our Prolog rule returns one category
            result = results[0]
            return jsonify({
                "status": "success",
                "category": result["Category"],
                "tests": result["Tests"]
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No recommendations found for given probability"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=8001, debug=True)