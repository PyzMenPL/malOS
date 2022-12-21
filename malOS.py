import os
import sys


class Filesystem:
    def __init__(self) -> None:
        self.root = Folder('/')
        # List of folder names
        self.current_directory = []

    def command(self, command) -> None:
        command = command.split()

        # If user inputs nothing
        if len(command) < 1:
            print("\tInvalid syntax: ", command)
            print("\tType 'help' to see all available commands")
            return

        if command[0] == 'help':
            print("\tcd <name> - makes you enter the folder <name>")
            print("\tcd .. - makes you go back to parent directory")
            print("\tcd / - makes you go all the way back to root directory")
            print("\tls - prints all folders and files in system")
            print("\tmkdir <name> - creates directory inside current folder")
            print("\tmkfile <name> - creates empty file inside current folder")
            print("\tmkfile <name> <size> - creates file with specified size inside current folder")
            print("\tpwd - prints working directory")
            print("\texit - closes the program")

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
            self.root.print()

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

                # Add folders
                self.root.add(folders, path_to_pass)
                print("\tFolder '" + command[1] + "' created successfully!")

        elif command[0] == 'mkfile':
            path = self.current_directory[:]
            user_input = command[1].split("/")
            file = None

            if '/' in command[1]:
                if command[1][0] == '/':
                    path = []

                for element in user_input:
                    if element != '':
                        path.append(element)

            # User specified name only
            if len(command) == 2:
                file = File(user_input[-1], 0)

            # User specified both parameters
            elif len(command) == 3:
                file = File(user_input[-1], command[2])

            self.root.add(file, path[:-1])
            print("\tFile '" + command[1] + "' created successfully!")

        elif command[0] == 'pwd':
            if not self.current_directory:
                print("\t/")
            else:
                print("\t/" + "/".join(self.current_directory))

        elif command[0] == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')

        elif command[0] == "exit":
            sys.exit()

        else:
            print("\tInvalid syntax: ", end='')
            for word in command:
                print(word, end=" ")
            print()
            print("\tType 'help' to see all available commands")
            return

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


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
        self.is_created = False

    def __str__(self) -> str:
        return "═ {} ({}, size={})".format(self.name, "file", self.size)

    def __repr__(self) -> str:
        # Instead of printing out <class 'str'>, it prints out as follows
        return "File '{}'".format(self.name)


class Folder(File):
    # Folder is a child of the File class (takes its name and size from it)
    def __init__(self, name: str) -> None:
        # The same as self.name = name and self.size = size
        super().__init__(name=name, size=0)
        self.contains = []

    def __iter__(self) -> object:
        # If iteration starts, we start from zero
        self.index = 0
        # We end up with the last item on the list
        self.limit = len(self.contains)
        return self

    def __next__(self) -> object:
        # If next() is called we increment the index
        self.index += 1

        # If the index is already out of the list, we abort the iteration
        if self.index == self.limit + 1:
            raise StopIteration

        # If the index is in the range of the list, we return the list element
        return self.contains[self.index - 1]

    def __str__(self) -> str:
        # If we need a folder name
        if self.size == 0:
            return "╦═ {} (dir)".format(self.name)
        else:
            return "╦═ {} (dir, size={})".format(self.name, self.size)

    def __repr__(self) -> str:
        # Instead of printing out <class 'str'>, it prints out as follows
        return "Folder '{}'".format(self.name)

    # path can be list of folder or single file
    def add(self, path, dst_folder_path) -> None:
        # If it reaches the destination folder, it saves the file.
        # If the condition did not check if the file was created, it would still be saved in the wrong places

        # If we reached our destination
        if not dst_folder_path:
            # If path is a file
            if isinstance(path, type(File('', 0))):
                # The file is added to desired folder and to all parent directories
                # If the desired folder is not found the file is added to the first folder that exists
                if not path.is_created:
                    path.is_created = True
                    self.contains.append(path)

            # if path is folder
            elif path[0].is_created is False:
                # Once added, it changes its state so that the file is not saved again
                path[0].is_created = True

                # We are adding folder to path because we want to create folder inside it
                dst_folder_path.append(path[0].name)

                # Adding folder into desired one
                self.contains.append(path.pop(0))

                # If there are still folders to add continue
                if len(path) != 0:
                    self.add(path, dst_folder_path)

                return None

        # For each item in the folder
        for child_folder in self.contains:
            # Checking whether the pursuit of a folder has been completed
            if len(dst_folder_path) == 0:
                return None

            # If the item in the folder list is a folder
            if isinstance(child_folder, type(Folder(''))) and child_folder.name == dst_folder_path[0]:
                del dst_folder_path[0]
                child_folder.add(path, dst_folder_path)

    def sizes(self) -> None:
        for child_folder in self.contains:
            # If I am a folder
            if isinstance(self, type(Folder(''))):
                self.size += int(child_folder.size)

            # If I encounter a folder
            if isinstance(child_folder, type(Folder(''))):
                child_folder.sizes()
                # After the size is calculated add it to self.size
                self.size += int(child_folder.size)

    def print(self, depth=0) -> None:
        """View the contents of subfolders"""
        # We display the directory we started with
        if depth == 0:
            print(self.__str__())
            depth += 1

        # If the folder is empty
        if not self.contains:
            print((depth - 1) * '║' + '╚' + "[Empty]")
            return None
        else:
            # For each item in the folder
            for child_folder in self.contains:
                # Display name with proper spacing
                print((depth - 1) * '║' + '╠' + child_folder.__str__())
                # If the item from the folder list is a folder
                if isinstance(child_folder, type(Folder(''))):
                    # Display the contents of the subfolder
                    child_folder.print(depth + 1)

    def goto(self, path_to_folder: list, result=bool) -> bool:
        """Internal method used to check if the folder that we want to enter exists"""
        # If the list is not yet empty
        if path_to_folder:
            # Checking if the folder next exists
            for sub_folder in self.contains:
                # If folder exists
                if path_to_folder[0] == sub_folder.name:
                    # Delete the folder from list
                    del path_to_folder[0]
                    # Pass modified list further and return True or False
                    return sub_folder.goto(path_to_folder, result)

            # If folder doesn't exists print error and return False
            else:
                print("\tFolder ", path_to_folder[0], " not found")
                return False

        return True


if __name__ == "__main__":
    print("Type 'help' to see all available commands")
    fastFS = Filesystem()
    while True:
        fastFS.command(input('$ '))
