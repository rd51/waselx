"""Stack (LIFO) data structure implementation."""

from typing import Any, List, Optional


class Stack:
    """Stack data structure for LIFO operations."""
    
    def __init__(self):
        self.items: List[Any] = []
    
    def push(self, value: Any):
        """Add value to top of stack."""
        self.items.append(value)
    
    def pop(self) -> Any:
        """Remove and return top value."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()
    
    def peek(self) -> Any:
        """Return top value without removing."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Return number of items."""
        return len(self.items)
    
    def clear(self):
        """Remove all items."""
        self.items.clear()
    
    def to_list(self) -> List[Any]:
        """Return copy of stack contents (top is last)."""
        return self.items.copy()
    
    def __len__(self) -> int:
        return len(self.items)
    
    def __str__(self) -> str:
        return f"Stack({self.items})"
