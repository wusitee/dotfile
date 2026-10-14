function t3 --wraps t3 --description 'Check Clash TUN, Global mode and Taiwan selection before running T3'
    command /home/wste/dotfile/script/clash-network-check.fish
    or return 1
    if test (count $argv) -eq 1; and test "$argv[1]" = --proxy-check
        return 0
    end

    command t3 $argv
end
