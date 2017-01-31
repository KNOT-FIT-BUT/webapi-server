'''
Created on 8. 5. 2014

@author: casey
'''
import inspect
import sys
import pkgutil

def loadClasses(mod_path, base_class, class_name_filter, skip_private_mod = True):
    result = []
    if not mod_path in sys.path:
        sys.path.append(mod_path)
    modules = pkgutil.iter_modules(path=[mod_path])
    for loader, mod_name, ispkg in modules: 
        if skip_private_mod and mod_name.startswith("_"):
            continue
        __import__(mod_name)
        class_name = filterClasses(mod_name, base_class, class_name_filter)
        if class_name:
            result.extend(class_name)
            #self.tools.append(loaded_class)
    return result
    
            
def filterClasses(mod_name, base, class_name_filter):
    class_name_filter = class_name_filter if isinstance(class_name_filter, list) else [class_name_filter]
    result = []
    for name, obj in inspect.getmembers(sys.modules[mod_name], inspect.isclass):
        parents =  [c.__name__ for c in inspect.getmro(obj)[1:]]
        if inspect.isclass(obj) and base.__name__ in parents and name not in class_name_filter:
            result.append(obj)
    return result        
    