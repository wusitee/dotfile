
#set the color

# enable z
# Invoke-Expression (& { (lua C:/Users/Simon/Scoop/apps/z.lua/current/z.lua --init powershell enhanced) -join "`n" })

Import-Module posh-git
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\robbyrussell.omp.json" | Invoke-Expression
# Invoke-Expression (&starship init powershell)


Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete

Set-PSReadlineKeyHandler -Key "Ctrl+d" -Function ViExit

Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo

# 1. 编译函数 make
function MakeThings {
	nmake.exe $args -nologo
}
Set-Alias -Name make -Value MakeThings

# Set-Alias -Name os-update -Value Update-Packages

# 3. 查看目录 ls & ll
function ListDirectory {
	(Get-ChildItem).Name
	Write-Host("")
}
# Set-Alias -Name ls -Value ListDirectory
Set-Alias -Name ll -Value Get-ChildItem

# remove the powershell ls in order to use the ls from busy-box
Remove-Alias -Name ls
Remove-Alias -Name rm
Remove-Alias -Name mv

# # remove the alias of man in order to use the man from busy-box
# Remove-Alias -Name man

function OpenCurrentFolder {
	param
	(
		$Path = '.'
	)
	Invoke-Item $Path
}
Set-Alias -Name open -Value OpenCurrentFolder
# Set-Alias -Name pip -Value pip3

# 使用自动补全
Import-Module Az.Tools.Predictor
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineKeyHandler -Chord "Ctrl+f" -Function ForwardWord
# use zoxide for autojummp
Invoke-Expression (& { (zoxide init powershell | Out-String) })
