#!/bin/bash

cd model_zoo
gunicorn model_zoo.wsgi --log-file -