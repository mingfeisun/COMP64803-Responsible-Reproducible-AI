def try_finally_file_read(filename): 
    print(f'Opening {filename}')
    file = open(filename, encoding='utf-8')
    try:
        print(f'Reading File')
        file.read()
    finally: 
        print(f'Closing File')
        file.close() 


filename = 'sudo_files/sudo_file.txt'

with open(filename, 'wb') as f: 
    f.write(b'\xf1\xf2\xf3\xf4\xf5')

try: 
    try_finally_file_read(filename) 
except UnicodeDecodeError as f:
    print(f'*****\n{f}\n*****') 
    print('Reading file without try block')
    file = open(filename, encoding='utf-8')
    print('Trying to read')
    try: 
        file.read()
    except Exception as e: 
        file.close()
        # Here we actually close the file because I don't want memory leaks, but pretend I didnt
        e.add_note('SUDO MESSAGE: The file was not closed')
        raise 