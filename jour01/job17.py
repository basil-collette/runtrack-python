print("JOB 17 ###################################################################################################################")

for x in range(1, 100+1):
    result = 'Fizz' if (x % 3 == 0) else ''
    result += 'Buzz' if (x % 5 == 0) else ''
    result = x if result == '' else result
    print(result)
