# you may use pandas only for IO reason
# Using it to do sort will impact your grade
# import pandas as pd
import random
import timeit


def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.
        
    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated
            
        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)  
        # record the time consumption of executing the method
        time = timeit.default_timer() - start
        
        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result
    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number 
        self.cols: the col number 
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 1

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly. 
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set, 
        as it is not UTF-8.
        You are allowed to use pandas or csv reader, 
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        with open(fileName, "r", encoding = 'latin-1') as file:
            for line in file:
                parts = line.strip().split(",")
                artist = parts[0]
                album_num = int(parts[1])
                track_num = int(parts[2])
                self.data.append([artist, album_num, track_num])
            
            self.rows = len(self.data)
            if self.data:
                self.cols = 3


    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        print(f"{'Artist Name':<30} {'Albums':<10} {'Tracks':<10}")
        print("-" * 50)
        for row in self.data:
            print(f"{row[0]:<30} {row[1]:<10} {row[2]:<10}")


    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.shuffle(self.data)

    @timeFunc
    def binarySearch(self, key: int | str, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        left = 0
        right = self.rows - 1

        while left <= right:
            mid = (left + right) // 2
            mid_value = self.data[mid][keyIndex]

            if mid_value == key:
                return mid

            if mid_value < key:
                left = mid + 1
            else: 
                right = mid - 1

        return -1


    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        for i in range(self.rows):
            if self.data[i][keyIndex] == key:
                return i
        return -1


    @timeFunc
    def bubbleSort(self, keyIndex: int):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        n = self.rows
        for i in range(n-1):
            for j in range(n-i-1):
                if self.data[j][keyIndex] > self.data[j+1][keyIndex]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]


    def merge(self, L: list, R: list, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.
        

        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        # Implementation details...
        result = []
        i = j = 0

        while i < len(L) and j < len(R):
            if L[i][keyIndex] < R[j][keyIndex]:
                result.append(L[i])
                i += 1
            else:
                result.append(R[j])
                j += 1

        result.extend(L[i:])
        result.extend(R[j:])

        return result

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        self.data = self._mergeSort(self.data, keyIndex)

    def _mergeSort(self, arr, keyIndex):

        # This is the helper function for merge sort.
        # You may change the name of this function or even not have it.
        # This is a helper method for mergeSort
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        sortedL = self._mergeSort(L, keyIndex)
        sortedR = self._mergeSort(R, keyIndex)

        return self.merge(sortedL, sortedR, keyIndex)

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # Implementation details...
        if self.rows > 0:
            self._quickSort(self.data, 0, self.rows-1, keyIndex)
        pass

    def _quickSort(self, arr, low, high, keyIndex):
        '''
        Parameters
        ----------
        arr : list
            The list need to be sort.
        low : int
            The index th

        '''
        if low < high:
            pi = self._partition(arr, low, high, keyIndex)

            self._quickSort(arr, low, pi-1, keyIndex)
            self._quickSort(arr, pi+1, high, keyIndex)

    def _partition(self, arr, low, high, keyIndex):
        pi = arr[high][keyIndex]
        left = low
        right = low
        while right < high:
            if arr[right][keyIndex] < pi:
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
            right += 1

        arr[left], arr[high] = arr[high], arr[left]
        return left


    def comment(self):
        '''
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it. 
        '''
        print("For searching, sequential search runs in O(n) time and does not require sorted data, while binary search operates in "
        "O(log n) time but only works correctly on pre-sorted data." \
        "For sorting, Bubble sort runs in O(n^2) time and is generally the least efficient because every pair of adjacent elements " \
        "may need to be compared repeatedly; however, it uses O(1) space. Merge sort consistently performs in O(n log n) time and is " \
        "stable, but it requires additional O(n) space due to the merging process. Quick sort also has an average time complexity of " \
        "O(n log n) and works in-place with O(log n) space, but its worst-case time is O(n^2), especially when many elements have the " \
        "same value.")



# create instance and call the following instance method
# using decroator to decroate each instance method
def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = 'music.csv'
    myLibrary.readFile(filePath)

    idx = 0
    myLibrary.data.sort(key = lambda data: data[idx])
    myLibrary.seqSearch(key = "30 Seconds To Mars", keyIndex=idx)
    myLibrary.binarySearch(key = "30 Seconds To Mars", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()
    myLibrary.comment()

if __name__ == "__main__":
    main()

