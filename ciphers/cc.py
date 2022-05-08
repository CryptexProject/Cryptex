#!/usr/bin/python

# caesar cipher package for the the codex project
# created by : C0SM0

# imports
import sys
import getopt

# help menu for displaying argument options
help_menu = """
      +------------------------------------------------------+
      |  [+] ARGUMENTS Caesar-Cipher                         |
      |  [+] ARG 1. Ciphering Process                        |
      |          [-e] ---------- Encrypt                     |
      |          [-d] ---------- Decrypt                     |
      |          [-b] ---------- Brute Force                 |
      +------------------------------------------------------+--+
      |  [+] ARG 2. Additional Aruments                         |
      |          [-k <int key>] ----------- Key                 |
      |              [not required for bruteforcing '-b']       |
      |          [-r <start,finish>] ------ Range               |
      |          [-t <plaintext>] --------- Input Text          |
      |          [-i <input file>] -------- Input File [.txt]   |
      |          [-o <output file>] ------- Output File         |
      |          [-e <plaintext>] --------- Custom exclude list |
      +---------------------------------------------------------+  
      |  [+] Example:                                           |
      |          cryptex -cc -e -k 5 -t hello -e "asd[]"        |  
      +---------------------------------------------------------+
    """

# generate path
# path = f"{getpass.getuser()}@caesar-cipher $ "

# encrypts content
def encrypt_caesar(plain_content, encryption_key, print_cnt, exclude):
    # output variable
    output = ''
 
    # encryption process
    for character in plain_content:
        if character in exclude:
            output += character
        elif character.isupper():
            output += chr((ord(character) + int(encryption_key) - 65) % 26 + 65)
        else:
            output += chr((ord(character) + int(encryption_key) - 97) % 26 + 97)

    # output content to cli
    if print_cnt == True:
        print(f'Encrypted Content:\n{output}\n')

    # output content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')


# decrypts content
def decrypt_caesar(plain_content, encryption_key, print_cnt, exclude):
    # output variable
    output = ''
 
    # decryption process
    for character in plain_content:
        if character in exclude:
            output += character
        elif character.isupper():
            output += chr((ord(character) - int(encryption_key) - 65) % 26 + 65)
        else:
            output += chr((ord(character) - int(encryption_key) - 97) % 26 + 97)

    # outputs content to cli
    if print_cnt == True:
        print(f'Decrypted Content:\n{output}\n')

    # outputs content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')

# bruteforces content
def bruteforce_caesar(plain_content, print_cnt, exclude, start_range=0, end_range=27):
    # output variable
    output = ''

    shift_key = start_range
    for shift in range(start_range, end_range):
        output += f'Shift Key: {shift_key}\n'
        shift_key += 1

        for character in plain_content:
            if character in exclude:
                output += character
            elif character.isupper():
                output += chr((ord(character) - shift - 65) % 26 + 65)
            else:
                output += chr((ord(character) - shift - 97) % 26 + 97)

        output += '\n\n'

    # outputs content to cli
    if print_cnt == True:
        print(f'Bruteforced Content:\n{output}\n')

    # outputs content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')

# parse all arguments
def caesar_parser():
    opts, _ = getopt.getopt(sys.argv[2:], 'k:i:t:o:r:e:', ['key', 'inputFile', 'inputText', 'outputFile', 'range', 'excludeList'])
    arg_dict = {}

    # loop through arguments, assign them to dict [arg_dict]
    for opt, arg in opts:
        # processing options
        if opt == '-k':
            arg_dict['-k'] = int(arg)
        if opt == '-r':
            arg_dict['-r'] = arg.split(',')
        # input options
        if opt == '-i':
            arg_dict['-i'] = arg
        if opt == '-t':
            arg_dict['-t'] = arg
        # output options
        if opt == '-o':
            arg_dict['-o'] = arg
        # exclude list
        if opt == '-e':
            arg_dict['-e'] = arg

    return arg_dict

# command line interface
def cli(argument_check):

    # one liners
    if argument_check == True:

        # tries to get all arguments
        try:
            arguments = caesar_parser()

        # catches arguments with no value
        except getopt.GetoptError:
            print(f'[!!] No value was given to your argument\n{help_menu}')

        # continues with recieved arguments
        else:    
            # getting variables for ciphering process
            key = arguments.get('-k')
            inputted_content = arguments.get('-t')
            print_content = True

            # symbols that can't be processed through the cipher
            exclude = "\n\t .?!,/\\<>|[]{}@#$%^&*()-_=+`~:;\"'0123456789" # Why aren't numbers processed? (Mart)

            
            # checks users output type
            if ('-i' in arguments):
                # tries to read file
                try:
                    inputted_content = open(arguments.get('-i'), 'r').read()

                # file does not exist
                except FileNotFoundError:
                    print('[!!] The attached file does not exist')

            # checks if output was specified
            if ('-o' in arguments):
                print_content = arguments.get('-o')

            # checks if range was specified
            if '-r' in arguments:   
                range = arguments.get('-r', False)

            # checks if custom exclude list was specified
            if '-e' in arguments:
                exclude = arguments.get('-e')

            # check ciphering process
            ciphering_process = sys.argv[1]

            # attempts to run cipher
            try:
                # encrypts caesar
                if ciphering_process == '-e':
                    encrypt_caesar(inputted_content, key, print_content, exclude)

                # decrypts caesar
                elif ciphering_process == '-d':
                    decrypt_caesar(inputted_content, key, print_content, exclude)

                # bruteforce caesar
                elif ciphering_process == '-b':
                    range = range if '-r' in arguments else False
                    if range == False:
                        bruteforce_caesar(inputted_content, print_content, exclude)
                    else:
                        bruteforce_caesar(inputted_content, print_content, exclude, int(range[0]), int(range[1])+1)

                # exception
                else:
                    print(f'[!!] No Key or Argument was specified\n{help_menu}')
                    
            # catches unspecified arguments
            except TypeError:
                print(f'[!!] No Key or Argument was specified\n{help_menu}')

    # help menu 
    else:
        print(help_menu)

# main code
def caesar_main():

    # checks for arguments
    try:
        sys.argv[1]
    except IndexError:
        arguments_exist = False
    else:
        arguments_exist = True

    cli(arguments_exist)

# runs main function if file is not being imported
if __name__ == '__main__':
    caesar_main()
