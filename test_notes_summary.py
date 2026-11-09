from services.summary_service import summarize_note


def main():

    summary = summarize_note(
        relative_path="machine_learning/linear_regression.md",
        subject="Machine Learning"
    )

    print(summary)
   

if __name__ == "__main__":
    main()