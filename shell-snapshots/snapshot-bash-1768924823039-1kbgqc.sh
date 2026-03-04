# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
# Shell Options
shopt -u autocd
shopt -u assoc_expand_once
shopt -u cdable_vars
shopt -u cdspell
shopt -u checkhash
shopt -u checkjobs
shopt -s checkwinsize
shopt -s cmdhist
shopt -u compat31
shopt -u compat32
shopt -u compat40
shopt -u compat41
shopt -u compat42
shopt -u compat43
shopt -u compat44
shopt -s complete_fullquote
shopt -u direxpand
shopt -u dirspell
shopt -u dotglob
shopt -u execfail
shopt -u expand_aliases
shopt -u extdebug
shopt -u extglob
shopt -s extquote
shopt -u failglob
shopt -s force_fignore
shopt -s globasciiranges
shopt -s globskipdots
shopt -u globstar
shopt -u gnu_errfmt
shopt -u histappend
shopt -u histreedit
shopt -u histverify
shopt -s hostcomplete
shopt -u huponexit
shopt -u inherit_errexit
shopt -s interactive_comments
shopt -u lastpipe
shopt -u lithist
shopt -u localvar_inherit
shopt -u localvar_unset
shopt -s login_shell
shopt -u mailwarn
shopt -u no_empty_cmd_completion
shopt -u nocaseglob
shopt -u nocasematch
shopt -u noexpand_translation
shopt -u nullglob
shopt -s patsub_replacement
shopt -s progcomp
shopt -u progcomp_alias
shopt -s promptvars
shopt -u restricted_shell
shopt -u shift_verbose
shopt -s sourcepath
shopt -u varredir_close
shopt -u xpg_echo
set -o braceexpand
set -o hashall
set -o interactive-comments
set -o monitor
set -o onecmd
shopt -s expand_aliases
# Aliases
# Check for rg availability
if ! command -v rg >/dev/null 2>&1; then
  alias rg='/home/philiptran/.npm-cache/_npx/11f72de11dbee700/node_modules/\@anthropic-ai/claude-code/vendor/ripgrep/x64-linux/rg'
fi
export PATH=/home/philiptran/.npm-cache/_npx/11f72de11dbee700/node_modules/.bin\:/home/philiptran/.vibe-kanban/worktrees/261a-hi/00_slide_proposal/node_modules/.bin\:/home/philiptran/.vibe-kanban/worktrees/261a-hi/node_modules/.bin\:/home/philiptran/.vibe-kanban/worktrees/node_modules/.bin\:/home/philiptran/.vibe-kanban/node_modules/.bin\:/home/philiptran/node_modules/.bin\:/home/node_modules/.bin\:/node_modules/.bin\:/home/philiptran/.nvm/versions/node/v20.20.0/lib/node_modules/npm/node_modules/\@npmcli/run-script/lib/node-gyp-bin\:/home/philiptran/.local/bin\:/home/philiptran/miniconda3/bin\:/home/philiptran/miniconda3/condabin\:/home/philiptran/.nvm/versions/node/v20.20.0/bin\:/home/philiptran/.npm-global/bin\:/home/philiptran/.cargo/bin\:/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/usr/games\:/usr/local/games\:/snap/bin
