SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

mkdir ~/.emily
cp -n -R $SCRIPT_DIR/scripts ~/.emily
cp -n -R $SCRIPT_DIR/icons ~/.emily

clear

python $SCRIPT_DIR/src/main.py