import random
from .models import Member
 
listofcompanion_inv_code = ['123456','001515','820061']


def companion_inv_code_exists(companion_inv_code):
    member = Member.objects.filter(companion_invitation_code=companion_inv_code)
    # return True if companion_inv_code in listofcompanion_inv_code else False
    return True if member is None else False
    

def generate_companion_inv_code():
    random_id = '-'.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    return random_id


def findNewcompanion_inv_code():
    while True:
        companion_inv_code = generate_companion_inv_code()
        if companion_inv_code_exists(companion_inv_code):  # Your function to check if it already exist
            print(companion_inv_code,'is already exists')
            continue
        return companion_inv_code


# print(findNewcompanion_inv_code(member))