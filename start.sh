#!/bin/bash

nohup celery -A tasks worker -l info &
nohup celery -A tasks beat -l info &