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
                if self.current_directory:
                    del self.current_directory[-1]
                else:
                    print("\tYou can't go back further!")
            else:
                self.cd(command[1])

        elif command[0] == 'ls':
            self.root.print()

        # Add directory or file if it doesn't exist
        elif command[0] == 'mkdir':
            file = Folder(command[1])
            self.root.add(file, self.current_directory[:])
            print("\tFolder '" + command[1] + "' created successfully!")

        elif command[0] == 'mkfile':
            file = None
            # User specified name only
            if len(command) == 2:
                file = File(command[1], 0)

            # User specified both parameters
            elif len(command) == 3:
                file = File(command[1], command[2])

            self.root.add(file, self.current_directory[:])
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
            print("\tInvalid syntax: ", command)
            print("\tType 'help' to see all available commands")
            return

    def cd(self, dst_name=None) -> None:
        if dst_name == '/':
            self.current_directory = []
        else:
            self.current_directory.append(dst_name)


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.is_created = False

    def __str__(self):
        return "- {} ({}, size={})".format(self.name, "file", self.size)

    def __repr__(self):
        # Instead of printing out <class 'str'>, it prints out as follows
        return "Plik '{}'".format(self.name)


class Folder(File):
    # Folder is a child of the File class (takes its name and size from it)
    def __init__(self, name: str) -> None:
        # The same as self.name = name and self.size = size
        super().__init__(name=name, size=0)
        self.contains = []

    def __iter__(self):
        # If iteration starts, we start from zero
        self.index = 0
        # We end up with the last item on the list
        self.limit = len(self.contains)
        return self

    def __next__(self):
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
            return "- {} (dir)".format(self.name)
        else:
            return "- {} (dir, size={})".format(self.name, self.size)

    def __repr__(self):
        # Instead of printing out <class 'str'>, it prints out as follows
        return "'Folder '{}'".format(self.name)

    def add(self, file, dst_folder_path) -> None:
        # If it reaches the destination folder, it saves the file.
        # If the condition did not check if the file was created, it would still be saved in the wrong places
        if dst_folder_path == [] and file.is_created is False:
            self.contains.append(file)

            # Once added, it changes its state so that the file is not saved again
            file.is_created = True
            return None

        # For each item in the folder
        for child_folder in self.contains:
            # Checking whether the pursuit of a folder has been completed
            if len(dst_folder_path) == 0:
                return None

            # If the item in the folder list is a folder
            if isinstance(child_folder, type(Folder(''))) and child_folder.name == dst_folder_path[0]:
                del dst_folder_path[0]
                child_folder.add(file, dst_folder_path)

    def sizes(self):
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
            print(depth * '\t', self)
            depth += 1

        # If the folder is empty
        if not self.contains:
            print(depth * '\t', "[Empty]")
            return None

        # For each item in the folder
        for child_folder in self.contains:
            # Display name with proper spacing
            print(depth * '\t', child_folder)

            # If the item from the folder list is a folder
            if isinstance(child_folder, type(Folder(''))):
                # Display the contents of the subfolder
                child_folder.print(depth + 1)


if __name__ == "__main__":
    print("Type 'help' to see all available commands")
    fastFS = Filesystem()
    while True:
        fastFS.command(input('$ '))
