"""Priority Queue implementation using heap."""

from typing import Any, Tuple, List


class PriorityQueue:
    """Priority queue for managing tasks by priority (min-heap based)."""
    
    def __init__(self):
        """Initialize empty heap. Index 0 unused for easier parent/child calculation."""
        self.heap: List[Tuple[int, float, Any]] = []  # (priority, order, value)
        self.order_counter = 0  # For FIFO within same priority
    
    def enqueue(self, value: Any, priority: int = 0):
        """
        Add item with priority. Lower priority number = higher importance.
        Items with same priority dequeued in FIFO order.
        """
        self.heap.append((priority, self.order_counter, value))
        self.order_counter += 1
        self._heapify_up(len(self.heap) - 1)
    
    def dequeue(self) -> Any:
        """Remove and return highest priority (lowest number) item."""
        if not self.heap:
            raise IndexError("dequeue from empty PriorityQueue")
        
        if len(self.heap) == 1:
            return self.heap.pop()[2]
        
        # Swap root with last element
        priority, order, value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return value
    
    def peek(self) -> Tuple[int, Any]:
        """Return priority and value of highest priority item without removing."""
        if not self.heap:
            raise IndexError("peek from empty PriorityQueue")
        return self.heap[0][0], self.heap[0][2]
    
    def _heapify_up(self, index: int):
        """Move element up to maintain heap property."""
        while index > 0:
            parent_idx = (index - 1) // 2
            
            if self.heap[index] < self.heap[parent_idx]:
                self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
                index = parent_idx
            else:
                break
    
    def _heapify_down(self, index: int):
        """Move element down to maintain heap property."""
        n = len(self.heap)
        
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            
            if left_child < n and self.heap[left_child] < self.heap[smallest]:
                smallest = left_child
            
            if right_child < n and self.heap[right_child] < self.heap[smallest]:
                smallest = right_child
            
            if smallest == index:
                break
            
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.heap) == 0
    
    def __len__(self) -> int:
        return len(self.heap)
    
    def __str__(self) -> str:
        return f"PriorityQueue({len(self.heap)} items)"
