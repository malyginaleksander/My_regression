Dim Arg, path1, str1, str2, full_1, full_2 
Set Arg = WScript.Arguments

'Parameter1, begin with index0
path1 = Arg(0)
str1 = Arg(1)
str2 = "B" + str1
full_1 = path1 + str1
full_2 = path1 + str2

set objExcel = createObject("Excel.Application")
objExcel.visible = True

set objWb = objExcel.Workbooks.Open(full_1)
objWb.saveas full_2

'Cleanup
objWb.Close True
Set objWb = Nothing
ObjExcel.Quit
Set ObjExcel = Nothing
Set Arg = Nothing
