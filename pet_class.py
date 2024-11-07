# Jonathan Lee
# Purpose: Pet class for the Upgrade Pet Chooser Program.

class Pet:

    __name = ""
    __age = 1
    __owner = ""
    __animal_type = ""
    __tableID = 0

    def __init__(self,
                 pet_name="",
                 pet_age=0,
                 owner_id=0,
                 animal_type_id=0,
                 sql_ID = 0):
        self.SetPetName(pet_name)
        self.SetPetAge(pet_age)
        self.SetOwnerName(owner_id)
        self.SetAnimalType(animal_type_id)
        self.__tableID = sql_ID

    # Get and Set Pet Name
    def GetPetName(self) -> str:
        return self.__name

    def SetPetName(self, pet_name: str) -> None:
        try:
            self.__name = pet_name
        except ValueError as e:
            print("Invalid input.")

    # Get and Set Pet Age
    def GetPetAge(self) -> int:
        return self.__age

    def SetPetAge(self, pet_age: int) -> None:
        try:
            self.__age = pet_age
        except ValueError as e:
            print("Invalid input. Age must be a positive integer.")

    # Get and Set Owner Name
    def GetOwnerName(self) -> str:
        return self.__owner

    def SetOwnerName(self, owner_name: str) -> None:
        try:
            self.__owner = owner_name
        except ValueError as e:
            print("Invalid input.")

    # Get and Set for Animal Type
    def GetAnimalType(self) -> str:
        return self.__animal_type

    def SetAnimalType(self, anm_type: str) -> None:
        try:
            self.__animal_type = anm_type
        except ValueError as e:
            print("Invalid input.")
    # Get Pet ID
    def GetID(self) -> str:
        return self.__tableID