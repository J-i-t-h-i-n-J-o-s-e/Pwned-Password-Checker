import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res =requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    firt5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(firt5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times....you should change your password!')
        else:
            print(f'{password} was not found. You have a strong password, Carry on...!')
    return 'done'



if __name__ == '__main__':
    f = open('input_your_passwords_here.txt')
    each_line = f.read().split('\n')
    del each_line[-1]
    sys.exit(main(each_line))
    # sys.exit(main(sys.argv[1:]))
