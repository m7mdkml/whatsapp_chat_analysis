# text_replacement.py by mohammed - This program will let you replace a specific line of text

# These variables will hold your inputs  
target = input("Enter text to be replaced: ")
replacement = input("Enter the replacement text: ")

# target file that will be changed
file_source = "wedo_chat_2017_2024.txt" 

# Opens and reads the text file then stores it
with open(file_source, 'r') as file: 
    file_content = file.read() 

# This line contains the function to replace from our input
replaced_content = file_content.replace(target, replacement)

with open(file_source, 'w') as file:
    file.write(replaced_content)
    
print("\ndid it work?")
