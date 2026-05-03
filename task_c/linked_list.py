"""Singly Linked List implementation."""

from typing import Optional, Any, List


class Node:
    """Node in a linked list."""
    
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['Node'] = None


class LinkedList:
    """Singly linked list data structure."""
    
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0
    
    def insert_at_head(self, value: Any):
        """Insert value at beginning."""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at_tail(self, value: Any):
        """Insert value at end."""
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def insert_at(self, index: int, value: Any) -> bool:
        """Insert at specific index (0-based). Returns True if successful."""
        if index < 0 or index > self.size:
            return False
        
        if index == 0:
            self.insert_at_head(value)
            return True
        
        current = self.head
        for _ in range(index - 1):
            if current is None:
                return False
            current = current.next
        
        new_node = Node(value)
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True
    
    def delete_at_head(self) -> Optional[Any]:
        """Delete and return head value."""
        if self.head is None:
            return None
        
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value
    
    def delete_at(self, index: int) -> Optional[Any]:
        """Delete at index and return value."""
        if index < 0 or index >= self.size or self.head is None:
            return None
        
        if index == 0:
            return self.delete_at_head()
        
        current = self.head
        for _ in range(index - 1):
            if current is None:
                return None
            current = current.next
        
        if current.next is None:
            return None
        
        value = current.next.value
        current.next = current.next.next
        self.size -= 1
        return value
    
    def search(self, value: Any) -> int:
        """Search for value, return index or -1."""
        current = self.head
        index = 0
        
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def get_at(self, index: int) -> Optional[Any]:
        """Get value at index."""
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current.value if current else None
    
    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        result = []
        current = self.head
        
        while current:
            result.append(current.value)
            current = current.next
        
        return result
    
    def reverse(self):
        """Reverse the linked list in-place."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        return str(self.to_list())
