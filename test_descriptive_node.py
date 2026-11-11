from graph.nodes import descriptive_node

test_state ={
        "request_type": "descriptive",
    "subject": "Machine Learning",
    "note_path": "machine_learning/linear_regression.pdf",
     "difficulty": "Intermediate",
    "num_questions": 3,
    "marks_per_question": 5
}

result = descriptive_node(test_state)
quiz = result["response"]
for index, question in enumerate(quiz.questions, start=1):

    print(f"\nQ{index}. {question.question}")

    print("Marks:", question.marks)

    print("\nExpected Answer:")
    print(question.expected_answer)

    print("\nKey Points:")

    for point in question.key_points:
        print("-", point)
