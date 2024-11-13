from collections.abc import MutableMapping
from typing import Any, Generator
import random


class Node:
    """
    A node in the Treap, which holds a key, a value, and a priority.

    Attributes:
        key (int): The key used for comparison in the Treap.
        value (Any): The value associated with the key.
        priority (int): The priority of the node, used to maintain the heap property.
        left (Node | None): The left child of the node.
        right (Node | None): The right child of the node.
    """

    def __init__(self, key: int, value: Any, priority: int | None = None) -> None:
        """
        Initialize a new node with a given key, value, and priority.

        Args:
            key (int): The key of the node.
            value (Any): The value associated with the key.
            priority (int | None): The priority of the node. If not provided, a random priority is assigned.
        """
        self.key: int = key
        self.value: Any = value
        self.priority: int = (
            priority if priority is not None else random.randint(0, 100)
        )
        self.left: Node | None = None
        self.right: Node | None = None


class Treap(MutableMapping):
    """
    A Treap is a hybrid data structure that combines properties of a Binary Search Tree (BST)
    and a Max Heap. The Treap maintains the Binary Search Tree property based on the keys,
    and a Max Heap property based on the priorities.

    This class provides efficient insertions, deletions, and lookups.

    Attributes:
        root (Node | None): The root node of the Treap, or None if the Treap is empty.
        __size (int): The number of elements in the Treap.

    Methods:
        __getitem__(key): Retrieves the value associated with the given key.
        __setitem__(key, value): Inserts the given key-value pair into the Treap.
        __delitem__(key): Deletes the key-value pair associated with the given key.
        __contains__(key): Checks whether the key is present in the Treap.
        __iter__(): Iterates over the keys of the Treap in ascending order.
        __reversed__(): Iterates over the keys of the Treap in descending order.
        __len__(): Returns the number of elements in the Treap.
    """

    def __init__(self) -> None:
        """
        Initialize an empty Treap.
        """
        self.root: Node | None = None
        self.__size: int = 0

    def _rotate_right(self, node: Node) -> Node:
        """
        Perform a right rotation on the given node to maintain heap property.

        Args:
            node (Node): The node on which the rotation will be performed.

        Returns:
            Node: The new root of the subtree after rotation.
        """
        if node.left is None:
            return node
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node: Node) -> Node:
        """
        Perform a left rotation on the given node to maintain heap property.

        Args:
            node (Node): The node on which the rotation will be performed.

        Returns:
            Node: The new root of the subtree after rotation.
        """
        if node.right is None:
            return node
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def _insert(self, root: Node | None, key: int, value: Any) -> Node:
        """
        Insert a new node with the given key and value into the Treap.

        Args:
            root (Node | None): The root of the current subtree.
            key (int): The key of the node to insert.
            value (Any): The value of the node to insert.

        Returns:
            Node: The root of the modified subtree after insertion.
        """
        if root is None:
            return Node(key, value)

        if key < root.key:
            root.left = self._insert(root.left, key, value)
            if root.left.priority > root.priority:
                root = self._rotate_right(root)
        elif key > root.key:
            root.right = self._insert(root.right, key, value)
            if root.right.priority > root.priority:
                root = self._rotate_left(root)
        else:
            root.value = value

        return root

    def __getitem__(self, key: int) -> Any:
        """
        Retrieve the value associated with the given key from the Treap.

        Args:
            key (int): The key of the node to retrieve.

        Returns:
            Any: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        raise KeyError(f"Key {key} not found.")

    def __setitem__(self, key: int, value: Any) -> None:
        """
        Insert a new key-value pair or update the value of an existing key in the Treap.

        Args:
            key (int): The key of the node to insert or update.
            value (Any): The value to associate with the key.
        """
        self.root = self._insert(self.root, key, value)
        self.__size += 1

    def __delitem__(self, key: int) -> None:
        """
        Delete the node with the given key from the Treap.

        Args:
            key (int): The key of the node to delete.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self.__size -= 1
        else:
            raise KeyError(f"Key {key} not found.")

    def _delete(self, root: Node | None, key: int) -> tuple[Node | None, bool]:
        """
        Delete a node with the given key from the Treap.

        Args:
            root (Node | None): The root of the current subtree.
            key (int): The key of the node to delete.

        Returns:
            tuple[Node | None, bool]: A tuple containing the new root of the modified subtree and a boolean indicating
                                       whether a node was deleted.
        """
        if root is None:
            return None, False

        deleted = False
        if key < root.key:
            root.left, deleted = self._delete(root.left, key)
        elif key > root.key:
            root.right, deleted = self._delete(root.right, key)
        else:
            deleted = True
            if root.left is None:
                return root.right, deleted
            elif root.right is None:
                return root.left, deleted
            elif root.left.priority < root.right.priority:
                root = self._rotate_left(root)
                root.left, _ = self._delete(root.left, key)
            else:
                root = self._rotate_right(root)
                root.right, _ = self._delete(root.right, key)

        return root, deleted

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key exists in the Treap.

        Args:
            key (int): The key to check.

        Returns:
            bool: True if the key is in the Treap, False otherwise.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __iter__(self) -> Generator[int, None, None]:
        """
        Iterate over the keys of the Treap in ascending order.

        Returns:
            Generator[int]: A generator yielding keys in ascending order.
        """
        yield from self._in_order(self.root)

    def __reversed__(self) -> Generator[int, None, None]:
        """
        Iterate over the keys of the Treap in descending order.

        Returns:
            Generator[int]: A generator yielding keys in descending order.
        """
        yield from self._reverse_in_order(self.root)

    def _in_order(self, node: Node | None) -> Generator[int, None, None]:
        """
        Helper method for in-order traversal of the Treap.

        Args:
            node (Node | None): The current node in the traversal.

        Returns:
            Generator[int]: A generator yielding keys in ascending order.
        """
        if node is not None:
            yield from self._in_order(node.left)
            yield node.key
            yield from self._in_order(node.right)

    def _reverse_in_order(self, node: Node | None) -> Generator[int, None, None]:
        """
        Helper method for reverse in-order traversal of the Treap.

        Args:
            node (Node | None): The current node in the traversal.

        Returns:
            Generator[int]: A generator yielding keys in descending order.
        """
        if node is not None:
            yield from self._reverse_in_order(node.right)
            yield node.key
            yield from self._reverse_in_order(node.left)

    def __len__(self) -> int:
        """
        Get the number of nodes in the Treap.

        Returns:
            int: The number of nodes in the Treap.
        """
        return self.__size
