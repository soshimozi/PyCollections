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
class NodeColor:
    BLACK = 0
    RED = 1

class DuplicateKeyError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return repr(self.key)

class TreeNode(object):
    def __init__(self, key, value, left, right):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return repr (self.value)

class AATreeNode(TreeNode):
    """This class represents a single node in a binary tree."""
    def __init__(self, key, value, left, right, level):
	super(AATreeNode, self).__init__(key, value, left, right)
        self.level = level

    def __repr__(self):
        return TreeNode.__repr__(self)

class RBTreeNode(TreeNode):
    def __init__(self, key, value, left, right, parent, color):
	super(RBTreeNode, self).__init__(key, value, left, right)
	self.parent = parent
        self.color = color

    def __repr__(self):
        return TreeNode.__repr__(self)

    
class AATree:
    """This class represents a balanced binary tree.
    This particular implementation uses the AA tree variation."""
    def __init__(self):
        self.root = None
        
        self._bottom = AATreeNode(None, None, None, None, 0)
        
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

    def _delete_node(self, key, T):
        if T != self._bottom:

            #last = delete = None

            # Step 1: Search down tree
            #         set last and delete
            self._last = T
            if key < T.key:
                T.left = self._delete_node(key, T.left)
            else:
                self._deleted = T
                T.right = self._delete_node(key, T.right)

            # Step 2: If at the bottom of the tree and
            #         item is present, we remove it
            if T == self._last and self._deleted != self._bottom and key == self._deleted.key:

                    self._deleted.key = T.key
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

    def _insert_node(self, key, value, T):
      
        # Do the normal binary tree insertion procedure.  Set the result of the
        # recursive call to the correct child in the case a new node was created or the
        # root of the subtree changes

        if T == self. _bottom:
            # Create a new leaf node with value.
            return AATreeNode(key, value, self._bottom, self._bottom, 1)

        else:
            if key < T.key:
                T.left = self._insert_node(key, value, T.left)
            else:
                if key > T.key:
                    T.right = self._insert_node(key, value, T.right)
                else:
                    raise DuplicateKeyError(value)

        # skew then split, returning the result
        return self. _split(self._skew(T))
          
    def insert(self, key, value):
        self.root = self._insert_node(key, value, self.root)

    def remove(self, key):
        self.root = self._delete_node(key, self.root)

class RedBlackTree:

    def __init__(self):
        
        self.nil = RBTreeNode(None, None, None, None, None, NodeColor.BLACK)
        self.nil.left = self.nil.right = self.nil.parent = self.nil

        self._root = self.nil

    def _is_nil(self, node):
        return node == self.nil
		
    def _left_rotate(self, x):

        y = x.right
        x.right = y.left

        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

        assert(self.nil.color == NodeColor.BLACK)

    def _right_rotate(self, y):

        x = y.left
        y.left = x.right
        
        if x.right != self.nil:
            x.right.parent = y

        x.parent = y.parent
        if y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

        assert(self.nil.color == NodeColor.BLACK)

    def _make_node(self, key, value):
        return RBTreeNode(key, value, self.nil, self.nil, self.nil, NodeColor.RED)

    def _insert(self, z):
        
        z.left = z.right = z.Parent = self.nil

        y = self._root
        x = self._root.left
        
        while not self._is_nil(x):
            y = x
            
            if x.key == z.key:
                raise DuplicateKeyError(z.key)
            else:
                if x.key > z.key:
                    x = x.left
                else:
                    x = x.right

        z.parent = y
        if y == self._root or y.key > z.key:
            y.left = z
        else:
            y.right = z

    def _rebalance(self, x):
        
        # red black property may have been destroyed
        # so we have to restore it
        while x.parent.color == NodeColor.RED:
            
            if x.parent == x.parent.parent.left:
                # if x's parent is a left, uncle must be a right
                y = x.parent.parent.right

                if y.color == NodeColor.RED:
                    # case 1
                    print("case #1")
                    x.parent.color = NodeColor.BLACK
                    y.color = NodeColor.BLACK
                    x.parent.parent.color = NodeColor.RED
                    x = x.parent.parent
                else:
                    # y is black
                    
                    # and x is right, case #2
                    # move x up and roate it (rotates child into Parent spot)
                    if x == x.parent.right:
                        print("case #2")
                        x = x.parent
                        self._left_rotate(x)

                    # case #3
                    print("case #3")
                    x.parent.color = NodeColor.BLACK
                    x.parent.parent.color = NodeColor.RED
                    self._right_rotate(x.parent.parent)
            else:

                # x's parent is a RIGHT child (symmetrical to left case)
                
                #if x's parent is a right, uncle must be a left
                y = x.parent.parent.left
                if y.color == NodeColor.RED:
                    # case #4
                    print("case #4")

                    x.parent.color = NodeColor.BLACK
                    y.color = NodeColor.BLACK
                    x.parent.parent.color = NodeColor.RED
                    x = x.parent.parent

                else:
                    
                    # x is left, case #2
                    # move x up and rotate it (rotates child into Parent's position)
                    if x == x.parent.left:
                        print("case #5")

                        x = x.parent
                        self._right_rotate(x)

                    print("case #6")

                    x.parent.color = NodeColor.BLACK
                    x.parent.parent.color = NodeColor.RED
                    self._left_rotate(x.parent.parent)
                    
    def insert(self, key, value):
        newnode = self._make_node(key, value)

        self._insert(newnode)

        self._rebalance(newnode)

        # always set root color to black
        self._root.left.color = NodeColor.BLACK

        return newnode


    def _deleteFixUp(self, x):
        root = self._root.left

        while x.color == NodeColor.BLACK and root != x:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == NodeColor.RED:
                    w.color = NodeColor.BLACK
                    x.parent.color = NodeColor.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.right.color == NodeColor.BLACK and w.left.color == NodeColor.BLACK:
                    w.color = NodeColor.RED
                    x = x.parent

                else:
                    
                    if w.right.color == NodeColor.BLACK:
                        w.left.color = NodeColor.BLACK
                        w.color = NodeColor.RED
                        self._right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = NodeColor.BLACK
                    w.right.color = NodeColor.BLACK
                    self._left_rotate(x.parent)
                    x = root
            else:
                w = x.parent.left
                if w.color == NodeColor.RED:
                    w.color = NodeColor.BLACK
                    x.parent.color = NodeCollor.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                    

                if w.right.color == NodeColor.BLACK and w.left.color == NodeColor.BLACK:
                    w.color = NodeColor.RED
                    x = x.parent
                else:
                    if w.left.color == NodeColor.BLACK:
                        w.right.color = NodeColor.BLACK
                        w.color = NodeColor.RED
                        self._left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = NodeColor.BLACK
                    w.left.color = NodeColor.BLACK
                    self._right_rotate(x.parent)
                    x = root
            
                    
        x.color = NodeColor.BLACK
        assert(self.nil.color == NodeColor.BLACK)


    def treeSuccessor(self, x):
        nil = self.nil
        
        root = self._root
        
        y = x.right
        if y != nil:
            while y.left != nil:
                y = y.left

            return y
        else:
            y = x.parent
            while x == y.right:
                x = y
                y = y.parent
            if y == root:
                return nil

            return y

    def treePredecessor(self, x):
        
        nil = self.nil
        root = self._root
        
        y = x.left
        if y != nil:
            while y.right != nil:
                y = y.right

            return right
        else:
            y = x.parent
            while x == y.left:
                if y == root:
                    return nil

                x = y
                y = y.parent

            return y

    def delete(self, z):
        
        nil = self.nil
        root = self._root
        
        if z.left == nil or z.right == nil:
            y = z
        else:
            y = self.treeSuccessor(z)
            
        if y.left == nil:
            x = y.right
        else:
            x = y.left

        x.parent = y.parent
        if root == x.parent:
            root.left = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x

        if y != z:
            
            assert( y != self.nil )

            if y.color == NodeColor.BLACK:
                self._deleteFixUp(x)

            y.left = z.left
            y.right = z.right
            y.parent = z.parent
            y.color = z.color
            z.left.parent = z.right.parent = y

            if z == z.parent.left:
                z.parent.left = y
            else:
                z.parent.right = y

            z = None
        else:
            if y.color == NodeColor.BLACK:
                self._deleteFixUp(x)

            y = None

        assert(self.nil.color == NodeColor.BLACK)
