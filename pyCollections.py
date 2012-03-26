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

import math

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
        self._key = key
        self._value = value
        self._left = left
        self._right = right

    def __repr__(self):
        return repr (self._value)

    def getKey(self):
        return self._key

class AATreeNode(TreeNode):
    """This class represents a single node in a binary tree."""
    def __init__(self, key, value, _left, _right, _level):
	super(AATreeNode, self).__init__(key, value, _left, _right)
        self._level = level

    def __repr__(self):
        return TreeNode.__repr__(self)

class RBTreeNode(TreeNode):
    def __init__(self, key, value, _left, _right, parent, color):
	super(RBTreeNode, self).__init__(key, value, _left, _right)
	self._parent = parent
        self._color = color

    def __repr__(self):
        return TreeNode.__repr__(self)

    
class AATree:
    """This class represents a balanced binary tree.
    This particular implementation uses the AA tree variation."""
    def __init__(self):
        self.root = None
        
        self._bottom = AATreeNode(None, None, None, None, 0)
        
        self._bottom._left = self._bottom
        self._bottom._right = self._bottom

        self._deleted = self._bottom
        self._last = self._bottom
        self.root = self._bottom

    def _skew(self, T):
        if T != self._bottom:

            if T._left._level == T._level:
            #swap the pointers of the horizontal _left links.
                L = T._left
                T._left = L._right
                L._right = T
                return L
            else:
                return T
            
        return T

    def _split(self, T):
        if T != self._bottom:
          
            if T._level == T._right._right._level:
                # We have two horizontal links.  Take the middle node, elevate it, and return it
                R = T._right
                T._right = R._left
                R._left = T
                R._level = R._level + 1
                return R
        
        return T

    def _delete_node(self, key, T):
        if T != self._bottom:

            #last = delete = None

            # Step 1: Search down tree
            #         set last and delete
            self._last = T
            if key < T._key:
                T._left = self._delete_node(key, T._left)
            else:
                self._deleted = T
                T._right = self._delete_node(key, T._right)

            # Step 2: If at the bottom of the tree and
            #         item is present, we remove it
            if T == self._last and self._deleted != self._bottom and key == self._deleted._key:

                    self._deleted._key = T._key
                    self._deleted = self._bottom
                   
                    T = T._right
                    self._last = None

            # Step 3: Otherwise we are nto at the bottom;
            #         rebalance
            else:
                if T._left._level < T._level - 1 or T._right._level < T._level - 1:

                    T._level = T._level - 1
                    if T._right._level > T._level:
                        T._right._level = T._level

                    T = self._skew(T)
                    T._right = self._skew(T._right)
                    T._right._right = self._skew(T._right._right)
                    T = self._split(T)
                    T._right = self._split(T._right)
        return T

    def _insert_node(self, key, value, T):
      
        # Do the normal binary tree insertion procedure.  Set the result of the
        # recursive call to the correct child in the case a new node was created or the
        # root of the subtree changes

        if T == self. _bottom:
            # Create a new leaf node with value.
            return AATreeNode(key, value, self._bottom, self._bottom, 1)

        else:
            if key < T._key:
                T._left = self._insert_node(key, value, T._left)
            else:
                if key > T._key:
                    T._right = self._insert_node(key, value, T._right)
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
        
        self._nil = RBTreeNode(None, None, None, None, None, NodeColor.BLACK)
        self._nil._left = self._nil._right = self._nil._parent = self._nil

        self._root = self._nil

    def _is_nil(self, node):
        return not node or node == self._nil
		
    def _left_rotate(self, x):

        y = x._right
        x._right = y._left

        if y._left != self._nil:
            y._left._parent = x

        y._parent = x._parent
        if x == x._parent._left:
            x._parent._left = y
        else:
            x._parent._right = y

        y._left = x
        x._parent = y

        assert(self._nil._color == NodeColor.BLACK)

    def __right_rotate(self, y):

        x = y._left
        y._left = x._right
        
        if x._right != self._nil:
            x._right._parent = y

        x._parent = y._parent
        if y == y._parent._left:
            y._parent._left = x
        else:
            y._parent._right = x

        x._right = y
        y._parent = x

        assert(self._nil._color == NodeColor.BLACK)

    def _make_node(self, key, value):
        return RBTreeNode(key, value, self._nil, self._nil, self._nil, NodeColor.RED)

    def _insert(self, z):
        
        z._left = z._right = z._Parent = self._nil

        y = self._root
        x = self._root._left
        
        while not self._is_nil(x):
            y = x
            
            if x._key == z._key:
                raise DuplicateKeyError(z._key)
            else:
                if x._key > z._key:
                    x = x._left
                else:
                    x = x._right

        z._parent = y
        if y == self._root or y._key > z._key:
            y._left = z
        else:
            y._right = z

    def _rebalance(self, x):
        
        # red black property may have been destroyed
        # so we have to restore it
        while x._parent._color == NodeColor.RED:
            
            if x._parent == x._parent._parent._left:
                # if x's parent is a left, uncle must be a _right
                y = x._parent._parent._right

                if y._color == NodeColor.RED:
                    # case 1
                    x._parent._color = NodeColor.BLACK
                    y._color = NodeColor.BLACK
                    x._parent._parent._color = NodeColor.RED
                    x = x._parent._parent
                else:
                    # y is black
                    
                    # and x is _right, case #2
                    # move x up and roate it (rotates child into Parent spot)
                    if x == x._parent._right:
                        x = x._parent
                        self._left_rotate(x)

                    # case #3
                    x._parent._color = NodeColor.BLACK
                    x._parent._parent._color = NodeColor.RED
                    self._right_rotate(x._parent._parent)
            else:

                # x's parent is a RIGHT child (symmetrical to left case)
                
                #if x's parent is a right, uncle must be a left
                y = x._parent._parent._left
                if y._color == NodeColor.RED:
                    # case #4
                    x._parent._color = NodeColor.BLACK
                    y._color = NodeColor.BLACK
                    x._parent._parent._color = NodeColor.RED
                    x = x._parent._parent

                else:
                    
                    # x is left, case #5
                    # move x up and rotate it (rotates child into Parent's position)
                    if x == x._parent._left:
                        x = x._parent
                        self._right_rotate(x)

                    # case #6
                    x._parent._color = NodeColor.BLACK
                    x._parent._parent._color = NodeColor.RED
                    self._left_rotate(x._parent._parent)
                    
    def search(self, key):
        x = self._root._left
        
        while not self._is_nil(x):
            y = x
            
            if x._key == key:
                return x
            else:
                if x._key > key:
                    x = x._left
                else:
                    x = x._right
        return None

    def insert(self, key, value):
        newnode = self._make_node(key, value)

        self._insert(newnode)

        self._rebalance(newnode)

        # always set root color to black
        self._root._left._color = NodeColor.BLACK

        return newnode


    def _delete_fix_up(self, x):
        root = self._root._left

        while x._color == NodeColor.BLACK and root != x:
            if x == x._parent._left:
                w = x._parent._right
                if w._color == NodeColor.RED:
                    w._color = NodeColor.BLACK
                    x._parent._color = NodeColor.RED
                    self._left_rotate(x._parent)
                    w = x._parent._right

                if w._right._color == NodeColor.BLACK and w._left._color == NodeColor.BLACK:
                    w._color = NodeColor.RED
                    x = x._parent

                else:
                    
                    if w._right._color == NodeColor.BLACK:
                        w._left._color = NodeColor.BLACK
                        w._color = NodeColor.RED
                        self._right_rotate(w)
                        w = x._parent._right

                    w._color = x._parent._color
                    x._parent._color = NodeColor.BLACK
                    w._right._color = NodeColor.BLACK
                    self._left_rotate(x._parent)
                    x = root
            else:
                w = x._parent._left
                if w._color == NodeColor.RED:
                    w._color = NodeColor.BLACK
                    x._parent._color = NodeCollor.RED
                    self._right_rotate(x._parent)
                    w = x._parent._left
                    

                if w._right._color == NodeColor.BLACK and w._left._color == NodeColor.BLACK:
                    w._color = NodeColor.RED
                    x = x._parent
                else:
                    if w._left._color == NodeColor.BLACK:
                        w._right._color = NodeColor.BLACK
                        w._color = NodeColor.RED
                        self._left_rotate(w)
                        w = x._parent._left

                    w._color = x._parent.color
                    x._parent._color = NodeColor.BLACK
                    w._left._color = NodeColor.BLACK
                    self._right_rotate(x._parent)
                    x = root
            
                    
        x._color = NodeColor.BLACK
        assert(self._nil._color == NodeColor.BLACK)


    def successor(self, x):
        nil = self._nil
        
        root = self._root
        
        y = x._right
        if y != nil:
            while y._left != nil:
                y = y._left

            return y
        else:
            y = x._parent
            while x == y._right:
                x = y
                y = y._parent
            if y == root:
                return nil

            return y

    def predecessor(self, x):
        
        nil = self._nil
        root = self._root
        
        y = x._left
        if y != nil:
            while y._right != nil:
                y = y._right

            return _right
        else:
            y = x._parent
            while x == y._left:
                if y == root:
                    return nil

                x = y
                y = y._parent

            return y

    def delete(self, z):
        
        nil = self._nil
        root = self._root
        
        if z._left == nil or z._right == nil:
            y = z
        else:
            y = self.successor(z)
            
        if y._left == nil:
            x = y._right
        else:
            x = y._left

        x._parent = y._parent
        if root == x._parent:
            root._left = x
        else:
            if y == y._parent._left:
                y._parent._left = x
            else:
                y._parent._right = x

        if y != z:
            
            assert( y != nil )

            if y._color == NodeColor.BLACK:
                self._delete_fix_up(x)

            y._left = z._left
            y._right = z._right
            y._parent = z._parent
            y._color = z._color
            z._left._parent = z._right._parent = y

            if z == z._parent._left:
                z._parent._left = y
            else:
                z._parent._right = y

            z = None
        else:
            if y._color == NodeColor.BLACK:
                self._delete_fix_up(x)

            y = None

        assert(self._nil._color == NodeColor.BLACK)

    def iterator(self, node):
        if node != self._nil:
            for x in self.iterator(node._left):
                yield x
            yield node
            for x in self.iterator(node._right):
                yield x


class BinaryHeap:
    def __init__(self, scorefn):
        self._scorefn = scorefn
        self._content = []

    def _sink_down(self, n):
        length = len(self._content)
        element = self._content[n]
        elemScore = self._scorefn(element)

        while True:
            child2N = (n + 1) * 2
            child1N = child2N - 1

            swap = None

            if child1N < length:
                child1 = self._content[child1N]
                child1Score = self._scorefn(child1)

                if child1Score < elemScore:
                    swap = child1N

            if child2N < length:
                child2 = self._content[child2N]
                child2Score = self._scorefn(child2)

                compare = elemScore
                if swap != None:
                    compare = child1Score
                    
                if child2Score < compare:
                    swap = child2N

            
            if swap != None:
                self._content[n] = self._content[swap]
                self._content[swap] = element
                n = swap
            else:
                break
                
        return

    def _bubble_up(self, n):
        # get element that has to be moved
        element = self._content[n]

        while n > 0:
            parentN = int(math.floor((n + 1) / 2)) - 1
            parent = self._content[parentN]

            # swap the elements if the parent is greater.
            if self._scorefn(element) < self._scorefn(parent):
                self._content[parentN] = element
                self._content[n] = parent

                # update 'n' to continue at the new position
                n = parentN
            else:
                break
        return

    def peek(self):
        return self._content[0]

    def size(self):
        return len(self._content)

    def push(self, element):
        self._content.append(element)
        
        self._bubble_up(len(self._content) - 1)

    def pop(self):
        result = self._content[0]
        end = self._content.pop()

        if len(self._content) > 0:
            self._content[0] = end
            self._sink_down(0)

        return result

    def remove(self, node):
        length = len(self._content)

        end = self._content.pop()
        for n in range(0, length):
            if self._content[n] == node:
                self._content[n] = end
                if self._scorefn(end) < self._scorefn(node):
                    self._bubble_up(n)
                else:
                    self._sink_down(n)

                return

            raise Exception("Node not found.")

