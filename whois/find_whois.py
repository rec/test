import json, sys, whois

names = [i.strip() for i in open('domain_names').readlines()]
domain, errors = {}, []

for name in names:
    try:
        domain[name] = whois.whois(name)
    except:
        errors.append(name)
        raise

if errors:
    print('ERRORS in names', *errors)

json.dump(domain, sys.stdout, indent=2)
