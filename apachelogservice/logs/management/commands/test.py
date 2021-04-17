path = r'D:\Dev\brandquad_test\apachelogservice/logs/logs_dir\watch?v=3ndEeGDVqD4.txt'
path2 = r'D:\Dev\brandquad_test\apachelogservice/logs/logs_dir\access.log'

path3 = f'{path}'
path4 = f'{path2}'
paths = [path, path2, path3, path4]
for path in paths:
    print(path)

with open(path) as f:
    f.write("123")
