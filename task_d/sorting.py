"""Sorting algorithms implementation."""

from typing import List, Any, Callable, Tuple


def bubble_sort(arr: List[Any], key: Callable = None) -> Tuple[List[Any], int]:
    """
    Sort using bubble sort algorithm.
    
    Returns:
        Tuple of (sorted list, number of comparisons)
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if key:
                should_swap = key(arr[j], arr[j + 1]) > 0
            else:
                should_swap = arr[j] > arr[j + 1]
            
            if should_swap:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    return arr, comparisons


def merge_sort(arr: List[Any], key: Callable = None) -> Tuple[List[Any], int]:
    """
    Sort using merge sort algorithm.
    
    Returns:
        Tuple of (sorted list, number of comparisons)
    """
    comparisons = [0]  # Use list to modify in nested function
    
    def merge(left: List[Any], right: List[Any]) -> List[Any]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            
            if key:
                should_take_left = key(left[i], right[j]) <= 0
            else:
                should_take_left = left[i] <= right[j]
            
            if should_take_left:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def merge_sort_helper(arr: List[Any]) -> List[Any]:
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        
        return merge(left, right)
    
    sorted_arr = merge_sort_helper(arr)
    return sorted_arr, comparisons[0]


def quick_sort(arr: List[Any], key: Callable = None) -> Tuple[List[Any], int]:
    """
    Sort using quick sort algorithm.
    
    Returns:
        Tuple of (sorted list, number of comparisons)
    """
    comparisons = [0]
    
    def partition(arr: List[Any], low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            comparisons[0] += 1
            
            if key:
                should_swap = key(arr[j], pivot) < 0
            else:
                should_swap = arr[j] < pivot
            
            if should_swap:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort_helper(arr: List[Any], low: int, high: int):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi - 1)
            quick_sort_helper(arr, pi + 1, high)
    
    arr_copy = arr.copy()
    if len(arr_copy) > 0:
        quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    
    return arr_copy, comparisons[0]
