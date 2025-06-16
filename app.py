from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from mockdata import featured_prompts, categories

app = Flask(__name__)

# Initialize Gemini API
genai.configure(api_key="AIzaSyDwEYdGEuukG4FUl2YRfQ9KF3ml5eRMbm8")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to enhance prompt using Gemini API
def enhance_prompt(prompt):
    try:
        response = model.generate_content(
            f"Enhance the following prompt to be more detailed, specific, and optimized for better AI outputs. Include context, target audience, tone, and actionable instructions: '{prompt}'"
        )
        return response.text
    except Exception as e:
        return f"Error: Failed to enhance prompt: {str(e)}"

@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("search", "").lower()
    selected_category = request.args.get("category", "All")

    # Filter prompts based on search and category
    filtered_prompts = [
        prompt for prompt in featured_prompts
        if (search_query in prompt["title"].lower() or
            search_query in prompt["description"].lower() or
            any(search_query in tag.lower() for tag in prompt["tags"])) and
        (selected_category == "All" or prompt["category"] == selected_category)
    ]

    return render_template(
        "index.html",
        prompts=filtered_prompts,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query
    )

@app.route("/enhance", methods=["POST"])
def enhance():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400
    
    try:
        enhanced_prompt = enhance_prompt(prompt)
        return jsonify({"enhanced_prompt": enhanced_prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)