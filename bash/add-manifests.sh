projects="\
cfgs \
dek \
doks \
editor \
impall \
myers \
nc \
safer \
simp \
sproc \
tdir \
versy \
wolk \
"

# scripta \
# backer \
# hardback \
# gitz \

for project in $projects; do
    cd /code/$project
    # ppy
    head -30 CHANGEL* | pbcopy
    git go new
    read -p "Hit enter: "
done
