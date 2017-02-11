# Password Generator

This is a small utility for locally handling passwords without storing
the key, the hash of the key or any similar information. Only the
password metadata is stored and used to generate the actual password
when requested.

Since password-generator 1.0.0 the password is sent to the clipboard rather
than stdout. After 10 seconds the password is removed from the clipboard.

## Dependencies

In order to function, password-generator needs

* Python version ≥ 3.4
* pip for python 3

### How install the dependencies on debian jessie

    # apt-get install python3 python3-pip

    
## Installation

    $ pip3 install --user git+https://github.com/marceloslacerda/password_generator.git

Please remember that by default pip will install the password-generator script
on the directory $HOME/.local/bin, so it's advisable to add that directory to
your shell initialization.

If you use bash you can achieve that adding this line to your ~/.bashrc:

    PATH=$PATH:$HOME/.local/bin

To have your password automatically copied to the clipboard you must have **either** xclip, xsel, the python-gtk
library or the python-qt library installed.

### On Debian Jessie

#### To install xclip

    # apt-get install xclip

#### To install xsel

    # apt-get install xsel


## Usage

Password Generator

Usage:

    password_generator get [-U <usr> | --user=<usr>] [-u <url> | --url=<url>] [-n]
    password_generator set [-U <usr> | --user=<usr>] [-u <url> | --url=<url>] [-n] [--length=<length>] [--symbols=<symbols>]
    password_generator list [-U <usr> | --user=<usr>]
    password_generator rm [-U --user=<usr>] [-u <url> | --url=<url>] [-n]


    Options:
      -U <usr>, --user=<usr> The username associated with that password
      -u <url>, --url=<url>  The url that uses that password. It will be stripped of subdomains and trailing parameters. Use -n to disable this behaviour
      -n                     Use this when you want to use the url as it is
      --length=<length>      The length of the password
      --symbols=<symbols>    Extra symbols to be appended to the password

## Upgrading the password database

As of 0.1.0 password-generator will use a JSON file to store its
database, if you have used this software prior 0.1.0 you will need to
convert the old database to the new format. To accomplish that do:

    $ upgrade-password-database ~/.pinfo > ~/.pinfo.json

If some password entries cannot be converted, you will be informed of
them and the upgrade script will ignore them.

If for some reason all previous you are unable to convert any entry,
it's possible that you are running into a bug that password-generator
had with distutils. Try the following to upgrade your databae:

	$ git clone https://github.com/marceloslacerda/password_generator
	$ cd password_generator/password_generator
	$ ./upgrade_database.py ~/.pinfo > ~/.pinfo.json

Your database should, then, be converted to the JSON format and you
shouldn't need to run that script again.

## Warning

password-generator was not audited by any security specialist, you should be
very careful on how you use it. It's an improvement over text files to
manage your passwords or using the same password for every service, but I (the
developer) can provide you (the user) no warranties of the safety of
password-generator over online password manager services. For more information
consult the LICENSE file and the Known limitations section.

## Known limitations

password-generator works by hashing your password and its metadata a few
thousand times and takes a slice of that hash to use as your password (encoding
it as numbers and letters).

The hashing mechanism is PBKDF2 which is theoretically easy-ish to calculate
with ASICs or GPUs[1]. This means that if an attacker can obtain your database
file and a valid password (not extremely difficult to happen considering recent
password breaches in the wild) he could, through brute force, discover your
password.

Doing some back-of-the-envelope calculations I estimate that the number of
SHA passes needed to brute force your password would be the current number of
passes(PASS) times the number of possible masters with a certain password
length(LEN) using only characters in the English alphabet(ALPHA):

![Equation 1](/equations/equation1.gif)

Currently the number of passes that password-generator does is 150,000 and the
size of the English alphabet is 26. Popular wisdom[2] says that we should
use passwords of at least 12 characters. So the number of possible SHA
calculations necessary to calculate all masters the size of your password would
be:

![Equation 2](/equations/equation2.gif)

Depending on the speed of the hash breaking mechanism this is more or less
secure. As of November 2016 AntMiner S9[3] is reported to be the fastest
specialized SHA256 calculator commercially available. It can calculate
14,000,000 million hashes per second. For that sort of machine it would take

![Equation 3](/equations/equation3.gif)

or approximately 32 years to calculate all the hashes of 12 character
passwords to discover our master password.

Supposing that we wanted to have a rainbow table of all hashes we would need at
least 5 bits to store a character, times the number of characters in a password
times the number of hashes that you want to store.

![Equation 4](/equations/equation4.gif)

If those calculations are correct it's safe to assume that if your password
database is retrieved and a derived password is known you would have plenty
of time to change your master and all your passwords.

[1] https://en.wikipedia.org/wiki/PBKDF2#Alternatives_to_PBKDF2

[2] https://blog.codinghorror.com/speed-hashing/

[3] https://en.bitcoin.it/wiki/Mining_hardware_comparison
