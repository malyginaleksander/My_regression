import inspect
import xlrd
import os

def worksheet(filename, sheet):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    source_filename = module.__file__
    local_path = os.path.join(os.path.dirname(source_filename),filename)
    #print ("DEBUG loading {}".format(local_path))
    full_path = os.path.abspath(local_path)
    #print ("DEBUG loading full {}".format(full_path))
    workbook = xlrd.open_workbook(full_path)
    worksheet = workbook.sheet_by_name(sheet)
    return worksheet
