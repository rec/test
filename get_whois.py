import os, subprocess


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


def get_whois(name):
    process = subprocess.Popen(
        ['pip', 'install', requirement, '--upgrade'],
        stdout=subprocess.PIPE)
    output, err = process.communicate()
            exit_code = process.wait()



def get_files(directory, names):
    os.makedirs(directory)
    for name in names:
        filename = os.path.join(directory, name)
        with open(filename, 'w') as fp:
            fp.write(get_whois(name))
