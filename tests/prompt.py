#! /usr/bin/env python


def confirm(*, prompt: str = 'Confirm?', default_answer: bool = True):
    _prompt = f'{prompt} [{"y" if default_answer else "n"}]{"n" if default_answer else "y"}: '

    while True:
        answer = input(_prompt).strip().lower()

        if not answer:
            return default_answer

        if answer in ['y', 'n']:
            return answer == 'y'

        print('Please enter y or n')

print(confirm(default_answer=False))
