attempts = 0

while attempts < 3:
    password = input("Enter password: ")

    if password == "python123":
        print("access granted")
        break
    else:
        attempts += 1
        print("intruder alert")

if attempts == 3:
    print("account locked. Try again later.")
