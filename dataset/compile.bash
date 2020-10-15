#!/usr/bin/env bash

files=""

for entry in "entities"/*
do
  files="${files} ${entry}"
done

for entry in "intents"/*
do
  files="${files} ${entry}"
done

files=${files:1}

echo "${files}"

eval snips-nlu generate-dataset en $files > dataset.json