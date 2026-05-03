"""Binary Search Tree implementation."""

from typing import Optional, List, Any


class Node:
    """Node in a binary search tree."""
    
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.height = 1


class BinarySearchTree:
    """Binary Search Tree for efficient searching and sorting."""
    
    def __init__(self):
        self.root: Optional[Node] = None
        self.size = 0
    
    def insert(self, value: Any) -> bool:
        """Insert a value into BST. Returns True if inserted, False if duplicate."""
        if self.root is None:
            self.root = Node(value)
            self.size += 1
            return True
        
        def _insert_recursive(node: Node, value: Any) -> bool:
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                    self.size += 1
                    return True
                else:
                    return _insert_recursive(node.left, value)
            elif value > node.value:
                if node.right is None:
                    node.right = Node(value)
                    self.size += 1
                    return True
                else:
                    return _insert_recursive(node.right, value)
            else:
                return False  # Duplicate
        
        return _insert_recursive(self.root, value)
    
    def search(self, value: Any) -> bool:
        """Search for a value in BST."""
        def _search_recursive(node: Optional[Node], value: Any) -> bool:
            if node is None:
                return False
            
            if value == node.value:
                return True
            elif value < node.value:
                return _search_recursive(node.left, value)
            else:
                return _search_recursive(node.right, value)
        
        return _search_recursive(self.root, value)
    
    def delete(self, value: Any) -> bool:
        """Delete a value from BST. Returns True if deleted, False if not found."""
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            self.size -= 1
        return deleted
    
    def _delete_recursive(self, node: Optional[Node], value: Any) -> tuple:
        """Recursive helper for delete. Returns (new_root, was_deleted)."""
        if node is None:
            return None, False
        
        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
            return node, deleted
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
            return node, deleted
        else:
            # Node to delete found
            # Case 1: No children (leaf)
            if node.left is None and node.right is None:
                return None, True
            
            # Case 2: One child
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            
            # Case 3: Two children - find in-order successor
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right, _ = self._delete_recursive(node.right, min_node.value)
            self.size += 1  # Compensate for the recursive delete
            return node, True
    
    def _find_min(self, node: Optional[Node]) -> Optional[Node]:
        """Find node with minimum value in subtree."""
        while node and node.left:
            node = node.left
        return node
    
    def inorder_traversal(self) -> List[Any]:
        """Left-Root-Right traversal."""
        result = []
        def _inorder(node: Optional[Node]):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
        _inorder(self.root)
        return result
    
    def preorder_traversal(self) -> List[Any]:
        """Root-Left-Right traversal."""
        result = []
        def _preorder(node: Optional[Node]):
            if node:
                result.append(node.value)
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        return result
    
    def postorder_traversal(self) -> List[Any]:
        """Left-Right-Root traversal."""
        result = []
        def _postorder(node: Optional[Node]):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.value)
        _postorder(self.root)
        return result
    
    def height(self) -> int:
        """Get height of tree."""
        def _height(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
        
        return _height(self.root)
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, value: Any) -> bool:
        return self.search(value)
