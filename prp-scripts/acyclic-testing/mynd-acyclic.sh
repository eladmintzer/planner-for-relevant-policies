#! /bin/bash

/home/cjmuise/Projects/mynd/translator-fond/translate.py $1 $2
java -Xmx1g -classpath /home/cjmuise/Projects/mynd/src mynd.MyNDPlanner -aostar -ff output.sas
