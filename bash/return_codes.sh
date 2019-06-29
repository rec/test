function succeed() {
    echo "succeed"
    return 0
}

function fail() {
    echo "fail"
    return 1
}

if [ succeed ] ; then
    echo "yes"
else
    echo "no"
fi

if [ -z fail ] ; then
    echo "yes"
else
    echo "no"
fi
