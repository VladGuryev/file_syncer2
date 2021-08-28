# file_syncer2

## This is my personal utility for backuping one file from one place to another
(dont ask me why I need that, anyway..)

### Added multiple file sycn support (it was easy, so why not?)
Not thoroughly tested

### Confines
Ones added to hash_bd the records with certain file_labels from config.json will be the markers for
search of hashes of files. If they are changed after some synces happened the program
will be executing the sync even there is no real need for it.
