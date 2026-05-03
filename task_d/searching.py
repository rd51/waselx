"""Searching algorithms implementation."""

from typing import List, Any, Tuple, Optional


def linear_search(arr: List[Any], target: Any) -> Tuple[Optional[int], int]:
    """
    Search using linear search.
    
    Returns:
        Tuple of (index or None, number of comparisons)
    """
    comparisons = 0
    
    for i, value in enumerate(arr):
        comparisons += 1
        if value == target:
            return i, comparisons
    
    return None, comparisons


def binary_search(arr: List[Any], target: Any) -> Tuple[Optional[int], int]:
    """
    Search using binary search (requires sorted array).
    
    Returns:
        Tuple of (index or None, number of comparisons)
    """
    comparisons = [0]
    
    def binary_search_helper(left: int, right: int) -> Optional[int]:
        if left > right:
            return None
        
        mid = (left + right) // 2
        comparisons[0] += 1
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            comparisons[0] += 1
            return binary_search_helper(mid + 1, right)
        else:
            comparisons[0] += 1
            return binary_search_helper(left, mid - 1)
    
    result = binary_search_helper(0, len(arr) - 1)
    return result, comparisons[0]


def binary_search_iterative(arr: List[Any], target: Any) -> Tuple[Optional[int], int]:
    """
    Binary search - iterative version.
    
    Returns:
        Tuple of (index or None, number of comparisons)
    """
    comparisons = 0
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None, comparisons
