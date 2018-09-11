def print_fun(y,z=False,level=0):
	for x in y:
		if isinstance(x,list):
			print_fun(x,z,level+1)
		else:
			if z:
				for m in range(level):
					print("\t",end='')
			print(x)
##这是"function"模块，提供了一个名为print_y()的函数，这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。
		
##这个函数名为"y",这可以是任何python列表。所指定的列表中的每个数据项会（递归到）输出到屏幕上，各数据项各占一行。

