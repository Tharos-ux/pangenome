#!/bin/bash

PYTHONPATH=""

if typeset -f __conda_activate > /dev/null; then
    return 0
fi

echo $PATH | grep '/local/miniconda3/bin' > /dev/null 2>&1
if [ $? -ne 0 ]; then
    export PATH=/local/miniconda3/bin:$PATH
fi

CUR_SHELL="$(ps -p$$ -ocmd=)"
__conda_setup="$('/usr/etc/conda' 'shell.$CUR_SHELL' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    export PATH="/usr/etc/conda:$PATH"
fi
unset __conda_setup
