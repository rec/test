import random as r
u='̡̢̧̨̖̗̘̙̜̝̞̟̠̣̤̥̦̩̪̫̬̭̮̯̰̱̲̳̹̺̻̼͇͈͉͍͎͓͔͕͖͙͚͜͟͢ͅM̴̵̶̷̸'
o = "'̛̀́̂̃̄̅̆̇̈̉̊̋̌̍̎̏̐̑̒̓̔̽̾̿̀́͂̓̈́͆͊͋͌͐͑͒͗͛̕̚͘͝͞͠͡'"
def zalgo(txt):
        return "".join(["".join([el] + [r.choice(o+u) for _ in range(r.randint(0,6))])
        for el in txt])
