## Foldify

A python CLI Tool to manage folder structures.
dist folder includes windows binary.

##### Features
* Copy a directory tree (only .txt files are copied, which can be used to note directory usage)
* Create a JSON from a directory tree.
* Create a directory tree from a json
* Print a directory tree.

##### Usage: (use foldify.py or windows binday in dist folder)
python foldify.py source_folder [dest_folder]

foldidy.exe --help
foldify.exe source_file [dest_file] 

##### Prints directory tree
    foldidy.exe source_file
##### Copy source_file directory to dest_file path
    foldidy.exe source_file  dest_file 
##### Create JSON of source_file as dest_file.json
    foldidy.exe source_file  dest_file.json 
##### Create dest_file directory from source_file.json
    foldidy.exe source_file.json  dest_file 
    

##### To Do
* Recompile linux binary.
* consolidate interactive and foldfity; make interactive mode an option.
* Add more stats when printing tree.
* Rebuild Tests
* Add Licence ?
* Add Tkinter GUI

##### Done
* Create create distribution for Windows
* Add real argparse CLI interface
* add options to include or not files
