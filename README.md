# epad-saver
script to download etherpads

Most etherpads are deleted after some period of time, if no edit happens. So here is a small script to generate backups of them.

## Features

* Simple download of txt files
* Batch download via a list
* Detects empty documents and unchanged versions

## Usage

* Downloading from a single URL

```
epad-saver.py -b https://yourpad.com/p/example
```
The content of the pad will be saved into the current directory. The title will be extracted from the provided baseurl.

* Downloading from list

If you have more than one pad you want to download, you can use a list. The format looks like
```
TITLE <BASEURL>
```
Note: Make sure you have a whitespace character between the title and your baseurl. Also the url needs to be placed between brackets

Now you can download all pads with:
```
epad-saver.py -f pads.md
```

* For further options like setting the title for the simple url download please use the help.

```
usage: epad-saver.py [-h] [-b BASEURL] [-t TITLE] [-f PADFILE] [-w WORKINGDIR]
                     [-s]

Save your Etherpads

optional arguments:
  -h, --help            show this help message and exit
  -b BASEURL, --baseurl BASEURL
                        BaseURL of the pad you like to save
  -t TITLE, --title TITLE
                        Title of the pad
  -f PADFILE, --padfile PADFILE
                        Path to a file containing a list of etherpads
  -w WORKINGDIR, --workingdir WORKINGDIR
                        Path to the directory the pad(s) are saved into;
                        Default: .
  -s, --no-duplicate-check
                        turn off the duplicate check
```

