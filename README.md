# Randowis Scraper
A simple web scraper for all your Randowis Comics needs.

## Requirements
This script requires:
* *Python 3*
    * On Windows use [this installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe).
    * On Arch based systems use `sudo pacman -Syu python`.
    * On Debian/Ubuntu based systems use `sudo apt install python3.8`.
    * Mac users aren't real people so they can figure it out themselves.
        * JK, you can use [this](https://www.python.org/downloads/mac-osx/).

* *Beautiful Soup*
    * You can install it with `pip` using `pip install beautifulsoup4`
    
## Usage
Open up your terminal/command prompt and enter the following:\
*Of course changing the **/path/to/script/** part*

`python /path/to/script/randowis-scraper.py` 
 
 ### Flags
 Options to pass to the script
 * `-h` or `--help`
    * Will display pretty much what I'm explaining now.
 * `-f` or `--first`
    * Gets the first comic on the first page
 * `-ks` or `--keep-page-structure`
    * Comics will be separated by pages