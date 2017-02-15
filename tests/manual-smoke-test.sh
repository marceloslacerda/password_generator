#!/bin/sh

echo "###Password should be equal to Z9x9Y6IgYMhrVvRt###"
password-generator get --db foobar.json -n -u foo.bar -U my-user --debug 123
echo "###Password should be equal to Z9x9Y6IgYMhrVvRt###"
password-generator get --db foobar.json -u http://foo.bar -U my-user --debug 123
echo "###Should show password not found###"
password-generator get --db foobar.json -n -u http://foo.bar -U my-user --debug 123
echo "###Should show password not found###"
password-generator get --db foobar.json -u http://foo.bar -U my-foo --debug 123
echo "###Should set a password###"
printf "y\n" | password-generator set --db barbaz.json -n -u bar.baz -U my-user --debug 123
echo "###Should show the new password equal to the value set previously###"
password-generator get --db barbaz.json -n -u bar.baz -U my-user --debug 123
echo "###Should ask for confirmation before overwriting the password###"
printf "y\ny\n" | password-generator set --db barbaz.json -n -u bar.baz -U my-user --debug 123
echo "###Should show the overwritten password different from before###"
password-generator get --db barbaz.json -n -u bar.baz -U my-user --debug 123
echo "###Should set a password with sybols and length 5###"
printf "y\n" | password-generator set --db barbaz.json -n -u bor.baz -U my-user --debug 123 --length=5 --symbols=#@
echo "###Should show the previously set password###"
password-generator get --db barbaz.json -n -u bor.baz -U my-user --debug 123
echo "###Should remove the password###"
password-generator rm --db barbaz.json -n -u bor.baz -U my-user
echo "###Should show password not found###"
password-generator get --db barbaz.json -n -u bor.baz -U my-user --debug 123
echo "###Should show version not supported###"
password-generator get --db highversion.json -n -u foo.bar -U my-user --debug 123
rm barbaz.json
