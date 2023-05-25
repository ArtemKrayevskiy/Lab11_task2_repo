"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from random import shuffle , choice
from copy import deepcopy
import time

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''


        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(c) for c in [top.left , top.right])
            
        return height1(self._root)
                

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() == 0:
            return False
        if self.height() < 2*log(self._size+1)-1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst_of_sorted = list(self.inorder())
        for i in range(len(lst_of_sorted)):
            if low <= lst_of_sorted[i]:
                lower_index = i
                break
        for i in range(len(lst_of_sorted)):
            if lst_of_sorted[i] >= high:
                higher_index =i
                break
        return lst_of_sorted[lower_index : higher_index +1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def helper_func(lst):
            if len(lst) == 1:
                return  BSTNode(lst[0])
            if len(lst) <= 0:
                return None
            new_root = BSTNode(lst[len(lst)//2])
            new_root.left = helper_func(lst[:len(lst)//2])
            new_root.right = helper_func(lst[(len(lst)//2) + 1:])
            return new_root
        lst_of_sorted = list(self.inorder())
        self._root = helper_func(lst_of_sorted)
        return self._root
    
    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst_of_sorted = list(self.inorder())
        for i in lst_of_sorted:
            if i > item:
                return i
        return None

        
    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self.height() == 0:
            return None
        lst_of_sorted = list(self.inorder())
        for i in range(len(lst_of_sorted)):
            if lst_of_sorted[i] >= item:
                try:
                    my_number = lst_of_sorted[i-1]
                except IndexError:
                    return None
                if i-1 >0:
                    return my_number
                else:
                    return None
        return None
    

    def add_without_recursion(self , item):

        new_node = BSTNode(item)
        if self.isEmpty():
            self._root = new_node
            self._size +=1
            return None
    
        mynode = self._root
        while True:
            if new_node.data < mynode.data:
                if mynode.left == None:
                    mynode.left = new_node
                    self._size += 1
                    return None
                else:
                    mynode = mynode.left
            else:
                if mynode.right == None:
                    mynode.right = new_node
                    self._size += 1
                    return None
                else:
                    mynode = mynode.right

    def find_without_recursion(self , item):
        mynode = self._root
        while mynode != None:
            if item == mynode.data:
                return mynode.data
            elif item < mynode.data:
                mynode = mynode.left
            elif item > mynode.data:
                mynode = mynode.right


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        with open(path ,'r' ) as file:
            full_lst = [i.replace('\n' ,'') for i in file.readlines()]
        words_to_search = []
        while len(words_to_search) != 10000:
            word = choice(full_lst)
            if word not in words_to_search:
                words_to_search.append(word)

        ###FINDING IN LIST WITH INDEX
        start_time = time.time()
        for i in words_to_search:
            full_lst.index(i)
        end_time = time.time()
        print("Searching for 10000 words with index method: " + str(end_time - start_time))


        ###SORTED TREE
        sorted_tree = LinkedBST()
        for i in full_lst:
            sorted_tree.add_without_recursion(i)

        start_time = time.time()
        for i in words_to_search:
            sorted_tree.find_without_recursion(i)
        end_time = time.time()
        print("Searching for 10000 words in tree with sorted dictionary: " + str(end_time - start_time))
            
        ###RANDOM TREE
        shuffle(full_lst)
        not_sorted_tree = LinkedBST()
        for i in full_lst:
            not_sorted_tree.add_without_recursion(i)

        start_time = time.time()
        for i in words_to_search:
            not_sorted_tree.find(i)
        end_time = time.time()
        print("Searching for 10000 words in tree with not sorted dictionary: " + str(end_time - start_time))

        ###Random tree rebalanced
        not_sorted_tree._root = not_sorted_tree.rebalance()
        start_time = time.time()
        for i in words_to_search:
            not_sorted_tree.find(i)
        end_time = time.time()
        print("Searching for 10000 words in rebalanced tree with not sorted dictionary: " + str(end_time - start_time))


mytree = LinkedBST()
print(mytree.demo_bst('words.txt'))
mytree.add(1)
mytree.add(2)
mytree.add(3)
mytree.add(4)
mytree.add(5)
mytree.add(6)
mytree.add(7)
mytree.add(8)
mytree.add(9)
mytree.add(10)
# print(mytree.predecessor(14))

