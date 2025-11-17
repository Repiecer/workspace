
def selection(arr: list) -> list:
    for i in range(len(arr)):arr[arr.index(min(arr[i:]))], arr[i] = arr[i], min(arr[i:])
    return arr

if __name__ == '__main__':
    print(selection([9, 6, 4, 8, 7, 8, 5, 3, 1]))