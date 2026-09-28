-- Record every directory Yazi enters in zoxide's database, so `Z` jumps
-- (and plain navigation) keep frecency rankings up to date.
require("zoxide"):setup {
	update_db = true,
}
