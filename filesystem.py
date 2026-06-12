class Node:
    """Represents a file or a folder in the file system."""
    def __init__(self, name, is_directory=True):
        self.name = name
        self.is_directory = is_directory
        self.children = {}  # Maps name -> Node object
        self.parent = None  

    def add_child(self, child_node):
        child_node.parent = self
        self.children[child_node.name] = child_node


class FileSystem:
    def __init__(self):
        self.root = Node("/", is_directory=True)
        self.current_directory = self.root
        self.history_stack = []  # Navigation history stack

    def _navigate_to_path(self, path_str):
        """Helper that processes paths like 'Documents/Photos' using Traversal.
        Returns the target folder node if found, or None if invalid.
        """
        if not path_str:
            return self.current_directory

        steps = path_str.strip("/").split("/")
        start_node = self.root if path_str.startswith("/") else self.current_directory
        
        curr = start_node
        for step in steps:
            if not step or step == ".":
                continue
            if step == "..":
                if curr.parent:
                    curr = curr.parent
                continue
            
            if step in curr.children:
                if curr.children[step].is_directory:
                    curr = curr.children[step]
                else:
                    print(f"Error: '{step}' is a file, not a folder.")
                    return None
            else:
                print(f"Error: Folder '{step}' does not exist.")
                return None
        return curr

    def create_folder(self, path_name):
        """Creates a folder, supporting nested paths (e.g., folder Documents/Code)."""
        if "/" in path_name:
            parts = path_name.rsplit("/", 1)
            target_dir = self._navigate_to_path(parts[0])
            new_name = parts[1]
        else:
            target_dir = self.current_directory
            new_name = path_name

        if target_dir is None or not new_name:
            return

        if new_name in target_dir.children:
            print(f"Error: '{new_name}' already exists there.")
            return

        new_folder = Node(new_name, is_directory=True)
        target_dir.add_child(new_folder)
        print(f"Folder '{new_name}' created successfully.")

    def create_file(self, path_name):
        """Creates a file inside a specific folder path (e.g., file Documents/notes.txt)."""
        if "/" in path_name:
            parts = path_name.rsplit("/", 1)
            target_dir = self._navigate_to_path(parts[0])
            new_name = parts[1]
        else:
            target_dir = self.current_directory
            new_name = path_name

        if target_dir is None or not new_name:
            return

        if new_name in target_dir.children:
            print(f"Error: '{new_name}' already exists there.")
            return

        new_file = Node(new_name, is_directory=False)
        target_dir.add_child(new_file)
        print(f"File '{new_name}' created successfully.")

    def change_directory(self, name):
        """Navigates into a subfolder."""
        if name in self.current_directory.children:
            target = self.current_directory.children[name]
            if target.is_directory:
                self.history_stack.append(self.current_directory)
                self.current_directory = target
            else:
                print(f"Error: '{name}' is a file, you can only enter folders.")
        else:
            print(f"Error: Folder '{name}' not found.")

    def go_back(self):
        """Navigates backward using the history stack."""
        if self.current_directory == self.root:
            print("You are already at the very top (Root) folder.")
        elif self.history_stack:
            self.current_directory = self.history_stack.pop()
        else:
            self.current_directory = self.current_directory.parent

    def pwd(self):
        """Returns the current folder path."""
        path = []
        curr = self.current_directory
        while curr:
            path.append(curr.name)
            curr = curr.parent
        path.reverse()
        return "/" + "/".join(path[1:]) if len(path) > 1 else "/"

    def list_dir(self):
        """Lists contents of the current folder."""
        contents = self.current_directory.children.keys()
        if not contents:
            print("(This folder is empty)")
            return
        print(f"\nContents of {self.pwd()}:")
        for item in contents:
            node = self.current_directory.children[item]
            marker = "[FOLDER]" if node.is_directory else "[FILE]"
            print(f"  {marker} {item}")

    def show_tree(self, node=None, indent=0):
        """DFS Traversal to print the visual map."""
        if node is None:
            node = self.root
            print("\n--- Visual Folder Map ---")
            print(node.name)
            indent = 1

        for name, child in sorted(node.children.items()):
            prefix = "    " * indent + "└── "
            marker = "/" if child.is_directory else ""
            print(f"{prefix}{name}{marker}")
            if child.is_directory:
                self.show_tree(child, indent + 1)

    def search(self, target_name, node=None, current_path=""):
        """DFS Traversal to find matches across the system."""
        if node is None:
            node = self.root
            current_path = ""
            print(f"\n--- Search Results for '{target_name}' ---")

        this_path = f"{current_path}/{node.name}" if node != self.root else ""
        if node.name == target_name:
            display_path = this_path if this_path else "/"
            print(f"Found match: {display_path} ({'Folder' if node.is_directory else 'File'})")

        for child in node.children.values():
            self.search(target_name, child, this_path)


# --- INTERACTIVE TERMINAL INTERFACE ---
if __name__ == "__main__":
    fs = FileSystem()
    print("=" * 60)
    print("  File System Simulator Initialized (Plain English Mode)")
    print("=" * 60)
    print("  Available Commands:")
    print("    folder <name> -> Create a new folder (e.g., folder Documents)")
    print("    file <name>   -> Create a new file (e.g., file Documents/notes.txt)")
    print("    list          -> Show everything inside the current folder")
    print("    go <name>     -> Enter a specific folder (e.g., go Documents)")
    print("    back          -> Leave the current folder and go back")
    print("    map           -> View the entire visual folder layout")
    print("    find <name>   -> Search the whole system for a file/folder")
    print("    exit          -> Close the simulator")
    print("=" * 60)

    while True:
        try:
            user_input = input(f"\nCurrent Folder: {fs.pwd()} > ").strip().split()
            if not user_input:
                continue

            command = user_input[0].lower()
            argument = user_input[1] if len(user_input) > 1 else None

            if command == "exit":
                print("Closing simulator. Goodbye!")
                break
            elif command == "folder":
                if argument: fs.create_folder(argument)
                else: print("Error: Please provide a folder name. Example: folder Documents")
            elif command == "file":
                if argument: fs.create_file(argument)
                else: print("Error: Please provide a file name. Example: file note.txt")
            elif command == "list":
                fs.list_dir()
            elif command == "go":
                if argument: fs.change_directory(argument)
                else: print("Error: Please specify which folder to go to. Example: go Documents")
            elif command == "back":
                fs.go_back()
            elif command == "map":
                fs.show_tree()
            elif command == "find":
                if argument: fs.search(argument)
                else: print("Error: Please specify what you want to find. Example: find resume.txt")
            else:
                print(f"Unknown command: '{command}'.")
        
        except KeyboardInterrupt:
            print("\nClosing simulator. Goodbye!")
            break
