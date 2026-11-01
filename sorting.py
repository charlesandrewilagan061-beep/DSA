
MAX_NUMBERS = 30


def parse_numbers(text):
    """Turn '5, 3, 8' (commas or spaces) into [5, 3, 8]."""
    parts = text.replace(',', ' ').split()
    if not parts:
        raise ValueError('Please enter at least one number.')
    if len(parts) > MAX_NUMBERS:
        raise ValueError(f'Please enter at most {MAX_NUMBERS} numbers.')
    numbers = []
    for part in parts:
        try:
            value = float(part)
        except ValueError:
            raise ValueError(f'"{part}" is not a valid number.')
        numbers.append(int(value) if value.is_integer() else value)
    return numbers


class Recorder:
    """Collects one frame per animation step and counts comparisons and swaps.

    compare = indices being compared (yellow)
    swap    = indices being swapped or written (red)
    pivot   = index of the pivot (purple)
    marker  = smallest so far / boundary of the part being worked on (cyan)
    done    = indices already in their final place (green)
    tags    = (index, label) pairs shown under the tiles, e.g. (3, 'j')
    """

    def __init__(self):
        self.frames = []
        self.comparisons = 0
        self.swaps = 0

    def add(self, items, text, compare=(), swap=(), pivot=None,
            marker=(), done=(), compared=False, tags=()):
        if compare or compared:
            self.comparisons += 1
        if swap:
            self.swaps += 1
        labels = {}
        for index, label in tags:
            labels[index] = labels[index] + ', ' + label if index in labels else label
        self.frames.append({
            'values': list(items),
            'text': text,
            'compare': list(compare),
            'swap': list(swap),
            'pivot': pivot,
            'marker': list(marker),
            'done': sorted(done),
            'tags': labels,
            'comparisons': self.comparisons,
            'swaps': self.swaps,
        })


def bubble_sort(items, rec):
    n = len(items)
    done = set()
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            a, b = items[j], items[j + 1]
            if a > b:
                rec.add(items, f'{a} > {b}, they are out of order, so swap them.',
                        compare=(j, j + 1), done=done, tags=[(j, 'j'), (j + 1, 'j+1')])
                items[j], items[j + 1] = b, a
                swapped = True
                rec.add(items, f'Swapped {a} and {b}.', swap=(j, j + 1), done=done,
                        tags=[(j, 'j'), (j + 1, 'j+1')])
            else:
                rec.add(items, f'{a} <= {b}, already in order.',
                        compare=(j, j + 1), done=done, tags=[(j, 'j'), (j + 1, 'j+1')])
        done.add(n - i - 1)
        if not swapped:
            break
        rec.add(items, f'End of pass {i + 1}: {items[n - i - 1]} is now in its final place.',
                done=done)


def selection_sort(items, rec):
    n = len(items)
    done = set()
    for i in range(n - 1):
        smallest = i
        rec.add(items, f'Pass {i + 1}: find the smallest value from index {i} onward. '
                       f'Start with {items[i]}.', marker=(smallest,), done=done,
                tags=[(smallest, 'min')])
        for j in range(i + 1, n):
            if items[j] < items[smallest]:
                rec.add(items, f'{items[j]} < {items[smallest]}, {items[j]} is the new smallest.',
                        compare=(j,), marker=(smallest,), done=done,
                        tags=[(smallest, 'min'), (j, 'j')])
                smallest = j
            else:
                rec.add(items, f'{items[j]} >= {items[smallest]}, the smallest stays the same.',
                        compare=(j,), marker=(smallest,), done=done,
                        tags=[(smallest, 'min'), (j, 'j')])
        done.add(i)
        if smallest != i:
            items[i], items[smallest] = items[smallest], items[i]
            rec.add(items, f'Swap the smallest value ({items[i]}) into index {i}.',
                    swap=(i, smallest), done=done)
        else:
            rec.add(items, f'{items[i]} is already the smallest, no swap needed.', done=done)


def insertion_sort(items, rec):
    done = {0}
    for i in range(1, len(items)):
        key = items[i]
        rec.add(items, f'Take {key} and insert it into the sorted part on the left.',
                marker=(i,), done=done, tags=[(i, 'key')])
        j = i
        while j > 0:
            if items[j - 1] > items[j]:
                rec.add(items, f'{items[j - 1]} > {items[j]}, so {key} moves left.',
                        compare=(j - 1, j), done=done, tags=[(j, 'key'), (j - 1, 'left')])
                items[j - 1], items[j] = items[j], items[j - 1]
                rec.add(items, f'Swapped, {key} is now at index {j - 1}.',
                        swap=(j - 1, j), done=done, tags=[(j - 1, 'key')])
                j -= 1
            else:
                rec.add(items, f'{items[j - 1]} <= {items[j]}, {key} is in the right place.',
                        compare=(j - 1, j), done=done, tags=[(j, 'key'), (j - 1, 'left')])
                break
        done.add(i)


def merge_sort(items, low, high, rec):
    if high - low <= 1:
        return
    middle = (low + high) // 2
    merge_sort(items, low, middle, rec)
    merge_sort(items, middle, high, rec)

    left = items[low:middle]
    right = items[middle:high]
    block = tuple(range(low, high))
    rec.add(items, f'Merge [{" ".join(map(str, left))}] and [{" ".join(map(str, right))}] '
                   f'into one sorted block.', marker=block)

    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            text = f'{left[i]} <= {right[j]}, write {left[i]} at index {k}.'
            items[k] = left[i]
            i += 1
        else:
            text = f'{left[i]} > {right[j]}, write {right[j]} at index {k}.'
            items[k] = right[j]
            j += 1
        rec.add(items, text, swap=(k,), marker=block, compared=True, tags=[(k, 'k')])
        k += 1
    while i < len(left):
        items[k] = left[i]
        rec.add(items, f'Copy the leftover {left[i]} to index {k}.', swap=(k,), marker=block,
                tags=[(k, 'k')])
        i += 1
        k += 1
    while j < len(right):
        items[k] = right[j]
        rec.add(items, f'Copy the leftover {right[j]} to index {k}.', swap=(k,), marker=block,
                tags=[(k, 'k')])
        j += 1
        k += 1


def quick_sort(items, low, high, rec, done):
    if low > high:
        return
    if low == high:
        done.add(low)
        rec.add(items, f'{items[low]} is alone, so it is in its final place.', done=done)
        return

    pivot = items[high]
    rec.add(items, f'Pick {pivot} (the last value) as the pivot.', pivot=high,
            marker=(low,), done=done, tags=[(high, 'pivot'), (low, 'i')])
    i = low
    for j in range(low, high):
        if items[j] <= pivot:
            rec.add(items, f'{items[j]} <= {pivot}, it belongs on the left side.',
                    compare=(j,), pivot=high, marker=(i,), done=done,
                    tags=[(high, 'pivot'), (i, 'i'), (j, 'j')])
            if i != j:
                items[i], items[j] = items[j], items[i]
                rec.add(items, f'Moved {items[i]} to the left side.',
                        swap=(i, j), pivot=high, done=done,
                        tags=[(high, 'pivot'), (i, 'i'), (j, 'j')])
            i += 1
        else:
            rec.add(items, f'{items[j]} > {pivot}, it stays on the right side.',
                    compare=(j,), pivot=high, marker=(i,), done=done,
                    tags=[(high, 'pivot'), (i, 'i'), (j, 'j')])

    done.add(i)
    if i != high:
        items[i], items[high] = items[high], items[i]
        rec.add(items, f'Place the pivot {pivot} between the smaller and larger values (index {i}).',
                swap=(i, high), done=done, tags=[(i, 'pivot')])
    else:
        rec.add(items, f'The pivot {pivot} is already in its final place.', pivot=i, done=done,
                tags=[(i, 'pivot')])

    quick_sort(items, low, i - 1, rec, done)
    quick_sort(items, i + 1, high, rec, done)


ALGORITHMS = {
    'bubble': 'Bubble sort',
    'selection': 'Selection sort',
    'insertion': 'Insertion sort',
    'merge': 'Merge sort',
    'quick': 'Quick sort',
}

DESCRIPTIONS = {
    'bubble': {
        'about': 'Compares neighbouring items and swaps them when they are in the wrong order. '
                 'After each pass the largest remaining value has "bubbled" to the end.',
        'time': 'O(n²)', 'space': 'O(1)', 'stable': 'Yes',
    },
    'selection': {
        'about': 'Finds the smallest item in the unsorted part and swaps it to the front. '
                 'The sorted part grows one item at a time.',
        'time': 'O(n²)', 'space': 'O(1)', 'stable': 'No',
    },
    'insertion': {
        'about': 'Takes one item at a time and slides it left until it sits in the right '
                 'place in the sorted part. Fast on lists that are almost sorted.',
        'time': 'O(n²)', 'space': 'O(1)', 'stable': 'Yes',
    },
    'merge': {
        'about': 'Splits the list in half again and again, then merges the sorted halves back '
                 'together. Always takes the same amount of work, whatever the input.',
        'time': 'O(n log n)', 'space': 'O(n)', 'stable': 'Yes',
    },
    'quick': {
        'about': 'Picks a pivot, puts smaller values on its left and larger values on its right, '
                 'then sorts both sides the same way. Usually the fastest in practice.',
        'time': 'O(n log n)', 'space': 'O(log n)', 'stable': 'No',
    },
}


def sort_numbers(text, algorithm):
    if algorithm not in ALGORITHMS:
        raise ValueError('Please choose a sorting algorithm.')
    items = parse_numbers(text)
    rec = Recorder()
    rec.add(items, 'The unsorted list. Press Next, or let it play.')

    if algorithm == 'bubble':
        bubble_sort(items, rec)
    elif algorithm == 'selection':
        selection_sort(items, rec)
    elif algorithm == 'insertion':
        insertion_sort(items, rec)
    elif algorithm == 'merge':
        merge_sort(items, 0, len(items), rec)
    elif algorithm == 'quick':
        quick_sort(items, 0, len(items) - 1, rec, set())

    rec.add(items, 'Done! The list is sorted.', done=range(len(items)))
    return items, rec.frames