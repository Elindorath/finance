#! /usr/bin/env python


def specific(greetings, to="Du", *args, **kwargs):
    print("SPECIFIC")
    print(greetings)
    print(to)
    print(args)
    print()
    print(kwargs)


def specific2(greetings, *args, to="Du", **kwargs):
    print("SPECIFIC 2")
    print(greetings)
    print(to)
    print(args)
    print()
    print(kwargs)

def general(*args, **kwargs):
    print("GENERAL")
    print(args)
    print()
    print(kwargs)


specific("Coucou", "blabla", "fouh", hello="you")
specific2("Coucou", "blabla", "fouh", hello="you")
general("Coucou", "toi", hello="you")
