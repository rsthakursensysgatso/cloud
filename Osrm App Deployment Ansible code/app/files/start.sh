#!/bin/sh
osrm-extract berlin-latest.osm.pbf -p profiles/car.lua
osrm-contract berlin-latest.osrm
#nohup osrm-routed berlin-latest.osrm  &
