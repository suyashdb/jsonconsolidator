# -*- coding: utf-8 -*-


"""bootstrap.bootstrap: provides entry point main()."""


__version__ = "0.0.1"


import sys
from .stuff import Stuff
import re, os, glob
import json

# bids_dspath = '/Users/suyashdb/Downloads/ds212'

# files_list = []
# regex = r"(?<=task-).*?(?=_)"
# tasks = []
# task  = 'xyz'
# json_list = []
# alljson_list = []
# allfiles = []
# iter_top_flag = 0


def main():
    # print("Executing bootstrap version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    # print("Stuff and Boo():\n%s\n%s" % (Stuff, Boo()))
    '''Check if dataset has session and edit search paths for json files accordingly'''
    bids_dspath = sys.argv[1]
    if len(sys.argv) < 2:
        print("Usage: jsonconsolidator path/to/dataset")
        sys.exit()
    files_list = []
    regex = r"(?<=task-).*?(?=_)"
    tasks = []
    task  = 'xyz'
    json_list = []
    alljson_list = []
    allfiles = []
    iter_top_flag = 0
    if not glob.glob(os.path.join(bids_dspath, 'sub-*/ses*')):
        print("No sessions")
        search_path = os.path.join(bids_dspath,'sub-*/func/sub*task*.json')
        task_search_path = os.path.join(bids_dspath, 'sub-*/func/')
    else:
        search_path = os.path.join(bids_dspath,'sub-*/ses*/func/sub*ses*task*.json')
        task_search_path = os.path.join(bids_dspath, 'sub-*/ses*/func/')

    files = glob.glob(search_path)
    '''find all task names from the json files'''
    for file in files:
        x = os.path.basename(file)
        files_list.append(x)
    for file in files_list:
        a = re.search(regex, file).group(0)
        if task not in a:
            tasks.append(a)
            task = a
        else:
            pass

    #check common key values pair in specific task jsons, for eg- if we have
    # 4 tasks, look for common key-values in each task and store a top level
    #json for it
    for task in set(tasks):
        task_path = os.path.join(task_search_path, ('sub*task-' + task +'*.json'))
        taskfiles = glob.glob(task_path)
        allfiles.extend(glob.glob(task_path))
        for file in taskfiles:
            json_list.append(json.loads(open(file).read()))
        #iter all dict in the list to find common key value pair
        common = dict(pair for pair in json_list[0].items()
         if all((pair in d.items() for d in json_list[1:])))
        #create top level json for every task
        task_json_path = os.path.join(bids_dspath, ('task-%s_bold.json' % (task)))
        #write common to top level task jsons
        if common:
            if os.path.exists(task_json_path):
                old_data = json.loads(open(basefile).read())
                common = {k:v  for k, v in old_data.items()  for k1,v1 in common.items() if k ==k1 and v==v1}
                if common != old_data:
                    common.update(old_data)
            with open(task_json_path, 'w') as outfile:
                json.dump(common, outfile, indent = 4)
            iter_top_flag = iter_top_flag + 1 #count how many tasks have common k:v

        '''delete common elements from each task json or delete jsons if all k:v are same in all jsons '''
        for basefile in taskfiles:
            file_data = json.loads(open(basefile).read())
            value = { k : file_data[k] for k in set(file_data) - set(common) }
            '''if the whole data is common then delete the files at base level'''
            if not value:
                print("all jsons are common hence base level json files are deleted, and a top level task json file is created")
                os.remove(basefile)
            else:
                if any(isinstance(el, list) for el in value['SliceTiming']):    # checks if slicetiming is list of lists
                    if 'SliceTiming' in value.keys():
                        value['SliceTiming'] = sum(value['SliceTiming'], []) # flatten list of lists
                with open(basefile, 'w') as writefile:
                    json.dump(value, writefile, indent = 4)


    #check for items common in all task jsons created at top level
    # if iterate_topJsons is True:
    if iter_top_flag == len(set(tasks)):
        filesearch = 'task-*bold.json'
        alltaskfiles = glob.glob(os.path.join(bids_dspath, filesearch))
        for file in alltaskfiles:
            alljson_list.append(json.loads(open(file).read()))

        all_common = dict(set.intersection(*[set(d.items()) for d in alljson_list]))

        if all_common:
            with open(os.path.join(bids_dspath, 'bold.json'), 'w') as outfile:
                    json.dump(all_common, outfile, indent = 4)
        for toptaskfile in alltaskfiles:
            file_data = json.loads(open(toptaskfile).read())
            value = { k : file_data[k] for k in set(file_data) - set(all_common) }
            if not value:
                    print( toptaskfile, "- json data is same as bold.json hence it is deleted")
                    os.remove(toptaskfile)
            else:
                if 'SliceTiming' in value.keys():    # checks if slicetiming is list of lists
                    if any(isinstance(el, list) for el in value['SliceTiming']):
                        value['SliceTiming'] = sum(value['SliceTiming'], []) # flatten list of lists
    #             print("not common values at top josn level are -  ", value)
                with open(toptaskfile, 'w') as writefile:
                    json.dump(value, writefile, indent = 4)



class Boo(Stuff):
    pass
