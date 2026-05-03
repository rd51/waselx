"""AVL Tree (self-balancing binary search tree) implementation."""

from typing import Optional, List, Any


class AVLNode:
    """Node in an AVL tree."""
    
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1
        self.rotation_count = 0


class AVLTree:
    """Self-balancing binary search tree with height balancing."""
    
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.size = 0
        self.rotation_count = 0
    
    def insert(self, value: Any) -> bool:
        """Insert a value and maintain balance."""
        if self.root is None:
            self.root = AVLNode(value)
            self.size += 1
            return True
        
        self.root, inserted = self._insert_recursive(self.root, value)
        if inserted:
            self.size += 1
        return inserted
    
    def _insert_recursive(self, node: Optional[AVLNode], value: Any) -> tuple:
        """Recursive insert with balancing."""
        if node is None:
            return AVLNode(value), True
        
        if value < node.value:
            node.left, inserted = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right, inserted = self._insert_recursive(node.right, value)
        else:
            return node, False  # Duplicate
        
        if not inserted:
            return node, False
        
        node = self._balance(node)
        return node, True
    
    def _balance(self, node: AVLNode) -> AVLNode:
        """Balance node if needed."""
        self._update_height(node)
        balance = self._get_balance(node)
        
        # Left heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """Perform left rotation."""
        self.rotation_count += 1
        node.rotation_count += 1
        
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        
        self._update_height(node)
        self._update_height(new_root)
        
        return new_root
    
    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """Perform right rotation."""
        self.rotation_count += 1
        node.rotation_count += 1
        
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        
        self._update_height(node)
        self._update_height(new_root)
        
        return new_root
    
    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Get balance factor of node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of node."""
        return node.height if node else 0
    
    def _update_height(self, node: AVLNode):
        """Update height of node."""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def search(self, value: Any) -> bool:
        """Search for value in AVL tree."""
        def _search_recursive(node: Optional[AVLNode], value: Any) -> bool:
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
        """Delete a value from AVL tree."""
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            self.size -= 1
        return deleted
    
    def _delete_recursive(self, node: Optional[AVLNode], value: Any) -> tuple:
        """Recursive delete with balancing."""
        if node is None:
            return None, False
        
        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
        else:
            # Node to delete found
            if node.left is None and node.right is None:
                return None, True
            
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            
            # Find in-order successor
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right, _ = self._delete_recursive(node.right, min_node.value)
            self.size += 1
        
        if not deleted:
            return node, False
        
        node = self._balance(node)
        return node, True
    
    def _find_min(self, node: Optional[AVLNode]) -> Optional[AVLNode]:
        """Find node with minimum value."""
        while node and node.left:
            node = node.left
        return node
    
    def inorder_traversal(self) -> List[Any]:
        """In-order traversal."""
        result = []
        def _inorder(node: Optional[AVLNode]):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
        _inorder(self.root)
        return result
    
    def height(self) -> int:
        """Get tree height."""
        return self._get_height(self.root)
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, value: Any) -> bool:
        return self.search(value)
