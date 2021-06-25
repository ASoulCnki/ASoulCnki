echo $(date "+%Y%m%d-%H%M%S") >> stop.text
ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9