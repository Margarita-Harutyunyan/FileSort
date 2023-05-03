import random
import pickle
import functools

class BigFile:
    def __init__(self, fileName, numCount, spaceLimit):
        self.__fileName = fileName
        self.__numCount = numCount
        self.__spaceLimit = spaceLimit
        self.__fileSize = numCount * 4
        self.__divisor = self.__fileSize // (self.__spaceLimit * 1000000) + 1
        self.__parts = []
        self.__sortedParts = []
        self.__generate(self.__fileName)

    def sort(self):
        # Divide the big file into lil files

        self.__divide()

        # Sort all the lil files that are part of the big file

        for part in self.__parts:
            self.__partSort(part)
        
        # Merge all the sorted lil files 

        sortedFile = functools.reduce(self.__mergeFiles, self.__sortedParts)
        print(f'The name of your huge sorted file is {sortedFile}')

        with open(sortedFile, 'rb') as file:
            count = 0
            while True:
                try:
                    num = pickle.load(file)
                except EOFError:
                    break
                else:
                    count += 1
            print(count)

    ### Private methods ###

    def __generate(self, fileName):
        with open(fileName, 'wb') as file:
            for num in random.sample(range(0, 2 ** 32), self.__numCount):
                pickle.dump(num, file)

    def __divide(self):
        start = 0
        end = self.__numCount // self.__divisor
        i = 1
        with open(self.__fileName, 'rb') as file:
            while end <= (self.__numCount + self.__numCount // self.__divisor):
                partName = self.__fileName.split('.')[0] + f'Part{i}.' + self.__fileName.split('.')[1]
                with open(partName, 'wb') as part:
                            for _ in range(start, end):
                                try:
                                    num = pickle.load(file)
                                except EOFError:
                                    break
                                else:
                                    pickle.dump(num, part)
                self.__parts.append(partName)
                start = end
                end += self.__numCount // self.__divisor
                print(f'start {start}   end {end}')
                i += 1
        print(self.__parts)

    def __partSort(self, part):
        # Load the file as a list
        nums = []
        with open(part, 'rb') as file:
            while True:
                try:
                    num = pickle.load(file)
                except EOFError:
                    break
                else:
                    nums.append(num)
        # Sort the list
        nums.sort()

        # Write the contents of the list in a new file
        newName = 'sorted_' + part
        with open(newName, 'wb') as file2:
            for num in nums:
                pickle.dump(num, file2)

        # Save the name of the new file
        self.__sortedParts.append(newName)
    
    def __mergeFiles(self, fileName1, fileName2):
        sortedFileName = fileName1.split('.')[0][-1] + fileName2.split('.')[0][-1] + '.' + fileName2.split('.')[1]
        ind1 = ind2 = 0
        file1 = open(fileName1, 'rb')
        file2 = open(fileName2, 'rb')

        with open(sortedFileName, 'wb') as file:
            while True:
                try:
                    file1.seek(ind1)
                    file2.seek(ind2)
                    num1 = pickle.load(file1)
                #    print(f'num1 {num1}')
                    num2 = pickle.load(file2)
                #    print(f'num2 {num2}')
                except EOFError:
                    break
                else:
                    if num1 <= num2:
                        pickle.dump(num1, file)
                        ind1 = file1.tell()
                    else:
                        pickle.dump(num2, file)
                        ind2 = file2.tell()

            while True:
                try:
                    file1.seek(ind1)
                    num = pickle.load(file1)
                except EOFError:
                    break
                else:
                    pickle.dump(num, file)
                    ind1 = file1.tell()
            
            while True:
                try:
                    file2.seek(ind2)
                    num = pickle.load(file2)
                except EOFError:
                    break
                else:
                    pickle.dump(num, file)
                    ind2 = file2.tell()

        return sortedFileName
    

if __name__ == '__main__':
    bigFile = BigFile('big.txt', 4000000000, 200)
    bigFile.sort()
