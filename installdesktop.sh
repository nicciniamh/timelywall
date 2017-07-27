#!/bin/bash
loc=user
act=install
[ "$XDG_SESSION_DESKTOP" == "" ] && act=create
[ $EUID -eq 0 ] && loc=system
cat << EOF
Greetings!
This script will install a desktop entry for Timely Wallpaper. This is not 
a script to install the program. It will run properly from any path so long as 
the initial dirctory structure is maintained.

EOF
if [ "$XDG_SESSION_DESKTOP" == "" ]; then
    cat <<EOF >&2
Cannot determine desktop session type.
"$(pwd)/timelywall.desktop" will be created,
but you will need to install it manually. 

EOF
else
cat << EOF
Installing to the ${loc} location defined by your desktop environment (${XDG_SESSION_DESKTOP}). 

EOF
fi
read -p "Press Enter to continue or ^C to abort: " fooey

dir=$(dirname $0)
[ "$0" != "$dir" ]  && cd $dir
if [ ! -f timelywall.desktop.skel ] ; then
    echo "Cannot find timelywall.desktop.skel">&2
    echo "Please run this script where timelywall is stored.">&2
fi
cat timelywall.desktop.skel | sed 's|@PATH|'$(pwd)'|g' >timelywall.desktop
if [ "$XDG_SESSION_DESKTOP" != "" ] ; then
    xdg-desktop-menu install --novendor timelywall.desktop >/dev/null 2>&1
    rc=$?
    case $rc in
        0 ) res="Entry installed OK";;
        1 ) res="xdg syntax error" ;;
        2 ) res="A required file cannot be found";;
        3 ) res="A required tool cannot be found";;
        4 ) res="The action failed";;
        5 ) res="Permission deined";;
        * ) res="unknown error";;
    esac
    [ $rc -eq 0 ] && { echo $res>&2; exit $rc;}
    echo "An error occurred (rc=$(rc): ${res}">&2
    exit $rc
fi
cat << EOF
The file "$(pwd)/timelywall.desktop" has been created. 
Please copy to the "applications" directory for your desktop manager.
(example: ~/.local/share/applications, /usr/share/applications, etc.)

EOF
exit 0