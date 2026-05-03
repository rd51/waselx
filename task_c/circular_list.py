"""Circular Linked List implementation."""

from typing import Optional, Any, List


class Node:
    """Node in a circular linked list."""
    
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['Node'] = None


class CircularLinkedList:
    """Circular linked list data structure."""
    
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0
    
    def insert(self, value: Any):
        """Insert value at end (maintains circular structure)."""
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
            new_node.next = new_node  # Point to itself
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
        
        self.size += 1
    
    def insert_at_head(self, value: Any):
        """Insert at beginning."""
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
        else:
            # Find last node
            current = self.head
            while current.next != self.head:
                current = current.next
            
            new_node.next = self.head
            current.next = new_node
            self.head = new_node
        
        self.size += 1
    
    def delete(self, value: Any) -> bool:
        """Delete first occurrence of value."""
        if self.head is None:
            return False
        
        # Special case: delete head
        if self.head.value == value:
            if self.head.next == self.head:  # Only one node
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            
            self.size -= 1
            return True
        
        # Find and delete
        current = self.head
        while current.next != self.head:
            if current.next.value == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at(self, index: int) -> Optional[Any]:
        """Delete at position (circular)."""
        if index < 0 or index >= self.size or self.head is None:
            return None
        
        if index == 0:
            value = self.head.value
            if self.head.next == self.head:
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            self.size -= 1
            return value
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        value = current.next.value
        current.next = current.next.next
        self.size -= 1
        return value
    
    def rotate(self, positions: int = 1):
        """Rotate list by moving head position."""
        if self.size <= 1:
            return
        
        positions = positions % self.size
        for _ in range(positions):
            if self.head:
                current = self.head
                while current.next != self.head:
                    current = current.next
                self.head = self.head.next
    
    def to_list(self, max_items: Optional[int] = None) -> List[Any]:
        """Convert to list (with optional limit to prevent infinite loop in demo)."""
        result = []
        if self.head is None:
            return result
        
        current = self.head
        count = 0
        limit = max_items if max_items else self.size
        
        while count < limit:
            result.append(current.value)
            current = current.next
            count += 1
            
            if current == self.head:
                break
        
        return result
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        return str(self.to_list())
