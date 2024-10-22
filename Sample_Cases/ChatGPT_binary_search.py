# Generated using ChatGPT 4o mini
# Prompt: Binary Search in Python
def binary_search_iterative(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore the left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore the right half
        else:
            right = mid - 1
    
    # Target is not present in the array
    return -1

# Example usage
arr = [2, 3, 4, 10, 40]
target = 10
result = binary_search_iterative(arr, target)
print(f"Element found at index: {result}")

def binary_search_recursive(arr, target, left, right):
    # Base case: if the range is invalid
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    # Check if target is present at mid
    if arr[mid] == target:
        return mid
    # If target is greater, ignore the left half
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    # If target is smaller, ignore the right half
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Example usage
arr = [2, 3, 4, 10, 40]
target = 10
result = binary_search_recursive(arr, target, 0, len(arr) - 1)
print(f"Element found at index: {result}")
