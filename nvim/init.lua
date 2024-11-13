-- bootstrap lazy.nvim, LazyVim and your plugins
if vim.g.vscode then
else
  require("config.lazy")
end
