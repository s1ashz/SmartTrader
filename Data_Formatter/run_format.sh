#!/usr/bin/env bash

executer=$1
dir=$2
#cd $dir

pwd

for file in $dir/*
do
  #cmd [option] "$file" >> results.out
  mkdir -p $dir/formatted
  ./$executer $file
done