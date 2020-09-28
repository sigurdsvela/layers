#!/bin/bash

mkdir testenv
cd testenv
mkdir 1layer
mkdir 2layer
mkdir 3layer

cd 1layer
layers new .
layers new ../2layer
layers new ../3layer

mkdir folder

dd if=/dev/zero of=./folder/0D148132C4CE bs=4096 count=100k
dd if=/dev/zero of=./folder/62D542B0C8F9 bs=4096 count=100k
dd if=/dev/zero of=./folder/AF942D7EBF45 bs=4096 count=100k

layers sync
layers mv --down folder
