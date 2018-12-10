from datetime import datetime
from django.http import HttpRequest
from accounts.models import User, Profile


def generate_years_for_bday():
    """

    :return: list
    """
    # get current year
    curr_year = datetime.now().year
    # cast the object to integer (for the purpose of calculations)
    curr_year = int(curr_year)
    # what year was it 70 years ago
    _70_years_ago = curr_year - 70
    list_of_years = []
    # generate the list of years over the past 70 years
    for i in range(0, 70):
        i_years_ago = _70_years_ago + i
        list_of_years.append(i_years_ago)
    return list_of_years


def is_phone_number(phone_number):
    """

    :param phone_number: the phone number you want to validate
    :return: boolean
    """
    # are there ten digits
    if len(phone_number) != 10:
        return False
    # are all the charaters in the phone number actually digits
    for digit in phone_number:
        if not digit.isdecimal:
            return False
    # is the first digit 0
    if phone_number[0] != '0':
        return False
    return True


def get_user(request):
    if isinstance(request, HttpRequest) and isinstance(request.user, User):
        return request.user
    return None


def get_user_profile(request):
    if isinstance(request, HttpRequest) and isinstance(request.user.profile, Profile):
        return request.user.profile
    return None
