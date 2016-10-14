# Password Generator

This is a small utility for locally handling passwords without storing 
the key, the hash of the key or any similar informations. Only the 
password metadata is stored and used to generate the actual password 
when requested.

## Installation

   pip3 install --user git+https://github.com/marceloslacerda/yesno.git
   pip3 install --user git+https://github.com/marceloslacerda/password_generator.git

Please remember that by default pip will install the script password-generator
on the directory $HOME/.local/bin, so it's advisable to add that directory to
to your shell initialization.

On bash you can achieve that adding this line to your ~/.bashrc:

    PATH=$PATH:$HOME/.local/bin

## Usage

    password_generator get [--user=<usr>] [--url=<url>]
    password_generator set [--user=<usr>] [--url=<url>] [--length=<length>] [--symbols=<symbols>]
    password_generator list [--user=<usr>]
    password_generator rm [--user=<usr>] [--url=<url>]


## Warning

password-generator was not audited by any security specialist, you should be
very careful on how you deal with it. It's an improvement over text files to
manage your passwords or using the same password for every service, but I(the
developer) can provide the user(you) no warranties of the safety of
password-generator over online password manager services.

## Known limitations

password-generator works by hashing your password and its metadata a few thousand times and takes a slice of that hash to use as your password(encoding it as numbers and letters).

The hashing mechanism is PBKDF2 which is theoretically easy-ish to calculate
with ASICs or GPUs[1] this means that if an attacker can obtain your database
file and a valid password(not extremely difficult to happen considering recent
password breaches in the wild) he could, through brute force discover your
password.

Doing some back-of-envelope calculation I estimate that the number of
SHA passes needed to bruteforce your password would be, the current number of
passes(PASS) times the number of possible masters that you could with your
password length(LEN) considering the types of characters that could appear in
your password(ALPHANUM):

    PASS*len(ALPHANUM)**LEN

Currently the number of passes that password-generator does is 150,000 and the
size of ALPHANUM is 62, popular wisdom[2] says that we should use passwords of at least 12 characters. So the number of possible SHA calculations necessary
to calculate all masters the size of your password would be:

    150,000*(62**12) = 4.83x10^26

Depending on the speed of the hash breaking mechanism this 


[1] https://en.wikipedia.org/wiki/PBKDF2#Alternatives_to_PBKDF2
[2] https://blog.codinghorror.com/speed-hashing/
