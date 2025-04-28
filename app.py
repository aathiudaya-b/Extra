from flask import Flask, request, jsonify
import requests
import dialogflow_v2 as dialogflow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# YouTube API
def get_youtube_links(query):
    API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API key
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={API_KEY}"
    response = requests.get(url)
    items = response.json().get("items", [])
    video_links = []
    for item in items:
        video_links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
    return video_links


# FreeCodeCamp Resources (Simplified)
def get_freecodecamp_resources(topic):
    # Placeholder: Replace with actual FreeCodeCamp API or scraped resources
    return [f"https://www.freecodecamp.org/news/{topic}/"]


# Dialogflow Agent Integration
def chat_with_agent(text):
    project_id = "YOUR_DIALOGFLOW_PROJECT_ID"  # Replace with your Dialogflow Project ID
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, "unique-session-id")

    text_input = dialogflow.types.TextInput(text=text, language_code="en")
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text


@app.route("/plan", methods=["POST"])
def generate_plan():
    data = request.json
    topic = data.get("topic", "Python")
    current_level = data.get("current_level", "beginner")
    days = int(data.get("days", 5))

    plan = []
    for i in range(1, days + 1):
        plan.append(
            f"Day {i}: Learn part {i} of {topic} (tailored for {current_level})"
        )

    plan.append(f"Final Project: Build a small project using your new {topic} skills.")

    # Fetch YouTube videos for the tech topic
    youtube_links = get_youtube_links(topic)
    plan.append(f"\nYouTube Learning Resources:\n")
    for link in youtube_links:
        plan.append(link)

    # Add FreeCodeCamp Resources
    freecodecamp_links = get_freecodecamp_resources(topic)
    plan.append(f"\nFreeCodeCamp Resources:\n")
    for link in freecodecamp_links:
        plan.append(link)

    return jsonify({"plan": "\n".join(plan)})


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    agent_reply = chat_with_agent(user_message)
    return jsonify({"reply": agent_reply})


if __name__ == "__main__":
    app.run(debug=True)
