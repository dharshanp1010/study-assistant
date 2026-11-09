from services.quiz_service import generate_mcq_quiz


def main():

    quiz = generate_mcq_quiz(
        relative_path="machine_learning/linear_regression.pdf",
        subject="Machine Learning",
        num_questions=5,
        difficulty="Intermediate"
    )

    print("\n========== GENERATED QUIZ ==========")
    print(f"\nQuiz: {quiz.title}")

    for index, question in enumerate(
        quiz.questions,
        start=1
    ):

        print(f"\nQ{index}. {question.question}")

        for option_index, option in enumerate(
            question.options,
            start=1
        ):
            print(f"   {option_index}. {option}")

        print(f"\nCorrect Answer: {question.correct_answer}")
        print(f"Explanation: {question.explanation}")

   


if __name__ == "__main__":
    main()