from services.notes_service import read_pdf_note


def main():

    content = read_pdf_note(
        "machine_learning/linear_regression.pdf"
    )
    print(content)
    


if __name__ == "__main__":
    main()