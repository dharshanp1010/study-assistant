
from graph.workflow import study_assistant_graph


def display_menu():

    print("\n========== PERSONAL AI STUDY ASSISTANT ==========")

    print("1. Ask a Question")
    print("2. Summarize Study Notes")
    print("3. Generate MCQ Quiz")
    print("4. Generate Descriptive Quiz")
    print("5. Exit")

    choice = input("\nEnter your choice: ")

    return choice


def get_common_note_inputs():

    subject = input("Enter the subject: ")
    note_path = input("Enter the note file path: ")

    return subject, note_path


def run_study_assistant(state):

    try:
        # Execute the LangGraph workflow
        result = study_assistant_graph.invoke(state)
        print(result.get("response", "No response generated."))

    except Exception as e:

        print("\nAn error occurred:", e)


def main():

    while True:

        choice = display_menu()
        # Option 1: Question Answering
        if choice == "1":

            subject = input("Enter the subject: ")
            question = input("Enter your question: ")

            level = input("Enter difficulty level (Beginner/Intermediate/Advanced): "
            )

            if not level.strip():
                level = "Intermediate"

            state = {
                "request_type": "question",
                "subject": subject,
                "question": question,
                "level": level
            }

            run_study_assistant(state)

        # Option 2: Summarization
        elif choice == "2":

            subject, note_path = get_common_note_inputs()

            state = {
                "request_type": "summary",
                "subject": subject,
                "note_path": note_path
            }

            run_study_assistant(state)

        # Option 3: MCQ Quiz
        elif choice == "3":

            subject, note_path = get_common_note_inputs()

            difficulty = input("Enter difficulty (Easy/Medium/Hard): ")

            num_questions = int(
                input("Enter number of questions: ")
            )

            state = {
                "request_type": "mcq",
                "subject": subject,
                "note_path": note_path,
                "difficulty": difficulty,
                "num_questions": num_questions
            }

            run_study_assistant(state)

        # Option 4: Descriptive Quiz
        elif choice == "4":

            subject, note_path = get_common_note_inputs()

            difficulty = input("Enter difficulty (Easy/Medium/Hard): ")

            num_questions = int(
                input("Enter number of questions: ")
            )

            marks_per_question = int(
                input("Enter marks per question: ")
            )

            state = {
                "request_type": "descriptive",
                "subject": subject,
                "note_path": note_path,
                "difficulty": difficulty,
                "num_questions": num_questions,
                "marks_per_question": marks_per_question
            }

            run_study_assistant(state)

        # Option 5: Exit
        elif choice == "5":

            print("\nThank you for using Personal AI Study Assistant!")
            break

        else:

            print("\nInvalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":

    main()
