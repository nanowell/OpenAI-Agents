import re


def check_password(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]',
                             password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error
                       or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }


def main():
    password = input("Enter your password: ")
    password_check = check_password(password)
    print(password_check)
    if password_check['password_ok']:
        print('Password is strong')
    else:
        print('Password is weak')
        if password_check['length_error']:
            print('Password should be 8 characters long')
        if password_check['digit_error']:
            print('Password should contain at least 1 digit')
        if password_check['uppercase_error']:
            print('Password should contain at least 1 uppercase letter')
        if password_check['lowercase_error']:
            print('Password should contain at least 1 lowercase letter')
        if password_check['symbol_error']:
            print('Password should contain at least 1 symbol')


if __name__ == '__main__':
    main()