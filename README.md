#Password Generator

This is a small utility for locally handling passwords without storing
the key, the hash of the key or any similar information. Only the
password metadata is stored and used to generate the actual password
when requested.

## Installation

    pip3 install --user git+https://github.com/marceloslacerda/password_generator.git

Please remember that by default pip will install the password-generator script
on the directory $HOME/.local/bin, so it's advisable to add that directory to your shell initialization.

If you use bash you can achieve that adding this line to your ~/.bashrc:

    PATH=$PATH:$HOME/.local/bin

## Usage

    password_generator get [--user=<usr>] [--url=<url>]
    password_generator set [--user=<usr>] [--url=<url>] [--length=<length>] [--symbols=<symbols>]
    password_generator list [--user=<usr>]
    password_generator rm [--user=<usr>] [--url=<url>]

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

    PASS*len(ALPHA)**LEN

Currently the number of passes that password-generator does is 150,000 and the
size of the English alphabet is 26. Popular wisdom[2] says that we should
use passwords of at least 12 characters. So the number of possible SHA
calculations necessary to calculate all masters the size of your password would
be:

    150,000*(26**12) = 1.4*10**22

Depending on the speed of the hash breaking mechanism this is more or less
secure. As of November 2016 AntMiner S9[3] is reported to be the fastest
specialized SHA256 calculator commercially available. It can calculate
14,000,000 million hashes per second. For that sort of machine it would take

    1.4*10**22 / 14000000000 = 10**12 seconds

or approximately 32 thousand years to calculate all the hashes of 12 character
passwords to discover our master password.

Supposing that we wanted to have a rainbow table of all hashes we would need at
least 5 bits to store a characteri, times the number of characters in a password
times the number of hashes that you want to store.

    5 * 1.4*10**22 = 8.75*10**21 bytes or 8.21 zettabytes

If those calculations are correct it's safe to assume that if your password
database is retrieved and a derived password is known you would have plenty
of time to change your master and all your passwords.

[1] https://en.wikipedia.org/wiki/PBKDF2#Alternatives_to_PBKDF2

[2] https://blog.codinghorror.com/speed-hashing/

[3] https://en.bitcoin.it/wiki/Mining_hardware_comparison
