echo " Please Wait.."
echo " Author: CardSec "

INFILE=$1

if [ -n "$NETCAT" ] ; then
 alias NETCAT="$NETCAT"
elif which netcat &> /dev/null ; then
 alias NETCAT='netcat'
else
 echo 'You need netcat to run this!'
fi

sed -e '1ibegin' -e '1icountrycode' $INFILE > $INFILE.f
echo 'end' >> $INFILE.f

`netcat whois.cymru.com 43 < $INFILE.f > $INFILE.whois.csv`

rm $INFILE.f
echo " Done"
echo ""
echo ""
