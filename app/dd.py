file_path=r'C:\Users\Olu-Ade\HTTP CODE CRAFTERS\codecrafters-http-server-python\app\files\hello.txt'
with open(file_path, 'r') as file:
    content = file.read()
    print(content)