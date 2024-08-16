try:
    import requests, random, string, time, os, keyboard
    from colorama import Fore, Style
    from bs4 import BeautifulSoup

except ImportError as error:
    input(f"Error: {error}. Make Sure All Moduels From 'modules.txt' Is Installed.\nTo Close This Windows Press The Enter Key.")
    exit()

def generator():

    redC = Fore.LIGHTRED_EX
    greenC = Fore.LIGHTGREEN_EX
    reset = Style.RESET_ALL

    digits = string.digits
    letters = string.ascii_letters
    special_characters = string.punctuation

    character_selection = digits + letters + special_characters
    
    try:
        while True:

            amount = int(input("Amount Of Usernames To Generate: "))
            if amount <= 0:
                print(redC, "The Amount Of Usernames Needs To Be Greater Than 0.", reset)
                return

            lenght = int(input("Character Lenght For Username: "))
            if lenght <= 0:
                print(redC, "The Character Amounts Needs To Be Greater Than 0.", reset)
                return
        
            with open("usernames_generated.txt", "w") as file:

                for char in range(amount):
                    generated_username = ""
                    
                    while len(generated_username) < lenght:
                        generated_username += random.choice(character_selection)
                        
                    file.write(generated_username + "\n")

            print(greenC + f"{amount} Usernames Have Now Been Created. Stored In 'usernames_generated.txt'", reset)
            time.sleep(3)
            return
    
    except ValueError:
        print(redC, "The Amount Needs To Be A Whole Number.", reset)

def checker():

    redC = Fore.LIGHTRED_EX
    yellowC = Fore.LIGHTYELLOW_EX
    greenC = Fore.LIGHTGREEN_EX
    reset = Style.RESET_ALL

    available_usernames = 0
    already_used = 0
    suspended = 0
    errors = 0

    total = 0
    
    with open("usernames_generated.txt", "r") as file:
        
        all_usernames = file.readlines()

        for username in all_usernames:

            if keyboard.is_pressed("enter"):
                break

            total += 1
            username = username.strip()
            response = requests.get(f"https://www.youtube.com/@{username}")

            if response.status_code == 200:
                already_used += 1
                print(redC, f"Already Used - " + 5*" " + response.url, reset)
            
            elif response.status_code == 404:
                available_usernames += 1
                print(greenC, f"Available - " + 5*" " + response.url, reset)

                with open("available_users.txt", "a") as file:
                    file.write("\n")

                    file.write(username)
            
            elif response.status_code == 403:
                suspended += 1
                print(redC, f"Suspended / Closed - " + 5*" " + response.url, reset)
            
            else:
                errors += 1
                print(yellowC, f"Error Code: {response.status_code} - " + 5*" " + response.url, reset)
    
    print(f"Out Of {total} Usernames:")
    print(greenC + f"- Available Usernames [{available_usernames}]\n", reset, redC + f"- Already Used [{already_used}]\n", reset)
    print(redC + f"- Suspended [{suspended}]\n", reset, yellowC + f"- Unsupported Errors [{errors}]", reset)
    file.close()

    stop = input("Press Enter To Go Back To Menu: ")
    if stop == "":
        time.sleep(2)
        return

def menu():

    yellowC = Fore.LIGHTYELLOW_EX
    greenC = Fore.LIGHTGREEN_EX
    reset = Style.RESET_ALL

    os.system("cls")

    print(yellowC + "[1] - Generate Usernames\n[2] - Check Availability Of Generated Usernames\n[3] - Clear .txt File Of Generated Usernames.\n[4] - Close Application", reset)
    user = input("Pick One Of The Actions Above: ")

    if user == "1":
        os.system("cls")
        generator()
    
    elif user == "2":
        print("To Stop The Checker, Press Enter.")
        time.sleep(2.5)
        os.system("cls")
        checker()

    elif user == "3":
        open("usernames_generated.txt", "w").close()
        print(greenC + "File Is Now Cleared.", reset)
        time.sleep(1)

    elif user == "4":
        time.sleep(0.5)
        quit()

while True:
    menu()
