#!/bin/bash

# Blame tilde expansion

alias foo=alias
foo=global

outer()
{
    local foo=outer
    inner
    echo -n outer\ ; declare -p foo
}

inner()
{
    #local foo=inner
    alias foo=(lol wut)
    local foo=inner
    echo -n inner\ ; declare -p foo
}

outer
echo -n global\ ; declare -p foo
alias foo
