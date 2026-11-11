from graph.nodes import mcq_node

test_state={
    "request_type": "mcq",
    "subject": "Machine Learning",
    "num_questions": 5,
    "difficulty": "Intermediate",
    "note_path": "machine_learning/linear_regression.pdf"
}
result=mcq_node(test_state)
quiz = result["response"]
print(quiz)
print("Quiz Title:", quiz.title)

for index, question in enumerate(quiz.questions, start=1):

    print(f"\nQ{index}. {question.question}")

    for option_index, option in enumerate(
        question.options, start=1
    ):
        print(f"   {option_index}. {option}")

    print("Correct Answer:", question.correct_answer)
    print("Explanation:", question.explanation)
