## Binary search - searches a sorted list recursively.

def binary_search(items, target_name, key=lambda item: item):
    return _binary_search_recursive(items, target_name, 0, len(items) - 1, key)


def _binary_search_recursive(items, target_name, low, high, key):
    # Base case: the search area is empty
    if low > high:
        return -1

    middle = (low + high) // 2
    middle_name = key(items[middle])

    if middle_name == target_name:
        left_result = _binary_search_recursive(
            items,
            target_name,
            low,
            middle - 1,
            key
        )

        if left_result != -1:
            return left_result

        return middle

    elif target_name < middle_name:
        return _binary_search_recursive(
            items,
            target_name,
            low,
            middle - 1,
            key
        )

    else:
        return _binary_search_recursive(
            items,
            target_name,
            middle + 1,
            high,
            key
        )
