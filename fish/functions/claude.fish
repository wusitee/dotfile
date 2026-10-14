function claude --wraps claude --description 'Check Clash TUN, Global mode and Taiwan selection before starting Claude'
    command /home/wste/dotfile/script/clash-network-check.fish
    or return 1
    if test (count $argv) -eq 1; and test "$argv[1]" = --proxy-check
        return 0
    end

    command claude $argv
end
