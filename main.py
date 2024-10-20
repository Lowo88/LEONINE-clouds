def choose_pet():
    print("Welcome to the Virtual Pet App!")
    print("Please choose your pet:")
    print("1. Zebra")
    print("2. Lion")
    
    choice = input("Enter the number of your choice (1 or 2): ")
    
    if choice == '1':
        pet_name = input("You chose a Zebra! What will you name it? ")
        pet = "Zebra"
    elif choice == '2':
        pet_name = input("You chose a Lion! What will you name it? ")
        pet = "Lion"
    else:
        print("Invalid choice. Please restart the app.")
        return
    
    print(f"You have chosen a {pet} named {pet_name}!")

if __name__ == "__main__":
    choose_pet()