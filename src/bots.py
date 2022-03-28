import random


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
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working"]
    if action in bad_things:
        return "YESS! Time for {}".format(action)
    elif action in good_things:
        return "What? {} sucks. Not doing that.".format(action)
    return "I don't care!"


def __action__():
    _input = input("Do you want to input your own action? (Yes/No): ")
    if _input == "Yes":
        _input = input("Write an action like for example 'work' for bots the to discuss: ")
        return _input
    return random.choice(["work", "play", "eat", "cry", "sleep", "fight"])


"""
print("\nMe: Do you guys want to {}? \n".format(action))
print("Alice: {}".format(alice(action)))
print("Bob: {}".format(bob(action)))
print("Dora: {}".format(dora(action)[0]))
print("Chuck: {}".format(chuck(action)))
"""
