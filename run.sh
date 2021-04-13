python3 main.py &
BOTPID=$!
while true
do
OUTPUT=$(git pull | grep "Already up to date.")
if [ -z "$OUTPUT" ]
then
kill $BOTPID
pip3 install pillow
pip3 install discord
pip3 install requests
pip3 install emojis
python3 main.py &
BOTPID=$!
echo "Bot rebooted"
fi
sleep 5
done
