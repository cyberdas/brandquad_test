import os


url = 'http://www.almhuette-raith.at/apache-log/access.log'
filename = url.split("/")[-1] # 
print(filename)
sequence = ""
filenames = ["apache%s.log", "apache%s.log", "apache%s.log"]
path = os.getcwd()
print(path)
print(os.path.join(path, "apache.log"))
filepath = ""
print(path)

# путь в директорию с логами

for filename in filenames:
    while os.path.isfile(filename % sequence):
        sequence = int(sequence or 0) + 1
    filename = filename % sequence
    print(filename)

print(os.getcwd())