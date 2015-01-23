import numpy as np

def load_config(defaults):
    """Create a configuration dictionary from a defaults dictionary.
    The defaults dictionary predefines valid key/value pairs and
    populates those with default values.  The config dictionary and
    kwargs are then used to update the values in the default
    configuration dictionary."""

    o = {}
    for key, item in defaults.iteritems():

        if isinstance(item,dict):
            o[key] = load_config(item)
        elif isinstance(item,tuple):
            item_list = [None,'',None,str]
            item_list[:len(item)] = item        
            value, comment, groupname, item_type = item_list

            if len(item) == 1:
                raise Exception('Option tuple must have at least one element.')
                    
            if value is None and (item_type == list or item_type == dict):
                value = item_type()
            
            keypath = key.split('.')

            if len(keypath) > 1:
                groupname = keypath[0]
                key = keypath[1]
                    
            if groupname:
                group = o.setdefault(groupname,{})
                group[key] = value
            else:
                o[key] = value
        else:
            raise Exception('Unrecognized type for default dict element.')

    return o


def update_dict(d0,d1,add_new_keys=False,append=False):
    """Recursively update the contents of python dictionary d0 with
    the contents of another python dictionary, d1.

    add_new_keys : Do not skip keys that already exist in d0.
    """

    if d0 is None or d1 is None: return
    
    for k, v in d0.iteritems():

        if not k in d1: continue

        if isinstance(v,dict) and isinstance(d1[k],dict):
            update_dict(d0[k],d1[k],add_new_keys,append)
        elif isinstance(v,list) and isinstance(d1[k],str):
            d0[k] = d1[k].split(',')            
        elif isinstance(v,np.ndarray) and append:
            d0[k] = np.concatenate((v,d1[k]))
        else: d0[k] = d1[k]

    if add_new_keys:
        for k, v in d1.iteritems(): 
            if not k in d0: d0[k] = d1[k]
