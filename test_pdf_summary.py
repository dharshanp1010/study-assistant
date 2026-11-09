from services.summary_service import summarize_pdf_note


def main():

    summary = summarize_pdf_note(
        relative_path="machine_learning/linear_regression.pdf",
        subject="Machine Learning"
    )
    print(summary)
    
if __name__ == "__main__":
    main()