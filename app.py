from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call backend

@app.route('/plan', methods=['POST'])
def generate_plan():
    data = request.json
    topic = data.get('topic', 'Python')
    current_level = data.get('current_level', 'beginner')
    days = int(data.get('days', 5))

    plan = []
    for i in range(1, days + 1):
        plan.append(f"Day {i}: Learn part {i} of {topic} (tailored for {current_level})")

    plan.append(f"Final Project: Build a small project using your new {topic} skills.")

    return jsonify({'plan': '\n'.join(plan)})

if __name__ == '__main__':
    app.run(debug=True)
