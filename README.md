# file_syncer2

## This is my personal utility for backuping one file from one place to another
(dont ask me why I need that, anyway..)

### Added multiple file sycn support (it was easy, so why not?)
Not thoroughly tested

### Use case
I needed to backup one file from one place to another if it has changed since last verify. So I wrote this
script. To launch it you should configure source file path and dest folder in config.json. Dest folder should exist otherwise the script fails.
Now more than one file sync is supported by providing in json many file_label sections. File label string - label for human to recognize the file by program whatever.

### Confines
Ones added to hash_bd the records with certain file_labels from config.json will be the markers for
search of hashes of files. If they are changed after some synces happened the program
will be executing the sync even there is no real need for it.
