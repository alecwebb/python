#Exercise in which various goals need to be met using python version 3
#Alec Webb

#import statistics
from collections import Counter

#check if the argument n is prime (is only divisible by 1 and itself). The smallest prime is 2.
def is_prime(n):
	#prime numbers are greater than 1, and not divisible by anything but themselves
	#cycle through 2 to n-1 to try all possibilities.
	if n > 1:
		for i in range(2,n):
			if(n % i) == 0:
				return False
		else:
			return True
			
#given a non-negative integer n, and optionally a dictionary results (whose keys are ints k and whose values are the result of fast_fib(k)), 
#calculate the nth fibonnaci number while memoizing the answers (don't use the pathologically slow recursive approach). 
def fast_fib(n, results={}):
	#base conditions
	if n == 0: return 0
	if n == 1: return 1
	
	#recursion through result set
	if not n in results:
		results[n] = fast_fib(n-1) + fast_fib(n-2)
	return results[n]

#given a list of values, create a new list with the same values in reversed order. Do not modify the original list.
def reversed(xs):
	#use extended slice to reverse the list
	return xs[::-1]

#return a list of all values that show up in xs at least once. The answer must not include any duplicates, 
#and must report the occurring values in the same order as their first occurrence.	
def nub(xs):
	#self explanatory, creates empty list (nub), traverse given list
	#place items from xs that dont exist yet in nub, into nub
	nub = []
	for item in xs:
		if item not in nub:
			nub.append(item)

	return nub

#given a two-argument function and two lists of arguments to supply, create a list of the results of applying 
#the function to each same-indexed pair of arguments from the two lists.
def zip_with(f, xs, ys):
	#in the event either list has no entries
	if len(xs) < 1 or len(ys) < 1:
		solution = []
	#in the event list1 is larger than list2
	if len(xs) >= len(ys):
		solution = list(map(f,xs[0:len(ys):1],ys))
	#in the event list2 is larger than list1
	if len(xs) <=len(ys):
		solution = list(map(f,xs,ys[0:len(xs):1]))

	return solution
	
#given a number n, we generate successive integer values in a sequence, which must end with a 1.
#if n is 1, the sequence ends.
#if n is even, the next number is n/2.
#if n is odd, the next number is n*3+1.
def collatz(n):
	colist = []
	
	while n != 1:
		colist.append(n)
		#iseven
		if n%2 == 0:
			n = int(n/2)
		#isodd
		else:
			n = 3*n+1
	#all roads lead to 1
	colist.append(1)

	return colist

def max_or_mode(check, switch):
	#this function finds the maximum value of identical items when switch is 0
	#or the mode when switch is 1
	if switch == 0:
		counter = Counter(check)
		cmax = max(counter.values())
		return cmax 
	
	#use counter, and list comprehension for multimodal lists
	#the counter counts the number of occurances of each number, creating in an i,j pair
	#the cmax variable finds the maximum occurance of one or more list entries
	#the mode uses a list comprehension to cycle through the i,j pairs to match
	#and places the number(i) with the (j) value equivalent to the cmax
	if switch == 1:
		counter = Counter(check)
		cmax = max(counter.values())
		mode = [i for i, j in counter.items() if j == cmax]
		return mode

		
#Given the name of a text file that contains one or more lines, each with a single integer on that line, 
#calculate these three properties and return in a triplet: (mean, median, mode)
def file_report(filename):
	with open(filename) as f:
		numbers = [num.strip('\n') for num in f.readlines()]

	#convert from str to int
	numbers = [int(n) for n in numbers]

	#use stat package if python version 3.4 or greater
	#mean = statistics.mean(numbers)
	#median = statistics.median(numbers)
	#otherwise must calculate ourselves
	
	mean = sum(numbers)/len(numbers)
	mode = max_or_mode(numbers, 1)
	
	#to get the median, sort the list
	numbers.sort()
	#find the middle position using the floor division operator
	middle = len(numbers)//2
	#check if the list is even or odd, if odd take the middle number
	if len(numbers) % 2:
		median = numbers[middle]
	#if the list is even average the two numbers in the middle
	else:
		median = (numbers[middle] + numbers[middle-1]) / 2

	return (mean, median, mode)

	
#Given a 9x9 2d list, check if it represents a valid, solved sudoku. We aren't solving a sudoku, we're only checking someone's completed attempt.	
def check_sudoku(grid):
	#to check the rows, pull and separate values, use the counter to check if the
	#each number has one occurance, this would indicate no duplication of values 0-9
	for row in grid:
		check = row[:]
		if max_or_mode(check,0) != 1:
			return False

	#to check for the columns, do the same thing but traverse the columns and place in 
	#the list
	for i in range(9):
		check = []
		for j in range(9):
			check.append(grid[j][i])
		if max_or_mode(check,0) != 1:
			return False

	#to check the 3x3 grids, the offset allows traversel through the component grids
	#apply the same count check.
	for i in range(3):
		for j in range(3):
			check = []
			roffset = i*3
			coffset = j*3
			for x in range(3):
				for y in range(3):
					check.append(grid[x + roffset][y + coffset])
			if max_or_mode(check,0) != 1:
				return False

	return True

#DEBUG
#grid  = [[1,2,3, 4,5,6, 7,8,9],
#		 [4,5,6, 7,8,9, 1,2,3],
#		 [7,8,9, 1,2,3, 4,5,6],

#		 [2,3,4, 5,6,7, 8,9,1],
#		 [5,6,7, 8,9,1, 2,3,4],
#		 [8,9,1, 2,3,4, 5,6,7],

#		 [3,4,5, 6,7,8, 9,1,2],
#		 [6,7,8, 9,1,2, 3,4,5],
#		 [9,1,2, 3,4,5, 6,7,8],
#		]
