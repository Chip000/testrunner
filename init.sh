#!/bin/bash
# Initialize the current directory with the correct folders

create_dirs=( "results" "bin" "inst" "tmp" )

for dir in ${create_dirs[@]}; do
    if [ -e $dir ]; then
	echo ">>> Nothing";
    else
	echo ">>> mkdir $dir";
	mkdir $dir;
    fi;
done;

# EOF
