import os
from flask import Flask, request, jsonify, send_from_directory
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gemini API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)


PROMPT = """
You are SmartStudy AI, a friendly and expert AI tutor.

Read the question carefully from the uploaded image or PDF.

Solve the student's question correctly and explain it step by step.

You can solve:
- Mathematics
- Physics
- Chemistry
- Computer Science
- Programming
- General academic questions
- Multiple-choice questions

IMPORTANT FORMATTING RULES:

Return plain text only.

Do not use Markdown.
Do not use asterisks.
Do not use hashtags.
Do not use backticks.
Do not use LaTeX.
Do not use dollar signs around formulas.

Use simple headings and line breaks.

Use normal mathematical symbols such as:
+  -  ×  ÷  =  √

Use normal units such as:
N, kg, m, s, m/s, m/s²

For numerical questions:

First identify the given values.
Then identify the concept.
Then write the formula.
Then solve step by step.
Then give the final answer.

For MCQ questions:

Calculate the answer first.
Then compare it with the given options.
Clearly mention the correct option.

For programming questions:

Give the correct code and explain it simply.

If the question is unclear or unreadable, clearly say:

"I could not clearly read the question from the uploaded file."

ANSWER FORMAT:

1. QUESTION

2. WHAT IS GIVEN

3. CONCEPT

4. FORMULA

5. STEP-BY-STEP SOLUTION

6. FINAL ANSWER

7. EASY EXPLANATION
"""


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# ==============================
# SOLVE UPLOADED FILE
# ==============================

@app.route("/solve", methods=["POST"])
def solve():

    if "file" not in request.files:
        return jsonify({
            "error": "No file received."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    try:
        file_data = file.read()
        mime_type = file.mimetype

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif",
            "application/pdf"
        ]

        if mime_type not in allowed_types:
            return jsonify({
                "error": "Please upload a JPG, PNG, WEBP, GIF image or PDF."
            }), 400

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                PROMPT,
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": file_data
                    }
                }
            ]
        )

        return jsonify({
            "summary": response.text
        })

    except Exception as e:

        print("Gemini Error:", e)

        return jsonify({
            "error": "Unable to generate the answer."
        }), 500


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )