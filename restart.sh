#!/bin/bash

# Kill existing Gunicorn processes
pkill gunicorn

# Start Gunicorn with new changes
gunicorn FutureStar_Project.wsgi:application --bind 0.0.0.0:8000