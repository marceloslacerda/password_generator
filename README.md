# Password Generator

This is a small utility for locally handling passwords without storing 
the key, the hash of the key or any similar informations. Only the 
password metadata is stored and used to generate the actual password 
when requested.

## Usage

    password_generator get [--user=<usr>] [--url=<url>]
    password_generator set [--user=<usr>] [--url=<url>] [--length=<length>] [--symbols=<symbols>]
    password_generator list [--user=<usr>]
    password_generator rm [--user=<usr>] [--url=<url>]
