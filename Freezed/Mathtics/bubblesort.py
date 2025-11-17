def bubblesort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
if __name__ == "__main__":
    print(bubblesort([1,2,3,4,5,6,7]))
    