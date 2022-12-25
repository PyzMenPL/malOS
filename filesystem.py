import os
import sys
from folder import Folder
from file import File


class Filesystem:
    def __init__(self) -> None:
        self.root = Folder('/')
        # List of folder names
        self.current_directory = []

    def command(self, command) -> str:
        command = command.split()

        # If user inputs nothing
        if len(command) < 1:
            print("\tInvalid syntax: ", command)
            print("\tType 'help' to see all available commands")

            # Return
            if self.current_directory:
                return self.current_directory[-1]
            else:
                return '/'

        if command[0] == 'help':
            print("\tcd <path> - makes you enter the folder <path>")
            print("\tcd .. - makes you go back to parent directory")
            print("\tcd / - makes you go all the way back to root directory")
            print("\tclear - clears your screen")
            print("\texit - closes the program")
            print("\tls - prints all folders and files in current folder")
            print("\tls <path> - prints all folders and files in folder specified in path")
            print("\tmkdir <path> - creates directory inside current folder")
            print("\tmkfile <path> - creates empty file inside current folder")
            print("\tmkfile <path> <size> - creates file with specified size inside current folder")
            print("\tpwd - prints working directory")
            print("\trm <path> - removes everything from path")

        elif command[0] == 'cd':
            if command[1] == '..':
                # If there is a folder you can go back to
                if self.current_directory:
                    del self.current_directory[-1]
                else:
                    print("\tYou can't go back further!")
            else:
                self.cd(command[1].split('/'))

        elif command[0] == 'ls':
            # If user specified path
            if len(command) == 2:
                # We assume that user is more likely to ls without '/' at the start of the path :D
                path = self.current_directory[:]

                # If our path starts in root
                if command[1][0] == '/':
                    path = []

                # Add every folder to path
                for item in command[1].split('/'):
                    if item != '':
                        path.append(item)

                # If user wants to print '/' directory
                if path == ['', '']:
                    path = []

                self.root.print(path)

            # If user didn't specify path
            else:
                self.root.print(self.current_directory[:])

        # Add directory or file if it doesn't exist
        elif command[0] == 'mkdir':
            # If the name of the folder is not given
            if command[-1] == "mkdir":
                print("\tProvide folder name!")
            else:
                # Declaring variables
                folders = []
                path_to_pass = self.current_directory[:]

                # If the folder names starts with '/' create them in root directory
                if command[1][0] == "/":
                    path_to_pass = []

                # Save directories in list
                for folder in command[1].split("/"):
                    if folder != '':
                        folders.append(Folder(folder))

                # If user wants to create root directory
                if command[1].split("/") == ['', '']:
                    print("\t'/' directory can only be one!")

                else:
                    # Add folders
                    self.root.add(folders, path_to_pass)

        elif command[0] == 'mkfile':
            path = self.current_directory[:]
            user_input = command[1].split("/")

            if '/' in command[1]:
                if command[1][0] == '/':
                    path = []

                for element in user_input:
                    if element != '':
                        path.append(element)

                # Because it is the name of the file we want to add
                del path[-1]

            # User specified name only
            if len(command) == 2:
                file = File(user_input[-1], 0)
                self.root.add(file, path)

            # User specified both parameters
            elif len(command) == 3:
                # Make sure user typed number
                if command[2].isdigit():
                    file = File(user_input[-1], int(command[2]))
                    self.root.add(file, path)
                else:
                    print("\tSpecified size is not a number!")

        elif command[0] == 'pwd':
            if not self.current_directory:
                print("\t/")
            else:
                print("\t/" + "/".join(self.current_directory))

        elif command[0] == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')

        elif command[0] == "exit":
            sys.exit()

        elif command[0] == "rm":
            if len(command) == 2:
                path = self.current_directory[:]

                if command[1][0] == '/':
                    path = []

                for item in command[1].split('/'):
                    if item != '':
                        path.append(item)

                if command[1].split('/') == ['', '']:
                    # Maybe some funny Easter egg here?
                    print("\tYou sussy baka!")
                else:
                    file = path.pop(-1)
                    self.root.delete(file, path)
            else:
                print("\tSpecify path!")

        else:
            print("\tInvalid syntax: ", end='')
            for word in command:
                print(word, end=" ")
            print()
            print("\tType 'help' to see all available commands")

        # Return
        if self.current_directory:
            return self.current_directory[-1]
        else:
            return '/'

    def cd(self, dst_name: list) -> None:
        # If we want to go to root directory
        if dst_name == ['', '']:
            self.current_directory = []

        # If we want to go to directory different from root
        else:
            # Creating the full path to destination folder (current_dirs)
            current_dirs = self.current_directory[:]

            for folder in dst_name:
                current_dirs.append(folder)

            result = self.root.goto(current_dirs[:])

            # If result is true this means that all folders exist
            if result:
                self.current_directory = current_dirs
                print("\tFolder changed successfully!")
