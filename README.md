## Foldify

A python CLI Tool to manage folder structures.

##### Features
* Labels empty folders
* Copy a directory tree (only .txt files are copied, which can be used to note directory usage)
* Create a json template from a directory tree
* Create a directory tree from a json template
* Pretty Print a directory tree

##### Install
    python setup.py install

##### Usage: (use foldify.py or windows binday in dist folder)
    foldify source_folder [--label update|remove ] [dest_folder]
    foldidy --help

###### Prints directory tree
    foldidy source_file
###### Label Empty folders with *_EMPTY* suffix
    foldidy source_file --label update
    foldidy source_file --label remove
    foldidy source_file --label update --custom-label LABEL
###### Copy source_file directory to dest_file path
    foldidy source_file  dest_file
###### Create JSON of source_file as dest_file.json
    foldidy source_file  dest_file.json
###### Create dest_file directory from source_file.json
    foldidy source_file.json  dest_file


##### To Do
* Better Docs for commands
* Tree stats when printing tree
* Add Deepdiff integration
* More Tests
* Add Tkinter GUI
* Add Migration Feature

##### Done
* Recompile Windows binary.
* Add Licence
* Consolidate interactive and foldfity; make interactive mode an option.
* Custom labels
* Create create distribution for Windows
* Add argparse CLI interface
* Add options to include or not files
