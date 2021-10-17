filename = 'test.my.file.png'

file_components = filename.rsplit('.', 1)
suffix = file_components[-1]
prefix = file_components[0]
print(suffix)
print(prefix)
