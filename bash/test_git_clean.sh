#!/bin/bash

if git diff-index --quiet HEAD -- ; then
    echo YES
else
    echo no
fi
