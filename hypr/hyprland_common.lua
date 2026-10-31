return function(options)
    local layout = options.layout
    local useScrolling = layout == "scrolling"
    local terminal = "ghostty"
    local fileManager = "yazi"
    local menu = "rofi -show combi"
    local mainMod = "SUPER"

    -- dorm-dev is the streamed remote desktop (docs/remote-dev.org).
    local hostFile = io.open("/etc/hostname")
    local hostname = hostFile and hostFile:read("l") or ""
    if hostFile then
        hostFile:close()
    end
    local remoteHost = hostname == "dorm-dev"

    hl.monitor({
        output = "",
        mode = "highres",
        position = "auto",
        scale = remoteHost and 1.6 or 2,
    })

    hl.env("XCURSOR_SIZE", "24")
    hl.env("XCURSOR_THEME", "Breeze_Dark")
    hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")
    hl.env("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
    hl.env("QT_IM_MODULE", "fcitx")
    hl.env("XMODIFIERS", "@im=fcitx")
    hl.env("SDL_IM_MODULE", "fcitx")

    hl.config({
        xwayland = {
            force_zero_scaling = true,
        },
        general = {
            gaps_in = 5,
            gaps_out = 10,
            border_size = 2,
            col = {
                active_border = "rgba(33ccffee)",
                inactive_border = "rgba(595959aa)",
            },
            resize_on_border = false,
            allow_tearing = false,
            layout = layout,
        },
        decoration = {
            rounding = 5,
            rounding_power = 2,
            active_opacity = 1.0,
            inactive_opacity = 1.0,
            shadow = {
                enabled = false,
                range = 4,
                render_power = 3,
                color = "rgba(1a1a1aee)",
            },
            blur = {
                enabled = false,
                size = 3,
                passes = 1,
                vibrancy = 0.1696,
            },
        },
        animations = {
            enabled = true,
        },
        master = {
            new_status = "master",
        },
        dwindle = layout == "dwindle" and {
            preserve_split = true,
        } or nil,
        scrolling = useScrolling and {
            fullscreen_on_one_column = false,
            column_width = 0.75,
            follow_min_visible = 0.75,
        } or nil,
        misc = {
            force_default_wallpaper = -1,
            focus_on_activate = true,
            disable_hyprland_logo = false,
            -- dorm-dev blanks its panel without Hypridle; wake it locally.
            key_press_enables_dpms = remoteHost,
            mouse_move_enables_dpms = remoteHost,
        },
        input = {
            kb_layout = "us",
            kb_variant = "",
            kb_model = "",
            kb_options = "caps:swapescape",
            kb_rules = "",
            follow_mouse = 1,
            sensitivity = 0,
            touchpad = {
                natural_scroll = true,
                tap_and_drag = true,
            },
        },
    })

    if useScrolling then
        hl.on("window.open_early", function(window)
            local workspace = window.workspace
            if not window.floating and workspace.tiled_layout == "scrolling" then
                hl.config({
                    scrolling = { column_width = workspace.windows == 0 and 1.0 or 0.75 },
                })
            end
        end)
    end

    hl.curve("easeOutQuint", { type = "bezier", points = { { 0.23, 1 }, { 0.32, 1 } } })
    hl.curve("easeInOutCubic", { type = "bezier", points = { { 0.65, 0.05 }, { 0.36, 1 } } })
    hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 1, 1 } } })
    hl.curve("almostLinear", { type = "bezier", points = { { 0.5, 0.5 }, { 0.75, 1.0 } } })
    hl.curve("quick", { type = "bezier", points = { { 0.15, 0 }, { 0.1, 1 } } })

    hl.animation({ leaf = "global", enabled = true, speed = 10, bezier = "default" })
    hl.animation({ leaf = "border", enabled = true, speed = 5.39, bezier = "easeOutQuint" })
    hl.animation({ leaf = "windows", enabled = true, speed = 4.79, bezier = "easeOutQuint" })
    hl.animation({ leaf = "windowsIn", enabled = true, speed = 4.1, bezier = "easeOutQuint", style = "popin 87%" })
    hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.49, bezier = "linear", style = "popin 87%" })
    hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.73, bezier = "almostLinear" })
    hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.46, bezier = "almostLinear" })
    hl.animation({ leaf = "fade", enabled = true, speed = 3.03, bezier = "quick" })
    hl.animation({ leaf = "layers", enabled = true, speed = 3.81, bezier = "easeOutQuint" })
    hl.animation({ leaf = "layersIn", enabled = true, speed = 4, bezier = "easeOutQuint", style = "fade" })
    hl.animation({ leaf = "layersOut", enabled = true, speed = 1.5, bezier = "linear", style = "fade" })
    hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 1.79, bezier = "almostLinear" })
    hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.39, bezier = "almostLinear" })
    hl.animation({ leaf = "workspaces", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })
    hl.animation({ leaf = "workspacesIn", enabled = true, speed = 1.21, bezier = "almostLinear", style = "fade" })
    hl.animation({ leaf = "workspacesOut", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })

    hl.workspace_rule({
        workspace = "special:magic",
        gaps_out = 130,
    })

    hl.window_rule({
        name = "fix-wechat",
        match = {
            class = "wechat",
            title = "negative:^(朋友圈|微信|设置|聊天文件|预览|图片和视频)\\W*",
        },
        no_blur = true,
        no_shadow = true,
        float = true,
        border_size = 0,
    })

    hl.window_rule({
        name = "fix-wechat-send",
        match = {
            class = "wechat",
            title = "^微信发送给$",
        },
        no_blur = true,
        no_shadow = true,
        border_size = 0,
    })

    hl.window_rule({
        name = "fix-wechat-picture-window",
        match = {
            class = "wechat",
            title = "^(图片和视频|朋友圈)$",
        },
        float = true,
        center = true,
    })

    hl.device({
        name = "epic-mouse-v1",
        sensitivity = -0.5,
    })

    if hl.plugin.hyprexpo then
        hl.config({
            plugin = {
                hyprexpo = {
                    columns = 3,
                    gap_size = 5,
                    bg_col = "rgb(111111)",
                    workspace_method = "center current",
                },
            },
        })
    end

    hl.bind(mainMod .. " + Return", hl.dsp.exec_cmd(terminal))
    hl.bind(mainMod .. " + SHIFT + Q", hl.dsp.window.close())
    hl.bind(mainMod .. " + SHIFT + E", hl.dsp.exit())
    hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
    hl.bind(mainMod .. " + SHIFT + Space", hl.dsp.window.float())
    hl.bind(mainMod .. " + F", hl.dsp.window.fullscreen())
    hl.bind(mainMod .. " + d", hl.dsp.exec_cmd(menu))
    hl.bind(mainMod .. " + space", hl.dsp.exec_cmd("~/dotfile/script/hypr-window-switcher.sh"))

    hl.bind(mainMod .. " + h", hl.dsp.focus({ direction = "l" }))
    hl.bind(mainMod .. " + l", hl.dsp.focus({ direction = "r" }))
    hl.bind(mainMod .. " + j", hl.dsp.focus({ direction = "d" }))
    hl.bind(mainMod .. " + k", hl.dsp.focus({ direction = "u" }))
    hl.bind(mainMod .. " + SHIFT + h", hl.dsp.window.move({ direction = "l" }))
    hl.bind(mainMod .. " + SHIFT + j", hl.dsp.window.move({ direction = "d" }))
    hl.bind(mainMod .. " + SHIFT + k", hl.dsp.window.move({ direction = "u" }))
    hl.bind(mainMod .. " + SHIFT + l", hl.dsp.window.move({ direction = "r" }))
    if useScrolling then
        hl.bind(mainMod .. " + W", hl.dsp.layout("colresize +conf"))
        hl.bind(mainMod .. " + SHIFT + W", hl.dsp.layout("colresize -conf"))
    else
        hl.bind(mainMod .. " + W", hl.dsp.group.toggle())
    end

    hl.bind(mainMod .. " + x", hl.dsp.focus({ last = true }))
    hl.bind(mainMod .. " + Tab", function()
        hl.dispatch(hl.dsp.group.next())
        hl.dispatch(hl.dsp.window.cycle_next({ next = true }))
        hl.dispatch(hl.dsp.window.bring_to_top())
    end)

    for workspace = 1, 10 do
        local key = workspace % 10
        hl.bind(mainMod .. " + " .. key, hl.dsp.focus({ workspace = workspace }))
        hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = workspace }))
    end

    hl.bind(mainMod .. " + minus", hl.dsp.workspace.toggle_special("magic"))
    hl.bind(mainMod .. " + SHIFT + minus", hl.dsp.window.move({ workspace = "special:magic" }))
    hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
    hl.bind(mainMod .. " + mouse_up", hl.dsp.focus({ workspace = "e-1" }))
    hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
    hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

    local repeatWhileLocked = { locked = true, repeating = true }
    hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"), repeatWhileLocked)
    hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), repeatWhileLocked)
    hl.bind("XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), repeatWhileLocked)
    hl.bind("XF86AudioMicMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), repeatWhileLocked)
    hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("brightnessctl s 10%+"), repeatWhileLocked)
    hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl s 10%-"), repeatWhileLocked)

    local whileLocked = { locked = true }
    hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), whileLocked)
    hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), whileLocked)
    hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), whileLocked)
    hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), whileLocked)

    hl.bind(mainMod .. " + V", hl.dsp.exec_cmd("copyq toggle"))
    hl.bind(mainMod .. " + T", hl.dsp.exec_cmd("/home/wste/code/Dayline/.venv/bin/dayline ui toggle-widget"))
    -- Dayline's panel lives on special:dayline; open it there if it is not mapped yet.
    hl.bind(mainMod .. " + A", function()
        if #hl.get_workspace_windows("special:dayline") == 0 then
            hl.exec_cmd("/home/wste/code/Dayline/.venv/bin/dayline ui show")
        else
            hl.dispatch(hl.dsp.workspace.toggle_special("dayline"))
        end
    end)
    hl.bind(mainMod .. " + N", hl.dsp.exec_cmd("swaync-client --toggle-panel"))
    hl.bind("Print", hl.dsp.exec_cmd("sh -c 'if pgrep -x slurp; then pkill slurp; else slurp | grim -g - - | wl-copy; fi'"))
    hl.bind(mainMod .. " + SHIFT + escape", hl.dsp.exec_cmd("hyprlock"))
    hl.bind(mainMod .. " + SHIFT + I", hl.dsp.exec_cmd("~/dotfile/script/toggle-inhibit-lid-sleep.sh"))
    hl.bind(mainMod .. " + I", hl.dsp.exec_cmd("~/dotfile/script/toggle-inhibit.sh idle"))
    hl.bind(mainMod .. " + P", hl.dsp.exec_cmd("hyprctl activewindow | wl-copy"))

    hl.window_rule({
        match = { class = ".*copyq.*" },
        float = true,
        size = "500 600",
        move = "985 385",
    })
    hl.window_rule({
        match = { title = ".*Photos and Videos.*" },
        float = true,
        size = "1000 800",
        center = true,
    })
    hl.window_rule({
        match = { title = ".*Volume Control.*" },
        float = true,
        size = "45% 35%",
        center = true,
    })
    hl.window_rule({
        match = { float = true },
        persistent_size = true,
        max_size = "1300 800",
    })
    hl.window_rule({
        name = "dayline-special-workspace",
        match = { class = "^io\\.github\\.wusitee\\.Dayline$" },
        workspace = "special:dayline",
    })
    hl.window_rule({
        name = "special-workspace-rule",
        match = {
            class = "negative:(com.mitchellh.ghostty|GTK Application|hyprpolkitagent|com.github.hluk.copyq)",
            workspace = "special:magic",
        },
        workspace = "+0",
    })

    if useScrolling then
        hl.gesture({
            fingers = 3,
            direction = "horizontal",
            action = "workspace",
        })
        hl.gesture({
            fingers = 3,
            direction = "vertical",
            action = "scroll_move",
        })
    else
        hl.gesture({
            fingers = 3,
            direction = "horizontal",
            action = "workspace",
        })
    end

    hl.on("hyprland.start", function()
        if remoteHost and os.getenv("DORM_DEV_AUTOLOGIN") then
            -- greetd's boot-time auto-login: lock, then blank the panel until a
            -- stream starts.
            hl.exec_cmd("hyprlock")
            hl.exec_cmd([[sh -c 'sleep 5; hyprctl dispatch "hl.dsp.dpms({action = \"off\"})"']])
        end
        hl.exec_cmd(terminal)
        hl.exec_cmd(remoteHost and "nm-applet" or "nm-applet & matebook-applet")
        hl.exec_cmd("waybar")
        hl.exec_cmd("systemctl --user start hyprpolkitagent")
        hl.exec_cmd("fcitx5 -d")
        hl.exec_cmd("copyq --start-server")
        hl.exec_cmd("awww-daemon")
        hl.exec_cmd(remoteHost and "hypridle -c ~/.config/hypr/hypridle-remote.conf" or "hypridle")
        hl.exec_cmd("swaync")
        if remoteHost then
            -- Restart: with lingering, Sunshine outlives a session and would
            -- keep the previous HYPRLAND_INSTANCE_SIGNATURE.
            hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP HYPRLAND_INSTANCE_SIGNATURE && systemctl --user restart app-dev.lizardbyte.app.Sunshine.service")
        else
            hl.exec_cmd("/home/wste/code/Dayline/.venv/bin/dayline ui")
            hl.exec_cmd("gammastep")
            hl.exec_cmd("onedrive --monitor")
        end
        hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
        hl.exec_cmd("hyprctl setcursor \"Breeze Dark\" 24")
        hl.exec_cmd("xrdb ~/.Xresources")
    end)

    hl.on("config.reloaded", function()
        hl.exec_cmd("xrdb ~/.Xresources")
    end)
end
