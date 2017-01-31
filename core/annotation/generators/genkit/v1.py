'''
Created on 11. 5. 2014

@author: casey
'''
import os, sys
from collections import OrderedDict
from ner import dates


features_code = {}

def generate(proc_res, kb, include_all_senses = False):

    '''
    Bake output with KB config and KB data. Pair KB column names from KB config and row data from KB.
    @proc_res - raw data from processing tools
    @kb - instance of KB class
    '''
    global features_code
    
    if not features_code:
        with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),"api","NER","geoData.all"),"r") as f:
            data = f.read()
        for row in data.split("\n"):
            items = row.split("\t")
            if len(items) >=2:
                features_code[items[0]] = items[1]
                
    result = groupResultItems(proc_res,include_all_senses)
    splitter = kb.config["value_splitter"] if kb.config["value_splitter"] is not None else ""
    splitter = splitter.encode("utf-8")
    result_kb = []
    for key,data in result.items():
        if str(key) in ["dates", "intervals"]:
            result_kb.append({key:data})
        else:
            
            if(include_all_senses):
                senses = data[0][-1]
                [item.pop() for item in data]
                kb_row = [bakeKBrow(sense,kb, splitter) for sense in senses]
                kb_row = kb_row if len(kb_row) > 1 else kb_row[0]
            else:
                kb_row = bakeKBrow(key, kb, splitter)
                
    
            result_kb.append({
                              "kb_row":kb_row,
                              "items":data
                              })
    return result_kb
    
def bakeKBrow(key, kb, splitter):
    global features_code
    kb_data = OrderedDict()
    item_type = kb.get_field(key, 0)[0]
    
    if item_type in kb.header:
        columns = kb.header[item_type]
    else:
        columns = kb.header["generic"]
    
    for a in range(len(columns)):
            colname = columns[a];
            field_data = kb.get_field(key,a)
            if colname.startswith('*'):
                field_data = field_data.split(splitter) if len(field_data) > 0 else ""
                colname = colname[1:]
            elif colname == "feature code":
                field_data = [field_data, features_code[field_data]] if field_data in features_code else field_data
            kb_data[colname] = field_data
            
                
    return kb_data 


def groupResultItems(result, include_all_senses=False):
        '''
        Group the same entities items into one container - saving bandwith data.
        '''
        results_group = {}
        for item in result:
            if isinstance(item, dates.Date):
                if item.class_type == item.Type.DATE:
                    item_id = "dates"
                    item_data= [item.s_offset, item.end_offset, item.source, str(item.iso8601)]
                elif item.class_type == item.Type.INTERVAL:
                    item_id = "intervals"
                    item_data= [item.s_offset, item.end_offset, item.source, str(item.date_from), str(item.date_to) ]
                else:
                    continue
            else:
                if item.preferred_sense:
                    item_id = item.preferred_sense
                    item_data = [item.begin, item.end, item.source, item.is_coreference()]
                    if include_all_senses:
                        senses = list(item.senses)
                        if item.preferred_sense in senses:
                            senses.remove(item.preferred_sense)
                            senses.insert(0,item.preferred_sense)
                        else:
                            senses.insert(0,item.preferred_sense)
                        item_data.append(senses)
                else:
                    continue
                
            if item_id not in results_group.keys():
                results_group[item_id] = [item_data]
            else:
                data = results_group.get(item_id)
                data.append(item_data)
                results_group[item_id] = data
                
        return results_group