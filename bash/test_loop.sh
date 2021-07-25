i=0
while true; do
    FILE=log-$i.txt

    if [ ! -f $FILE ]; then
        touch $FILE
        break
    fi
    ((i++))
done

echo $FILE
