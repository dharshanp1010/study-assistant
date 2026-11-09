from services.notes_service import read_note


def main():

    content = read_note(
        "machine_learning/linear_regression.md"
    )

    print(content)

if __name__ == "__main__":
    main()