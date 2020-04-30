# por
Pi Open Retic - A web based way to control your sprinklers or reticulation.

This project I started as a way to learn Python and Django using a PI Raspberry. By connecting to the GPIO you can add run cycles and stations and there is a "ReticEngine" run by cron which will pick up when to water. It even checks the local BOM stations to see if has been raining and will turn off once a configurable threshold is reached.

# What you will need
1. Raspberry PI - I have used a Zero W for mine.
2. Python 3.6+, Django 2+, Mysql/MariaDB - or SQLite (not tested)
3. 5V Relay switches - 1 for each sprinkler and an optional "master"
4. 24v AC power supply if you do not already have one (your old system should already have this)

# TODO
1. A screen for the addition of weather stations - it's rather hard coded at the moment.
2. A screen to Add Stations - this is done manually but you can configure the GPIO assigments later.


