#!/bin/bash

if [ -z "$MOLECULE_SCENARIO" ]
then
    molecule test
else
    molecule test --scenario-name=$MOLECULE_SCENARIO
fi
