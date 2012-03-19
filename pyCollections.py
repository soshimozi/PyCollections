"""
AATree
======

       AATree (AA) is a Python package for the usage of AA
       binary balanced trees.

Using
-----
       Just write in Python

       >>> import AATree as AA
       >>> tree = AA.Tree()
       >>> tree.insert('H')
       >>> tree.insert('E')
       >>> tree.insert('L')
       >>> tree.insert('O')
       >>> tree.insert('X')
       >>> tree.remove('X')  
"""

class DuplicateKeyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class AATreeNode:
    """This class represents a single node in a binary tree."""
    def __init__(self, value, level, left, right):
        self.value = value
        self.level = level
        self.left = left
        self.right = right

class RBTreeNode:
	def __init__(self, value, parent, left, right):
		self.value = value
		self.parent = parent
		self.left = left
		self.right = right

class RBTree:
	"""This class represents a balanced binary tree.
	This particluar implementation uses the Red-Black tree variation."""
	def __init__(self):
		self._leaf = RBTreeNode(None, None, None, None)
		self._leaf.parent = self._leaf
		self._leaf.left = self._leaf.right = self._leaf

	def _grandparent(self, n):
		if n and n.parent:
			return n.parent.parent
		else:
			return None

	def _uncle(self, n):
		g = grandparent(n)
		if not g:
			return None

		if n.parent == g.left:
			return g.right
		else:
			return g.left

class AATree:
    """This class represents a balanced binary tree.
    This particular implementation uses the AA tree variation."""
    def __init__(self):
        self.root = None
        
        self._bottom = AATreeNode(None, 0, None, None)
        
        self._bottom.left = self._bottom
        self._bottom.right = self._bottom

        self._deleted = self._bottom
        self._last = self._bottom
        self.root = self._bottom
    
    def _skew(self, T):
        if T != self._bottom:

            if T.left.level == T.level:
            #swap the pointers of the horizontal left links.
                L = T.left
                T.left = L.right
                L.right = T
                return L
            else:
                return T
            
        return T

    def _split(self, T):
        if T != self._bottom:
          
            if T.level == T.right.right.level:
                # We have two horizontal links.  Take the middle node, elevate it, and return it
                R = T.right
                T.right = R.left
                R.left = T
                R.level = R.level + 1
                return R
        
        return T

    def _delete_node(self, value, T):
        if T != self._bottom:

            #last = delete = None

            # Step 1: Search down tree
            #         set last and delete
            self._last = T
            if value < T.value:
                T.left = self._delete_node(value, T.left)
            else:
                self._deleted = T
                T.right = self._delete_node(value, T.right)

            # Step 2: If at the bottom of the tree and
            #         item is present, we remove it
            if T == self._last and self._deleted != self._bottom and value == self._deleted.value:

                    self._deleted.value = T.value
                    self._deleted = self._bottom
                   
                    T = T.right
                    self._last = None

            # Step 3: Otherwise we are nto at the bottom;
            #         rebalance
            else:
                if T.left.level < T.level - 1 or T.right.level < T.level - 1:

                    T.level = T.level - 1
                    if T.right.level > T.level:
                        T.right.level = T.level

                    T = self._skew(T)
                    T.right = self._skew(T.right)
                    T.right.right = self._skew(T.right.right)
                    T = self._split(T)
                    T.right = self._split(T.right)
        return T

    def _insert_node(self, value, T):
      
        # Do the normal binary tree insertion procedure.  Set the result of the
        # recursive call to the correct child in the case a new node was created or the
        # root of the subtree changes

        if T == self. _bottom:
            # Create a new leaf node with value.
            return AATreeNode(value, 1, self._bottom, self._bottom)

        else:
            if value < T.value:
                T.left = self._insert_node(value, T.left)
            else:
                if value > T.value:
                    T.right = self._insert_node(value, T.right)
                else:
                    raise DuplicateKeyError(value)

        # skew then split, returning the result
        return self. _split(self._skew(T))
          
    def insert(self, value):
        self.root = self._insert_node(value, self.root)

    def remove(self, value):
        self.root = self._delete_node(value, self.root)
