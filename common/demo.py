def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1], arr[j]
    return arr

arr = [9,99,1,10,20,30]
sorted_arr = bubble_sort(arr=arr)
print(sorted_arr)