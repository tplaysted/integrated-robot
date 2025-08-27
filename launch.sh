#!/bin/bash

arg0=$(basename "$0" .sh)
blnk=$(echo "$arg0" | sed 's/./ /g')

usage_info()
{
    echo "Usage: $arg0 interface [{-v|--venv} interpreter]"
}

usage()
{
    exec 1>&2   # Send standard output to standard error
    usage_info
    exit 1
}

error()
{
    echo "$arg0: $*" >&2
    exit 1
}

help()
{
    usage_info
    echo
    echo "  interface                          -- Start the services to listen on this IP (required)"
    echo "  {-v|--venv} interpreter            -- Set virtual environment path (default: .venv)"
    exit 0
}

args()
{
    [ $# = 0 ] && error "No interface specified"
    export INTERFACE="$1"
    shift

    while test $# -gt 0
    do
        case "$1" in
        (-v|--venv)
            shift
            [ $# = 0 ] && error "No environment path specified"
            export VENV="$1"
            shift;;
        (-h|--help)
            help;;
#       (-V|--version)
#           version_info;;
        (*) usage;;
        esac
    done
}

export VENV='.venv'
export LG_WD=/tmp

args "$@"

MOTOR=("$VENV/bin/python" "motor.py" "-i" "$INTERFACE")
SERVO=("$VENV/bin/python" "servo.py" "-i" "$INTERFACE")

trap "kill 0" exit

"${MOTOR[@]}" &
"${SERVO[@]}" &

wait
