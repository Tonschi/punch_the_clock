import time
count = 0
def timer():
  while True:
    time.sleep(60)
    count += 1
    print("This program has now been running for " + str(count) + " minutes")

timer() # Carry this function out in the background
print("Hello! Welcome to the program timer!")
name = raw_input("What is your name?")
print("Nice to meet you, " + name + "!")
