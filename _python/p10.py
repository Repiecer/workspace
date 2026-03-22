import this
zen = this.s
lines = len(zen.splitlines())
words = len(zen.split())
chas = len(zen)
spaces = zen.count(' ')
print('Zen of Python统计')
print(f'行数:{lines}', f'单词数:{words}', f'字符数:{chas}', f'空格数:{spaces}', sep='\n')
