import random

bad_verbs = ["fight", "bicker", "yell", "complain", "cry"]
good_verbs = ["sing", "play", "work", "play", "eat", "sleep"]


def __action__():
    verbs = [bad_verbs, good_verbs]
    bad_good = random.choice(verbs)
    a = random.choice(bad_good)
    # Will loop until a and b are not the same verb
    while True:
        bad_good = random.choice(verbs)
        b = random.choice(bad_good)
        if b != a:
            break
    # End of loop

    c = random.choice([1, 2])
    if c == 1:
        return a, None
    else:
        return a, b


def alice(a, b=None):
    return "I think {} sounds great!".format(a + "ing")


def bob(a, b=None):
    if b is None:
        return "Not sure about {}. Don't I get a choice?".format(a + "ing")
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing")


def dora(a, b=None):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    b = random.choice(alternatives)
    res = "Yea, {} is an option. Or we could do some {}.".format(a, b)
    return res, b


def chuck(a, b=None):
    action = a + "ing"
    if action in bad_verbs:
        return "YESS! Time for {}".format(action)
    elif action in good_verbs:
        return "What? {} sucks. Not doing that.".format(action)
    return "I don't care!"


"""
print("\nMe: Do you guys want to {}? \n".format(action))
print("Alice: {}".format(alice(action)))
print("Bob: {}".format(bob(action)))
print("Dora: {}".format(dora(action)[0]))
print("Chuck: {}".format(chuck(action)))
"""
