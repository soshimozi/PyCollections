"""
pyCollections
======

       pyCollections is a Python package which contains various
       collections.

Using
-----
       Just write in Python

       >>> import pyCollections  as pyc
       >>> tree = pyc.AATree()
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

class TreeNode(object):
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return repr (self.value)

class AATreeNode(TreeNode):
    """This class represents a single node in a binary tree."""
    def __init__(self, value, level, left, right):
	super(AATreeNode, self).__init__(value, left, right)
        self.level = level

    def __repr__(self):
        return TreeNode.__repr__(self)

class RBTreeNode(TreeNode):
    def __init__(self, value, isred, parent, left, right):
	super(RBTreeNode, self).__init__(value, left, right)
	self.parent = parent
        self.isred = isred

    def __repr__(self):
        return TreeNode.__repr__(self)


class RBTree:

    # every node is red or black
    # root and leaf nodes are black
    # every red node has a black parent
    # all simple paths from any node x to a descendant
    # leaf have the same number of black nodes = black-height(x)

    
    def _binary_insert(self, z):
        # even though at instantiation, these are set to nill - make sure they still are
        z.left = z.right = self._nil
        
        y = self._root
        x = self._root.left

        while x != self._nil:
            y = x
            if x.value > z.value:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y == self._root or y.key > z.key:
            y.left = z
        else:
            y.right = z


    def _is_nil(self, n):
        return n == self._nil

    def _left_rotate(self, y):

        y = x.right
        x.right = y.left

        if not self._is_nil(y.left):
            y.left.parent = x

        y.parent = x.parent
        
        if x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y


    def _right_rotate(self, y):
        
        x = y.left
        y.left = x.right
        
        if not self._is_nil(x.right):
            x.right.parent = y
        
        x.parent = y.parent
        
        if y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def _is_red(self, x):
        return x.isred

    def _rebalance(self, x):
        
 

    def insert(self, value):
        
        x = self._make_node(value, false)
        self._binary_insert(x)
        
        newNode = x

        x.isred = True

        while x.parent.isred:
            
            if x.parent = x.parent.parent.left:
                
                y = x.parent.parent.right
                if y.isred:
                    x.parent.isred = False
                    y.isred = False
                    x.parent.parent.isred = True
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self._left_rotate(x)

                    x.parent.isred = False
                    x.parent.parent.isred = True
                    self._right_rotate(x.parent.parent)
            else:
                
                y = x.parent.parent.left
                if y.isred:
                    x.parent.isred = False
                    y.isred = False
                    x.parent.parent.isred = True
                    x = x.parent.parent
                else:
                    
                    if x == x.parent.left:
                        x = x.parent
                        self._right_rotate(x)

                    x.parent.isred = False
                    x.parent.parent.isred = True
                    self._left_rotate(x.parent.parent)
                    

                    
        self.root.left.isred = False
        return newNode

        

    """This class represents a balanced binary tree.
       This particluar implementation uses the Red-Black tree variation."""
    def __init__(self):
        self._nil = RBTreeNode(None, False, None, None)
        self._root = self._nil

    def _make_node(self, value, isred):
        return RBTreeNode(value, isred, self._nil, self._nil, self._nil)

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

    def _insert_case1(self, n):
        if not n.parent:
            n.color = COLOR_BLACK
        else:
            self._insert_case2(n)

    def _insert_case2(self, n):
        if n.parent.color == COLOR_BLACK:
            return # tree is still valid
        else:
            self._insert_case3(n)

    def _insert_case3(self, n):
        u = self._uncle(n)

        if u and u.color == COLOR_RED:
            n.parent.color = COLOR_BLACK
            u.color = COLOR_BLACK
            g = self._grandparent(n)
            g.color = COLOR_RED
            self._insert_case1(g)
        else:
            self._insert_case4(n)

    def _insert_case4(self, n):
        g = self._grandparent(n)
        
        if n == n.parent.right and n.parent == g.left:
            self._rotate_left(n.parent)
            n = n.left
        else:
            if n == n.parent.left and n.parent = g.right:
                self._rotate_right(n.parent)
                n = n.right
            

        self._insert_case5(n)

    def _insert_case5(self, n):
        g = grandparent(n)

        n.parent.color = COLOR_BLACK
        g.color = COLOR_RED
        
        if n == n.parent.left:
            self._rotate_right(g)
        else:
            self._rotate_left(g)
        
    

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
