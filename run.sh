current=`pwd`
apifolder=$current"/api/NER"
corefolder=$current"/core"
echo ${PYTHONPATH}
export PYTHONPATH=${PYTHONPATH}:$apifolder
export PYTHONPATH=${PYTHONPATH}:$corefolder
python webapiner.py