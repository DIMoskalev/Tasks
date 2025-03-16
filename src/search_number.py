# Если список уже в функции, то она будет выглядеть вот так:
def search(number: id) -> bool:
    list_numbers = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    left = 0
    right = len(list_numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if list_numbers[mid] == number:
            return True
        elif list_numbers[mid] < number:
            left = mid + 1
        else:
            right = mid - 1
    return False


print(search(357))
# Выведет False
print(search(705))
# Выведет True


# Если список будет передаваться в функцию, то вот так:
def search_num_in_list(number: id, list_numbers: list) -> bool:
    left = 0
    right = len(list_numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if list_numbers[mid] == number:
            return True
        elif list_numbers[mid] < number:
            left = mid + 1
        else:
            right = mid - 1
    return False


list_numbers_out = [1, 2, 3, 45, 356, 569, 600, 705, 923]

print(search_num_in_list(357, list_numbers_out))
# Выведет False
print(search_num_in_list(705, list_numbers_out))
# Выведет True

# В обоих случаях функция использует алгоритм бинарного поиска, который как раз использует сложность O(log n).
# Этот алгоритм работает быстрее, тк он делит список на две части на каждом шаге, а не просто перебирает элементы.
# Cложность O(n) была бы при обычном переборе, к примеру: True if number in list_numbers else False
