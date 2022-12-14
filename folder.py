from file import File


class Folder:
    # Folder is a child of the File class (takes its name and size from it)
    def __init__(self, name: str) -> None:
        self.name = name
        self.size = 0
        self.is_created = False
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
                    self.size += path.size

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

                # Update folder size when adding a file
                if isinstance(path, type(File("", 0))):
                    if path.is_created:
                        self.size += path.size

                return None

        # If we get here this means that nothing happened because the folder was not found.
        # There's reference to self.name so the message is shown only once.
        if isinstance(path, type(File("", 0))) and self.name == '/':
            print("\tCould not find folder '" + dst_folder_path[0] + "'")

    def print(self, path: list, depth=None, what_to_add=None) -> None:
        """View the contents of subfolders"""
        # Make sure we are not going to print file
        if path:
            for item in self.contains:
                if path[0] == item.name:
                    if isinstance(item, type(File("", 0))):
                        print("\t'" + item.name + "' is a file!")
                        return None
                    else:
                        break
            else:
                print("\tFolder '" + path[0] + "' doesn't exists!")
                return None

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

            # If my folder contains 2 items print ??? else none
            if len(self.contains) >= 2:
                what_to_add = True
            else:
                what_to_add = False

            # If the folder is empty
            if not self.contains:
                # Display proper spacing
                for dependency in depth:
                    if dependency:
                        print('???   ', end='')
                    else:
                        print('    ', end='')
                print('????????? ' + "[Empty]")
                return None

            # If the folder is not empty
            else:
                # For each item in the folder
                for index in range(0, len(self.contains)):
                    # Display proper spacing
                    for dependency in depth:
                        if dependency:
                            print('???   ', end='')
                        else:
                            print('    ', end='')

                    # If we are printing last element
                    if index == len(self.contains) - 1:
                        # Don't print ???
                        what_to_add = False

                        # Print last element
                        print('????????? ' + self.contains[index].__str__())

                    # If we are printing any other element
                    else:
                        print('????????? ' + self.contains[index].__str__())

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
                    # Making sure we are cd-ing into Folder
                    if isinstance(sub_folder, type(File(""))):
                        print("\t'" + sub_folder.name + "' is a file!")
                        return False
                    else:
                        # Delete the folder from list
                        del path_to_folder[0]
                        # Pass modified list further and return True or False
                        return sub_folder.goto(path_to_folder, result)

            # If folder doesn't exists print error and return False
            else:
                print("\tFolder '" + path_to_folder[0] + "' not found")
                return False

        return True

    def delete(self, file, path) -> int:
        """Method for deleting files"""
        # If we are not in desired folder
        if len(path):
            for item in self.contains:
                # If we found next folder
                if item.name == path[0]:
                    # We make sure it is a folder
                    if isinstance(item, type(Folder(''))):
                        # Removing folder that we are currently in
                        del path[0]

                        # Getting the size of deleted file
                        size_to_del = item.delete(file, path[:])

                        # Changing self.size
                        self.size -= size_to_del
                        return size_to_del

                    # If it isn't folder
                    else:
                        print("\t" + path[0] + " is not a folder!")
                        return 0

            # If we haven't found folder from path
            else:
                print("\t" + path[0] + " doesn't exist!")
                return 0

        # If we are in desired folder
        else:
            for item in self.contains:
                if file == item.name:
                    # Changing self size
                    self.size -= item.size

                    # Removing file from desired folder
                    del self.contains[self.contains.index(item)]
                    print("\t" + item.name + " deleted successfully!")

                    return item.size
