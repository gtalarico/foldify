ALLOWED_FILES = ['.txt',''] # blank is for folders

# IGNORE = ['(desktop.ini)', '(.*\.txt)']
IGNORE = ['(desktop.ini)', '(.*\.git)']
IGNORE_PATTERN = r'|'.join(IGNORE)

EMPTY_LABEL = '_EMPTY'
