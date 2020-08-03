#!/bin/bash

flake8 .
ERROR_CODE=$?
if [ ${ERROR_CODE} == 0 ]; then
    # Output in green
    echo "$(tput setaf 2)Flake8 verification has passed!"
else
    # Output in red
    echo "$(tput setaf 1)Flake8 verification has failed!"
    exit ${ERROR_CODE}
fi