#! /usr/bin/bash

for f in test_is_greater_than*; do
    suffix="${f#test_is_greater_than}"
    mv -- "$f" "test_is_less_than$suffix"
done


