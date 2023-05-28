
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "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"

questions = [
    "What industries are you interested in?",
    "What do you enjoy doing the most?",
    "What skills do you possess?",
    "Which field of knowledge interests you the most?",
    "How do you feel about working in a team?",
    "What's more important to you: career or work-life balance?",
    "What important qualities should your future profession have?",
    "Do you value the opportunity to travel while working?",
    "How do you react to stressful situations?",
    "How do you handle challenges and problems at work?",
    "How do you envision your future career in 5 years?",
    "Are you interested in working with new technologies?",
    "What values are you looking for in your professional activity?",
    "How do you feel about changes in the work environment?",
    "Is it important for you to have the opportunity to learn and develop in your profession?",
    "How do you organize your work time and tasks?",
    "How do you feel about working at a high pace?",
    "How do you feel about working with data and analytics?",
    "Are you interested in working with clients and customer service?",
    "How do you approach the creative process at work?",
]

options = [
    ["Technology", "Art", "Business"],
    ["Creativity", "Analytics", "Communication"],
    ["Programming", "Design", "Project Management"],
    ["Science", "Medicine", "Finance"],
    ["Very positive", "Depends on the situation", "Prefer working alone"],
    ["Career", "Work-life balance", "Both equally important"],
    ["Creativity", "Leadership", "Communication skills"],
    ["Yes, it's very important", "Desirable, but not necessary", "Doesn't affect my career choice"],
    ["I cope well", "I partially cope", "I struggle to cope"],
    ["I find solutions", "I seek help from colleagues", "Stress doesn't affect me"],
    ["I find solutions", "I seek guidance from management", "I face difficulties"],
    ["Stable position in a large company", "Starting my own business", "Working abroad"],
    ["Yes, it's my hobby", "I'm interested in trying it out", "Not interested"],
    ["Self-fulfillment", "Financial stability", "Social responsibility"],
    ["I resist changes", "I embrace them with understanding", "I enjoy changes"],
    ["Yes, it's very important", "Partially important", "Not important"],
    ["I set realistic goals", "I prioritize tasks", "I adapt to the situation"],
    ["I work well in a fast-paced environment", "I adapt easily to changes", "I struggle with a high pace"],
    ["Very interested", "Partially interested", "Not interested"],
    ["Yes, it's important", "Partially important", "Not important"],
    ["Very interested", "I enjoy standard routines", "Depends on the task"],
]

# Save user's answers
answers = []

@app.route('/', methods=['POST'])
def process_question():
    data = request.get_json()
    question_index = data['question_index']
    selected_option = data['selected_option']

    # Save the user's answer
    answers.append(selected_option)

    # Check if all questions have been answered
    if question_index < len(questions):
        question = questions[question_index]
        option1 = options[question_index][0]
        option2 = options[question_index][1]
        option3 = options[question_index][2]
        return jsonify({'question': question, 'option1': option1, 'option2': option2, 'option3': option3})
    else:
        # Get career recommendations based on user's answers
        results = get_results(answers)
        return jsonify({'results': results})

def get_results(answers):
    # Build the text for the query to the GPT-3.5 model
    prompt = "Career Orientation Test:\n\n"
    for i, ans in enumerate(answers):
        prompt += f"Question {i+1}: {questions[i]}\n"
        prompt += f"Your answer: Option {ans+1}\n\n"

    # Call the GPT-3.5 model to get career recommendations
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=3,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Get the list of recommended professions
    recommendations = [choice['text'].strip() for choice in response['choices']]
    return recommendations

if __name__ == '__main__':
    app.run()
