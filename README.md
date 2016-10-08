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

If you have more than one pad you want to download, you can use a list. The layout uses a simple mardown syntax:

```
[TITLE](BASEURL)
```
Note: Lines with no links will be skipped. So feel free to organize your pad list in categories or add comments to the links etc.

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

## Notes

* By default the **empty pad detection** currently only works with riseup.net pads, as the beginning of the welcome message is necessary to do this. If you are using another provider you can add the message into the welcomeMessages list.
