'''
Created on 13. 5. 2014

@author: casey
'''

import re

def loadHeaderFromFile(filename):
    column_ext_def = {"g":{"type":"image"},
                      "u":{"type":"url"}
                      }

    col_prefix = {
        "person":"p",
        "artist":"a",
        "location":"l",
        "artwork":"w",
        "museum":"c",
        "event":"e",
        "visual_art_form":"f",
        "visual_art_medium":"d",
        "art_period_movement":"m",
        "visual_art_genre":"g",
        "nationality":"n",
        "mythology":"y",
        "family":"i",
        "group":"r"
    }
    regex = re.compile('(?u)^(?:<([^:>]+)(?:[:]([^>]+))?>)?(?:\{((?:\w|[ ])*)(?:\[([^\]]+)\])?\})?((?:\w|[ ])+)$')
    columns = {}
    groups = {}
    with open(filename,'r') as f:
        raw_colums = f.read().strip()

    for row in raw_colums.split("\n"):
        column = []
        dataPlus = {}
        row_split = row.split("\t")
        row_head = row_split.pop(0)
        item_type, item_subtype, item_flags, item_prefix, item_name = regex.search(row_head).groups() 
        print item_type, item_subtype, item_flags, item_prefix, item_name
        row_prefix = col_prefix[item_type]
        groups[row_prefix]= {"name": item_type.lower()}
        column.append(item_name.lower())
        for col_name in row_split:
            item_type, item_subtype, item_flags, item_prefix, item_name = regex.search(col_name).groups() 
            if item_flags is not None:
                for k in item_flags:
                    if k in column_ext_def:
                        dataPlus[item_name.lower()] = {"type":column_ext_def[k]["type"],
                                                       "data":item_prefix if item_prefix else ""
                                                       }
            if item_flags is not None and "m" in item_flags:
                item_name = "*" + item_name
            column.append(item_name.lower())
        groups[row_prefix]["dataPlus"] = dataPlus
        columns[row_prefix] = column
    return columns, groups


def loadHeaderFromFile2(filename):
    column_ext_def = {"g":{"type":"image"},
                      "u":{"type":"url"}
                      }
        
    columns = {}
    groups = {}
    with open(filename,'r') as f:
        raw_colums = f.read().strip()
        
    for row in raw_colums.split("\n"):
        column = []
        dataPlus = {}
        row_split = row.split("\t")
        row_head = row_split.pop(0)
        row_prefix, row_head, row_id = row_head.split(":")
        groups[row_prefix]= {"name": row_head.lower()}
        column.append(row_id.lower())
        for col_name in row_split:
            prefix = ""
            url = ""
            if ':' in col_name:
                col_split = col_name.split(":")
                prefix = ":".join(col_split[:-1])
                if "[" in prefix:
                    prefix,url = prefix.split("[")
                col_name = col_split[-1]
                for k in prefix:
                    if k in column_ext_def:
                        dataPlus[col_name.lower()] = {"type":column_ext_def[k]["type"],
                                                                     "data":url[:-1]
                                                                     }
                if "m" in prefix:
                    col_name = "*" + col_name
            column.append(col_name.lower())
        groups[row_prefix]["dataPlus"] = dataPlus
        columns[row_prefix] = column  
    return columns, groups
    
