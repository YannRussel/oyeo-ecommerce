# This file must be used with "source <venv>/bin/activate.fish" *from fish*
<<<<<<< HEAD
# (https://fishshell.com/). You cannot run it directly.
=======
# (https://fishshell.com/); you cannot run it directly.
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2

function deactivate  -d "Exit virtual environment and return to normal shell environment"
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME $_OLD_VIRTUAL_PYTHONHOME
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
<<<<<<< HEAD
        set -e _OLD_FISH_PROMPT_OVERRIDE
        # prevents error when using nested fish instances (Issue #93858)
        if functions -q _old_fish_prompt
            functions -e fish_prompt
            functions -c _old_fish_prompt fish_prompt
            functions -e _old_fish_prompt
        end
    end

    set -e VIRTUAL_ENV
    set -e VIRTUAL_ENV_PROMPT
=======
        functions -e fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
    end

    set -e VIRTUAL_ENV
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2
    if test "$argv[1]" != "nondestructive"
        # Self-destruct!
        functions -e deactivate
    end
end

# Unset irrelevant variables.
deactivate nondestructive

<<<<<<< HEAD
set -gx VIRTUAL_ENV /home/israel/Documents/oyeo-final/env

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/"bin $PATH
=======
set -gx VIRTUAL_ENV "/Users/borisbab/Documents/Projet-oyéo/oyeo-ecommerce/env"

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2

# Unset PYTHONHOME if set.
if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # fish uses a function instead of an env var to generate the prompt.

    # Save the current fish_prompt function as the function _old_fish_prompt.
    functions -c fish_prompt _old_fish_prompt

    # With the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command.
        set -l old_status $status

        # Output the venv prompt; color taken from the blue of the Python logo.
<<<<<<< HEAD
        printf "%s%s%s" (set_color 4B8BBE) '(env) ' (set_color normal)
=======
        printf "%s%s%s" (set_color 4B8BBE) "(env) " (set_color normal)
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        # Output the original/"old" prompt.
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
<<<<<<< HEAD
    set -gx VIRTUAL_ENV_PROMPT '(env) '
=======
>>>>>>> 589caa82c75f1fcc38df9e82660516420c1d66d2
end
