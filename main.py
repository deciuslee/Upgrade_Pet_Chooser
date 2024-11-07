# Jonathan Lee
# Purpose: Upgrade Pet Chooser

# Original Pet Chooser: Creating a Pets Class using different inputs and values
                      # 1. Start
                      # 2. Connect to your personal (pets) database
                      # 3. Read data
                      # 4. Create one (object) instance of a Pets class for each pet listed in your database.
                      #     Keep your Pets class in a separate file
                      # 5. Display a list of pet names, from the pet object instances
                      # 6. Ask the user to choose a pet
                      # 7. Once a pet is chosen, print that pet's info from the (object) instance.
# Upgrade Pet Chooser
# (a) Clone your Pet Chooser program to a new PyCharm project.
#     At every menu, allow the user to use Q or q to quit your program nicely.
# (b) Initial View: When the program begins, list all of the pets like before, and ask the user to choose a pet.
#     Once a pet is chosen, print out the same information as before.
# (c) Options: When the pet's information has been displayed, ask the user if they would like to continue or edit the pet's information.
#     Display the chosen pet’s information and ask whether user would like to [C]ontinue, [Q]uit, or [E]dit this pet?
#     Choosing to quit (by typing Q + [ENTER]), quit the program nicely.
#     Choosing to continue (by typing C + [ENTER]), display the list of pets again from the Initial View.
#     Choosing to edit (by typing E + [ENTER]), display the Edit Process below.
# (d) Edit Process: Ask the user which pet to edit (a number from the Initial View list), step through the pet's name and age to ask the user to provide an update.
#     Updating that pet's name in the database.  Display a message indicating the pet's name has been updated
#     Updating that pet's age in the database.  Display a message indicating the pet's age has been updated.
# When the updates are complete, display the list of pets again from the Initial View.

# Import pymysql.cursors
import pymysql.cursors
# Import mysql database credentials
from creds import *
# Import Pets class
from pet_class import Pet


def main_menu():
    exit_cond = False
    print("*".center(45, "*"))
    print(" Welcome to the Upgraded Pet Chooser Program ")
    print("*".center(45, "*"))
    while not exit_cond:
        try:
            i = 1
            print("Press [ENTER] to view pets list below:")
            input()
            for pet in pets_list:
                print(f"[{i}] {pet.GetPetName()}")
                i += 1
            print("[Q] Quit")

            user_input = input("Enter the desired pet number or press [Q] to quit:")
            if user_input == "q" or user_input == "Q":
                print("Thanks for using the Upgrade Pet Chooser Program. Goodbye!")
                exit_cond = True
            elif not user_input.isnumeric():
                print("Invalid number. Please choose again.")
                input("Press [ENTER] to continue.")
            elif int(user_input) <= 0 or int(user_input) > i-1:
                print(f"Please choose a number between 1 and {i-1}")
                input("Press [ENTER] to continue:")
            else:
                print_quit = printPet(pets_list[int(user_input)-1], user_input)
                # Break out of the loop
                if print_quit:
                    return

        except Exception as e:
            raise e

# Edit pet options provided to user:
def editPet(chosen_pet: Pet):
    print(f"You have chosen to edit {chosen_pet.GetPetName()}.")
    print("Press [ENTER] after each prompt if you would like to keep the current value.")
    new_name = input("New name: ")
    # [Q] to quit program.
    if new_name.upper() == "Q":
        print("Thanks for using the Upgrade Pet Chooser Program. Goodbye!")
        return True
    new_age = input("New age: ")
    if new_age.upper() == "Q":
        print("Thanks for using the Upgrade Pet Chooser Program. Goodbye!")
        return True

    if new_name == "":
        print("Name of pet not changed.")
    # Do not allow integer names
    elif new_name.isnumeric() == True:
        print("Name of pet must not be a number. Name not changed.")
    else:
        print(chosen_pet.GetID())
        name_update = f"update pets set name = '{new_name}' where id = {chosen_pet.GetID()};"
        myConnection.cursor().execute("use pets;")
        myConnection.cursor().execute(name_update)
        myConnection.commit()
        print(f"Pet's name successfully updated to {new_name}")

    if new_age == "":
        print("Age of pet not changed.")
    # Do not allow non positive integer ages
    elif new_age.isnumeric() == False:
        print("Invalid age entered. Age not updated.")
    else:
        age_update = f"update pets set age = '{new_age}' where id = {chosen_pet.GetID()};"
        myConnection.cursor().execute(age_update)
        myConnection.commit()
        print(f"Pet's age successfully updated to {new_age}")

    # Update class object by pulling updated information from sql server
    sqlSelect = f"select id, name, age from pets where id = {chosen_pet.GetID()};"
    with myConnection.cursor() as cursor:
        cursor.execute(sqlSelect)
        for row in cursor:
            chosen_pet.SetPetName(row['name'])
            chosen_pet.SetPetAge(row['age'])

    # Return false if user chooses to continue.
    return False

# Display user's choice: [C], [Q] or [E].
def printPet(chosen_pet: Pet, pet_number : int):
        print_exit = False
        print(f"You have chosen {chosen_pet.GetPetName()}, the {chosen_pet.GetAnimalType()}. "
              f"{chosen_pet.GetPetName()} is {chosen_pet.GetPetAge()} years old. "
              f"{chosen_pet.GetPetName()}'s owner is {chosen_pet.GetOwnerName()}.\n")

        while print_exit == False:
            edit_choice = input("Would you like to [C]ontinue, [Q]uit, or [E]dit the selected pet? ")
            # [Q] to quit out of program.
            if edit_choice.lower() == "q":
                print("Thank you for using Upgrade Pet Chooser. Exiting program now. Goodbye!")
                return True
            # [C] to continue.
            elif edit_choice.lower() == "c":
                print_exit = True
            # [E] to edit pet selection.
            elif edit_choice.lower() == "e":
                quitting = editPet(pets_list[int(pet_number)-1])
                # Break out of this loop and function if user previously quit in another function
                if quitting == True:
                    return True
                print_exit = True
            else:
                print("Invalid selection. Please try again.")

        input("Press [ENTER] to continue:")
        # Return false if user chooses to continue
        return False


# Establish a connection to the MySQL database.
try:
    myConnection = pymysql.connect(host=hostname,
                                   user=username,
                                   password=password,
                                   db=database,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print(f"An error has occurred.  Exiting program: {e}")
    print()
    exit()

# Execute a query.
try:
    with myConnection.cursor() as cursor:

        # Create list holding each pet object
        pets_list = []
        # Modify the SQL query
        sqlSelect = """
            SELECT pets.id, pets.name, pets.age, owners.name, types.animal_type 
            FROM pets JOIN owners ON pets.owner_id=owners.id 
            JOIN types ON pets.animal_type_id=types.id;
            """

        # Execute select
        cursor.execute(sqlSelect)
        for row in cursor:
            # Create Pet instances
            pets_list.append(Pet(row['name'], row['age'], row['owners.name'], row['animal_type'], row['id']))

        main_menu()


except Exception as e:
    print(f"An error has occurred.  Exiting Upgrade Pet Chooser Program: {e}")
    print("Thank you for using the Upgrade Pet Chooser!")
    print()

# Close database connection
finally:
    myConnection.close()
    print("Database connection closed.")