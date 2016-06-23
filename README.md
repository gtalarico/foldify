## Foldify

An interactive CLI Tool to manage folder structures.
dist folder includes windows binary.

##### Usage:
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
* consolidate interactive and foldfity. Make interactive an option.
* Rebuild Tests
* Add Tkinter GUI
* Add Licence

##### Done
* Create create distribution for Windows
* Add real argparse CLI interface
* add options to include or not files
