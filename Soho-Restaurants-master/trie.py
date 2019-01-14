class Trie:
    def __init__(self):
        # self.children is a dict of child nodes of the current node int he Trie
        self.children = {}
        self.value = None

    def __normalise(self, value):
        return str(value).lower().strip()

    def add(self, val, string=None):
        # 'string' retains the initial string that was added so it can be set as the value of the terminal node
        # 'val' is the remaining string to be added after each call to .add().
        # 'val' also holds the initial string at the first call, but is overwritten at each subsequent call,
        #   hence the need to store the full string elsewhere.
        val = self.__normalise(val)
        if string is None:
            string = val

        # Get the starting character of the string to insert:
        #  if it exists in tree, current_node to it
        #  else create new Trie at corresponding new node in tree
        string_start = val[0]
        if string_start in self.children:
            node = self.children[string_start]
        else:
            node = Trie()
            self.children[string_start] = node

        # Is this the last char in the string?
        #  Yes: set node.value to the string being added to indicate termination of a valid branch
        #  No: call .add() using the remainder of the string
        if len(val) == 1:
            node.value = string
        else:
            node.add(val[1:], string)  # We also need to pass the full string to retain it thru calls

    def get(self, find_this):
        # finds exact match of find_this in Trie
        current_node = self  # this is the head node
        find_this = self.__normalise(find_this)

        # iterate over the characters in the value to find
        for char in find_this:
            # if the current character is a child node, set current_node to it
            # else return None to signal string not found
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return None

        # At this point we have traversed the trie all the way from the first to last character in the string,
        #  so we return current_node.value to verify.
        return current_node.value

    def find(self, prefix, current_node=None, return_vals=None):
        # finds all strings in Trie beginning with prefix
        prefix = self.__normalise(prefix)
        if current_node is None:
            current_node = self
        if return_vals is None:
            return_vals = []

        # iterate of the characters in the prefix to search
        for char in prefix:
            # if current character is a child node, set current_node to it
            # else return None to signal no match on given prefix
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return None

        # populate return_vals if the current node is a valid terminal node
        if current_node.value:
            return_vals.append(current_node.value)
        # iterate recursively over the child nodes (current_node.children)
        #   calling .find() with the each child node & the return_vals array
        for char in current_node.children:
            self.find("", current_node.children[char], return_vals)

        return return_vals


# Tests ###############################
# t = Trie()
# t.add("a")
# t.add("asd")
# t.add("asx")
# t.add("q")
# t.add("qw")
# t.add("qas")
# t.add("qwerty")
# t.add("azerty")
#
# print("\n.get() tests:")
# print(t.get("qw"))    # returns "qw"
# print(t.get("qa"))    # returns None
# print(t.get(" a "))   # returns "a"
# print(t.get(" as "))  # returns None
# print(t.get(" "))     # returns None
#
# print(t.get(""))            # returns None
# print(t.get(1))             # returns None
# print(t.get(t))             # returns None
# print(t.get("qwertyuiop"))  # returns None
#
# print("\n.find() tests:")
# print(t.find("qw"))      # returns ["qw", "qwerty"]
# print(t.find("a"))       # returns ['a', 'asx', 'asd', 'azerty']
# print(t.find("z"))       # returns None
# print(t.find("azer"))    # returns ['azerty']
# print(t.find("azerty"))  # returns ['azerty']
# print(t.find(" a "))     # returns ['a', 'asx', 'asd', 'azerty']
# print(t.find(" "))       # returns ['a', 'asx', 'asd', 'azerty', 'q', 'qas', 'qw', 'qwerty']
# print(t.find(" asd "))   # returns ['asd']
# print(t.find(" z "))     # returns None
#
# print(t.find(""))            # returns ['a', 'asx', 'asd', 'azerty', 'q', 'qas', 'qw', 'qwerty']
# print(t.find(1))             # returns None
# print(t.find(t))             # returns None
# print(t.find("qwertyuiop"))  # returns None
