import sys


def command(arg):
    if arg[1] == "file":
        with open(arg[2], "r") as file:
            print(file.read())
    elif arg[1] == "text":
        text = " ".join(arg[2:])
        print(text)
    else:
        print("Invalid command:(")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py file/text text/file_name")
        sys.exit(1)
    else:
        command(sys.argv)

# comanda e cv de genul: "python main.py file data.txt" sau "python main.py text ceva_text"
