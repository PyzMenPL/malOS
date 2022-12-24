import os
import sys


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
            print("\tls - prints all folders and files in current folder")
            print("\tmkdir <path> - creates directory inside current folder")
            print("\tmkfile <path> - creates empty file inside current folder")
            print("\tmkfile <path> <size> - creates file with specified size inside current folder")
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

                    # Return
                    if self.current_directory:
                        return self.current_directory[-1]
                    else:
                        return '/'

                # Add folders
                self.root.add(folders, path_to_pass)

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


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
        self.is_created = False

    def __str__(self) -> str:
        return "{} ({}, size={})".format(self.name, "file", self.size)

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
            return "{} (dir)".format(self.name)
        else:
            return "{} (dir, size={})".format(self.name, self.size)

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
                # Checking if the file already exists
                for item in self.contains:
                    if path.name == item.name:
                        print("\tThis file already exists!")
                        return None

                if not path.is_created:
                    path.is_created = True
                    self.contains.append(path)
                    print("\tFile '" + path.name + "' created successfully!")

            # if path is folder
            elif path[0].is_created is False:
                # Checking if the folder already exists
                for item in self.contains:
                    if path[-1].name == item.name:
                        print("\tFolder '" + path[0].name + "' already exists!")
                        return None

                # Once added, it changes its state so that the file is not saved again
                path[0].is_created = True

                # We are adding folder to path because we want to create folder inside it
                dst_folder_path.append(path[0].name)

                # If skip is true we skip path[0]
                skip = False

                # Searching through to find if the folder is already created
                for item in self.contains:
                    if path[0].name == item.name:
                        skip = True

                # If the folder is not created add it to self
                if not skip:
                    print("\tFolder '" + path[0].name + "' created successfully!")
                    self.contains.append(path.pop(0))

                # If the folder is already created delete it from list
                else:
                    del path[0]

                # If there are still folders to add continue
                if len(path) != 0:
                    self.add(path, dst_folder_path)

                # If there are no folders to add return
                else:
                    return None

        # For each item in the folder
        for child_folder in self.contains:
            # Checking whether the search for a folder has been completed
            if len(dst_folder_path) == 0:
                return None

            # If the item in the folder list is a folder
            if isinstance(child_folder, type(Folder(''))) and child_folder.name == dst_folder_path[0]:
                del dst_folder_path[0]
                child_folder.add(path, dst_folder_path)
                return None

        # If we get here this means that nothing happened because the folder was not found.
        # There's reference to self.name so the message is shown only once.
        if isinstance(path, type(File("", 0))) and self.name == '/':
            print("\tCould not find folder '" + dst_folder_path[0] + "'")

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

    def print(self, path: list, depth=None, what_to_add=None) -> None:
        """View the contents of subfolders"""
        # If we are in our desired folder
        if not path:
            # Doesn't activate on first folder
            if what_to_add is not None:
                # Receives information from previous folder
                depth.append(what_to_add)

            # Doesn't activate on first folder
            if depth is None:
                depth = []
                print(self.__str__())

            # If my folder contains 2 items print ║ else none
            if len(self.contains) >= 2:
                what_to_add = True
            else:
                what_to_add = False

            # If the folder is empty
            if not self.contains:
                # Display proper spacing
                for dependency in depth:
                    if dependency:
                        print('║   ', end='')
                    else:
                        print('    ', end='')
                print('╚══ ' + "[Empty]")
                return None

            # If the folder is not empty
            else:
                # For each item in the folder
                for index in range(0, len(self.contains)):
                    # Display proper spacing
                    for dependency in depth:
                        if dependency:
                            print('║   ', end='')
                        else:
                            print('    ', end='')

                    # If we are printing last element
                    if index == len(self.contains) - 1:
                        # Don't print ║
                        what_to_add = False

                        # Print last element
                        print('╚══ ' + self.contains[index].__str__())

                    # If we are printing any other element
                    else:
                        print('╠══ ' + self.contains[index].__str__())

                    # If the item from the folder list is a folder
                    if isinstance(self.contains[index], type(Folder(''))):
                        self.contains[index].print(path, depth=depth[:], what_to_add=what_to_add)
        # If we are not in our desired folder
        else:
            # Look for it
            for item in self.contains:
                if len(path) != 0:
                    if item.name == path[0]:
                        del path[0]
                        item.print(path)

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
    current_folder = "/"

    while True:
        current_folder = fastFS.command(input(current_folder + ' $ '))
