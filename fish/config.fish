if status is-interactive
    # Commands to run in interactive sessions can go here
end
zoxide init fish | source
# kubectl completion fish | source

# Created by `pipx` on 2024-07-02 19:18:57
set PATH $PATH /home/wste/.local/bin

# init pyenv
# pyenv init - | source
# status --is-interactive; and pyenv virtualenv-init - | source
alias ff=fastfetch
function y
	set tmp (mktemp -t "yazi-cwd.XXXXXX")
	yazi $argv --cwd-file="$tmp"
	if set cwd (command cat -- "$tmp"); and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
		builtin cd -- "$cwd"
	end
	rm -f -- "$tmp"
end

starship init fish | source
direnv hook fish | source
