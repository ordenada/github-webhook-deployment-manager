#!/bin/bash

rm -r code.zip

git archive --format=zip --output=code.zip master

echo "Packaged"
