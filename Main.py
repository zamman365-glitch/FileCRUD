from pathlib import Path
import os


def readfileandfolder():
    try:
        p = Path('')
        items = list(p.rglob('*'))

        for index, file in enumerate(items):
            print(f'{index+1} - {file}')

    except Exception as e:
        print(e)


def create_file():

    try:
        readfileandfolder()

        file_name = input('Enter the name of file:- ')
        p = Path(file_name)

        if p.exists():
            print("FILE ALREADY EXISTS")

        else:
            with open(file_name, 'w') as file:

                content = input('Enter your file content:- ')
                file.write(content)

                print('FILE ADDED!')

    except Exception as e:
        print(e)


def read_file():

    try:
        readfileandfolder()

        file_name = input("Enter name of your file:- ")
        p = Path(file_name)

        if p.exists():

            with open(file_name, 'r') as file:
                print(file.read())

        else:
            print('FILE NOT FOUND!')

    except Exception as e:
        print(e)


def update_file():

    try:
        readfileandfolder()

        file_name = input("Enter name of your file:- ")
        p = Path(file_name)

        if p.exists():

            print('Press 1 to overwrite the content:-')
            print('Press 2 to append new content:-')

            option = int(input("Enter your choice:- "))

            if option == 1:

                with open(file_name, 'w') as file:

                    content = input('Enter your content:- ')
                    file.write(content)

                    print('CONTENT CHANGED...')

            elif option == 2:

                with open(file_name, 'a') as file:

                    content = input('Enter your content:- ')
                    file.write(content)

                    print('CONTENT APPENDED...')

            else:
                print("INVALID INPUT")

        else:
            print('FILE DOES NOT EXIST')

    except Exception as e:
        print(e)


def delete_file():

    try:
        readfileandfolder()

        file_name = input("Enter file name to delete:- ")
        p = Path(file_name)

        if p.exists():

            os.remove(p)   # os is removing path of that file 

            print("FILE DELETED!")

        else:
            print("FILE NOT FOUND!")

    except Exception as e:
        print(e)

def rename_file():
    try:
        readfileandfolder()
        file_name=input('Enter name of your file:')
        p=Path(file_name)
        if p.exists():
            new_file=input('Enter new name of file:')
            p.rename(new_file)
            print('FILE RENAMED!')
        else:
            print('FILE NOT FOUND!')
    except Exception as e:
        print(e)

def  create_folder():
    try:

        readfileandfolder()
        folder_name=input('enter name of your folder:')
        p=Path(folder_name)
        if p.exists():
            print('FOLDER ALREADY EXISTS!')
        else:
            p.mkdir()
            print('FOLDER CREATED!')


    except Exception as e:
        print(e)

def delete_folder():
    try:

        readfileandfolder()
        folder_name=input('enter name of your folder:')
        p=Path(folder_name)
        if p.exists():
            p.rmdir()
            print('FOLDER DELETED !')
        else :
            print('FOLDER NOT FOUND !')

    except Exception as e:
        print(e)



def folder_file():

    readfileandfolder()

    folder_name = input('Enter name of your folder: ')
    file_name = input('Enter the name of file: ')

    # Folder path
    p = Path(folder_name)

    if p.exists():
        print('FOLDER ALREADY EXISTS!')

    else:
        p.mkdir()
        print('FOLDER CREATED!')

    # File path inside folder
    file_path = p / file_name

    with open(file_path, 'w') as file:

        content = input('Enter your file content: ')
        file.write(content)

        print('FILE ADDED!')







   




while True:

    print("\nPress 1 for creating a file")
    print("Press 2 for reading a file")
    print("Press 3 for updating a file")
    print("Press 4 for deleting a file")
    print("Press 5 for renaming a file")
    print("Press 6 for creating a folder")
    print("Press 7 for deleting a folder")
    print("Press 8 for creating a folder and file in folder")
    print("Press 0 for exiting")

    option = int(input("Enter your choice:- "))

    if option == 1:
        create_file()

    elif option == 2:
        read_file()

    elif option == 3:
        update_file()

    elif option == 4:
        delete_file()
    
    elif option == 5:
        rename_file()

    elif option == 6:
        create_folder()

    elif option == 7:
        delete_folder()

    elif option ==8:
        folder_file()

    elif option == 0:
        print("PROGRAM EXITED")
        break

    else:
        print("INVALID OPTION")