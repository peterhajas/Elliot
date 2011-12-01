Elliot
======

A piece of software for calling yourself
----------------------------------------

by Peter Hajas
--------------

Why would you call yourself? Well, here are just a few reasons:
- You are lonely. Very lonely.
- You like the sound of robot voices (this is the same as [1]).
- You need an excuse to get back to work.

Whatever your reasons may be, Elliot is here to help you!

Elliot is a simple interface to the service provided at fakecall.net. It supports:
 - Registering an account with fakecall.net
 - Calling your number
 - Deleting your account

To use Elliot, just run it with a command. Possible commands are:
 - call
 - delete

For example:

    `./Elliot.py call`

fakecall.net provides some security for these accounts through a password.

I'd rather not manage *another* password, but I respect the need for security.

For this, Elliot will create a password. It will save it, along with your number,
in a plaintext file in your user directory (`~/.elliot`). This is pretty ample
security for my usage of fakecall.net, but it might not be for you.

Elliot is licensed under the BSD license.
Please see the License file or the comment at the top of Elliot.py
