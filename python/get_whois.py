#!/usr/bin/env python

import os, sys, subprocess


def get_names(filename='domain-names.txt'):
    with open(filename) as fp:
        for line in fp:
            line = line.strip()
            if line:
                yield line


def call(*args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, err = process.communicate()
    exit_code = process.wait()
    return output, err, exit_code


def get_whois(name):
    output, err, exit_code = call('/usr/bin/whois', name)
    if exit_code:
        print('FAILED to read', name, exit_code, err, file=sys.stderr)
    return output


def get_files(directory, names):
    os.makedirs(directory, exist_ok=True)
    for name in names:
        filename = os.path.join(directory, name)
        with open(filename, 'wb') as fp:
            whois = get_whois(name)
            if whois:
                fp.write(whois)
                print('written', name)


if __name__ == '__main__':
    get_files('names', get_names())
