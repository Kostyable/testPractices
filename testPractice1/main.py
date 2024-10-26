import doctest

def bubble_sort(lst):
    """Фукнкция сортировки пузырьком.

    >>> bubble_sort([3, 2, 4, 1, 5])
    [1, 2, 3, 4, 5]

    >>> bubble_sort([10, 9, 8, 7])
    [7, 8, 9, 10]

    >>> bubble_sort([1, 2, 3])
    [1, 2, 3]

    >>> bubble_sort([5, 5])
    [5, 5]

    >>> bubble_sort([-1])
    [-1]

    >>> bubble_sort([])
    []

    >>> bubble_sort([3, 2, 'four', 1, 5])
    Traceback (most recent call last):
        ...
    ValueError: Элементы списка должны быть числами

    >>> bubble_sort([[10], 9, 8, 7])
    Traceback (most recent call last):
        ...
    ValueError: Элементы списка должны быть числами

    >>> bubble_sort([1, 2, None])
    Traceback (most recent call last):
        ...
    ValueError: Элементы списка должны быть числами

    >>> bubble_sort(55)
    Traceback (most recent call last):
        ...
    TypeError: Входные данные должны быть списком

    >>> bubble_sort({-1})
    Traceback (most recent call last):
        ...
    TypeError: Входные данные должны быть списком

    >>> bubble_sort(None)
    Traceback (most recent call last):
        ...
    TypeError: Входные данные должны быть списком
    """

    if not isinstance(lst, list):
        raise TypeError("Входные данные должны быть списком")

    if not all(isinstance(i, (int, float)) for i in lst):
        raise ValueError("Элементы списка должны быть числами")

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

    return lst

if __name__ == "__main__":
    assert bubble_sort([3, 2, 4, 1, 5]) == [1, 2, 3, 4, 5], "Сортировка работает неправильно для списка [3, 2, 4, 1, 5]"
    assert bubble_sort([10, 9, 8, 7]) == [7, 8, 9, 10], "Сортировка работает неправильно для списка [10, 9, 8, 7]"
    assert bubble_sort([1, 2, 3]) == [1, 2, 3], "Сортировка работает неправильно для списка [1, 2, 3]"
    assert bubble_sort([5, 5]) == [5, 5], "Сортировка работает неправильно для списка [2, 2]"
    assert bubble_sort([-1]) == [-1], "Сортировка работает неправильно для списка [-1]"
    assert bubble_sort([]) == [], "Сортировка работает неправильно для пустого списка"

    try:
        print("Тест 1. Список со строкой")
        bubble_sort([3, 2, 'four', 1, 5])
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        print("Тест 2. Список с вложенным списком")
        bubble_sort([[10], 9, 8, 7])
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        print("Тест 3. Список с None")
        bubble_sort([1, 2, None])
    except ValueError as e:
        print(f"Ошибка: {e}")

    try:
        print("Тест 4. Ввод числа вместо списка")
        bubble_sort(55)
    except TypeError as e:
        print(f"Ошибка: {e}")

    try:
        print("Тест 5. Ввод множества вместо списка")
        bubble_sort({-1})
    except TypeError as e:
        print(f"Ошибка: {e}")

    try:
        print("Тест 6. Ввод None вместо списка")
        bubble_sort(None)
    except TypeError as e:
        print(f"Ошибка: {e}")

    doctest.testmod()
    print("Все тесты пройдены успешно")
