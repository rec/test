from inspect import getframeinfo, stack

def debuginfo(message):
    caller = getframeinfo(stack()[1][0])
    print("%s:%d - %s" % (caller.filename, caller.lineno, message)) # python3 syntax print

def grr(arg):
    debuginfo(arg)      # <-- stack()[1][0] for this line

grr("aargh")            # <-- stack()[2][0] for this line
