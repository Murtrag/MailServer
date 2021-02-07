import re
import random
import string
import hashlib

"""
ALPHABET is a global variable, that keeps all uppercase letter, all lowercase
letters and digits.
"""
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_salt():
    """
    Generates a 16-character random salt.
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        salt += random.choice(ALPHABET)
    return salt


def password_hash(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.
    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.
    """

    # generate salt if not provided
    salt = generate_salt() if salt is None else salt

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += "a" * (16 - len(salt))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate hash
    t_sha = hashlib.sha256()

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    t_sha.update(salt.encode("utf-8") + password.encode("utf-8"))

    # return salt & hash joined
    return salt + t_sha.hexdigest()


def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)
    """

    # extract salt
    salt = hashed[:16]

    # extract hash to compare with
    hash_to_check = hashed[16:]

    # hash password with extracted salt
    new_hash = password_hash(pass_to_check, salt)

    # compare hashes. If equal, return True
    return new_hash[16:] == hash_to_check


def check_pass_len(pass_to_check):
    """check if password has more than 8 chars """
    return len(pass_to_check) >= 8


def slice_args(args):
    # puendlts
    pairs = {}
    for pair_item in args:
        if "-" in pair_item:
            f_pair_item = pair_item if "--" not in pair_item else pair_item[1:3]
            try:
                pairs[f_pair_item] = args[
                    args.index(pair_item) + 1 : args.index(pair_item) + 2
                ][0]
                if re.match("-{1,2}[a-z]+", pairs[f_pair_item]):
                    pairs[f_pair_item] = None
            except IndexError:
                pairs[f_pair_item] = None
    if set([arg.strip("-") for arg in pairs]) - set("puendlts"):
        raise KeyError("Podany parametr jest zabroniony")
    return pairs
