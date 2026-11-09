from services.quiz_service import generate_descriptive_quiz


def main():

    quiz = generate_descriptive_quiz(
        relative_path="machine_learning/linear_regression.pdf",
        subject="Machine Learning",
        num_questions=3,
        difficulty="Intermediate",
        marks_per_question=5
    )

    print(f"\nQuiz: {quiz.title}")

    for index, question in enumerate(
        quiz.questions,
        start=1
    ):

        print(f"\nQ{index}. {question.question}")

        print(f"Marks: {question.marks}")

        print("\nExpected Answer:")
        print(question.expected_answer)

        print("\nKey Points:")
        for point in question.key_points:
            print(f"- {point}")

    print("\n======================================")


if __name__ == "__main__":
    main()