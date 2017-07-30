#!/bin/bash

if [ -z "$MOLECULE_SCENARIO" ]
then
    molecule create
    molecule destroy
else
    molecule --debug create --scenario-name=$MOLECULE_SCENARIO
    molecule destroy --scenario-name=$MOLECULE_SCENARIO
fi
