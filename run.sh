python3 main.py &
BOTPID=$!
while true
do
#OUTPUT=$(git pull | grep "Already up to date.")
OUTPUT="owo"
if [ -z "$OUTPUT" ]
then
kill $BOTPID
cd cone
make
cd ..
python3 main.py &
BOTPID=$!
echo "Bot rebooted"
fi
sleep 5
done
