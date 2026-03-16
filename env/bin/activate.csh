# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
<<<<<<< HEAD

# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; unsetenv VIRTUAL_ENV_PROMPT; test "\!:*" != "nondestructive" && unalias deactivate'
=======
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; test "\!:*" != "nondestructive" && unalias deactivate'
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
setenv VIRTUAL_ENV /home/israel/Documents/oyeo-final/env

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/"bin":$PATH"
=======
setenv VIRTUAL_ENV "/Users/borisbab/Documents/Projet-oyéo/oyeo-ecommerce/env"

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
<<<<<<< HEAD
    set prompt = '(env) '"$prompt"
    setenv VIRTUAL_ENV_PROMPT '(env) '
=======
    set prompt = "(env) $prompt"
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2
endif

alias pydoc python -m pydoc

rehash
