from filesystem import Filesystem

if __name__ == "__main__":
    print("Type 'help' to see all available commands")
    fastFS = Filesystem()
    current_folder = "/"

    while True:
        current_folder = fastFS.command(input(current_folder + ' $ '))
