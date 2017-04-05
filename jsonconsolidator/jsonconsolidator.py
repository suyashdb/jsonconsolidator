# -*- coding: utf-8 -*-


"""bootstrap.bootstrap: provides entry point main()."""


__version__ = "0.0.1"


import sys, shutil
from .stuff import Stuff
import re, os, glob
import json, copy

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
    print("List of argument strings: %s %s" % (sys.argv[1:], sys.argv[2:]))
    # print("Stuff and Boo():\n%s\n%s" % (Stuff, Boo()))
    '''Check if dataset has session and edit search paths for json files accordingly'''
    bids_dspath = sys.argv[1]
    second_argument = 0


    if len(sys.argv) < 2:
        print("Usage: jsonconsolidator path/to/dataset")
        sys.exit()
    if len(sys.argv) ==3:
        second_argument = sys.argv[2]
    else:
        change_file = False
        print("Dry Run - No files will be actually changed.")

    if second_argument == '-v':
        change_file = False
    elif second_argument == 'final':
        change_file = True

    if second_argument == 'final':
        bakdir = os.path.join(bids_dspath,'.backup_json')
        if os.path.isdir(bakdir) is False:
            os.mkdir(bakdir)



    files_list = []
    regex = r"(?<=task-).*?(?=_)"
    tasks = []
    task  = 'xyz'
    json_list = []
    alljson_list = []
    allfiles = []
    iter_top_flag = 0
    # change_file = False
    iterate_topJsons = False
    changefile_list = []
    deletefile_list = []
    newfile_list = []

    def compareList(li):
        result = copy.deepcopy(li[0])
        for element in li:
            for key in element:
                if key in result and result[key] != element[key]:
                    del result[key]
        return result

    if not glob.glob(os.path.join(bids_dspath, 'sub-*/ses*')):
        print("dataset has single session")
        search_path = os.path.join(bids_dspath,'sub-*/func/sub*task*.json')
        task_search_path = os.path.join(bids_dspath, 'sub-*/func/')
    else:
        search_path = os.path.join(bids_dspath,'sub-*/ses*/func/sub*ses*task*.json')
        task_search_path = os.path.join(bids_dspath, 'sub-*/ses*/func/')

    files = glob.glob(search_path)
    if len(files) == 0:
        print("There are no json files at sub*/func/ level to consolidate. Everything looks great. exiting...")
        sys.exit()

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
    # print(tasks)
    for task in set(tasks):
        task_path = os.path.join(task_search_path, ('sub*task-' + task +'*.json'))
        taskfiles = glob.glob(task_path)
        allfiles.extend(glob.glob(task_path))
        for file in taskfiles:
            json_list.append(json.loads(open(file).read()))
        #iter all dict in the list to find common key value pair
        common = compareList(json_list)
        # common = dict(pair for pair in json_list[0].items()
        #  if all((pair in d.items() for d in json_list[1:])))
        #create top level json for every task
        task_json_path = os.path.join(bids_dspath, ('task-%s_bold.json' % (task)))
        #write common to top level task jsons
        if common:
            if os.path.exists(task_json_path):
                old_data = json.loads(open(task_json_path).read())
                common = {k:v  for k, v in old_data.items()  for k1,v1 in common.items() if k ==k1 and v==v1}
                if common != old_data:
                    common.update(old_data)
            if change_file is True:
                with open(task_json_path, 'w') as outfile:
                    json.dump(common, outfile, indent = 4)
                    newfile_list.append(task_json_path)
            else:
                newfile_list.append(task_json_path)
            iter_top_flag = iter_top_flag + 1 #count how many tasks have common k:v

        '''delete common elements from each task json or delete jsons if all k:v are same in all jsons '''
        for basefile in taskfiles:
            file_data = json.loads(open(basefile).read())
            value = { k : file_data[k] for k in set(file_data) - set(common) }
            '''if the whole data is common then delete the files at base level'''
            if not value:
                if change_file is True:
                    shutil.copy2(basefile, bakdir)
                    print("all jsons are common hence base level json files are deleted, and a top level task json file is created")
                    os.remove(basefile)
                else:
                    # print(basefile, " - will be deleted")
                    deletefile_list.append(basefile)
            else:
                for k, v in value.items():
                    if type(value[k]) is list:
                        if any(isinstance(el, list) for el in value[k]):    # checks if slicetiming is list of lists
                            if k in value.keys():
                                value[k] = sum(value[k], []) # flatten list of lists
                #print("not common values are -  ", value, task)
                if change_file is True:
                    iterate_topJsons == True
                    print("rewriting after removing common key:value pairs from json at subject level - ", basefile)
                    shutil.copy2(basefile, bakdir)
                    with open(basefile, 'w') as writefile:
                        json.dump(value, writefile, indent = 4)
                    changefile_list.append(basefile)
                else:
                    # print("Dry Run ... Following file will be re-written after removing common k:v pairs - ", basefile)
                    changefile_list.append(basefile)
                # if any(isinstance(el, list) for el in value['SliceTiming']):    # checks if slicetiming is list of lists
                #     if 'SliceTiming' in value.keys():
                #         value['SliceTiming'] = sum(value['SliceTiming'], []) # flatten list of lists
                # with open(basefile, 'w') as writefile:
                #     json.dump(value, writefile, indent = 4)
        print("Common k:v pairs for task-", task, '\n', common)
        print("***** Files to be changed after removing above common k:v pair***** \n ", changefile_list, '\n')
        changefile_list = []
    print("**** Files that will be deleted****\n", deletefile_list, '\n')
    print("***** New Files that will be created are *****\n", newfile_list, '\n' )





    #check for items common in all task jsons created at top level
    # if iterate_topJsons is True:
    if iter_top_flag == len(set(tasks)) & iterate_topJsons == True:
        filesearch = 'task-*bold.json'
        alltaskfiles = glob.glob(os.path.join(bids_dspath, filesearch))
        for file in alltaskfiles:
            alljson_list.append(json.loads(open(file).read()))
        if len(alljson_list) > 1:
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
        else:
            print("All jsons are already consolidated and doesnt require further cosolidation")
            sys.exit()




class Boo(Stuff):
    pass
