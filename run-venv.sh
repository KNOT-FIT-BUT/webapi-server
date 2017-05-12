current=`pwd`
apifolder=$current"/api/NER"
corefolder=$current"/core"
echo ${PYTHONPATH}
export PYTHONPATH=${PYTHONPATH}:$apifolder
export PYTHONPATH=${PYTHONPATH}:$corefolder
../py/bin/python webapiner.py
