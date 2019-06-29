if [ "$1" != "" ]; then
    echo YES
else
    echo NO $1
fi


if [ "$1" == git ]; then
    echo AHA
fi

if [ "$1" == git ]; then
    return -1
fi

echo EHE
