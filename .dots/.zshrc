export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="xiong-chiamiov-plus"

plugins=(
    git
    sudo
    web-search
    python
    pip
    history-substring-search
    colored-man-pages
    zsh-autosuggestions
    zsh-syntax-highlighting
    archlinux
    eza
)

source $ZSH/oh-my-zsh.sh

pokemon-colorscripts --no-title -s -r
source <(fzf --zsh)
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt appendhistory

alias p="python3"
alias j='jsonVer(){ cat "$@" | jq; unset -f jsonVer; }; jsonVer'
alias ara='ara(){ find / -type f -name "$@" -print 2>/dev/null }; ara'
alias md2pdf='md2pdf(){ pandoc -o "${@%%.*}.pdf" --template pdf_theme --listings --pdf-engine=xelatex --toc "$@"; unset -f md2pdf; }; md2pdf'

# alias ipv4="nmcli device show | grep IP4.ADDRESS | head -1 | awk '{print $2}' | rev | cut -c 4- | rev"
alias ipv4="nmcli device show | awk '/IP4.ADDRESS/{print \$2}' | cut -d'/' -f1 | head -1"

# alias ipv6="nmcli device show | grep IP6.ADDRESS | head -1 | awk '{print $2}' | rev | cut -c 4- | rev"
alias ipv6="nmcli device show | awk '/IP6.ADDRESS/{print \$2}' | cut -d'/' -f1 | head -1"

# xinput --set-prop "Elan TrackPoint" "libinput Accel Speed" -0.7
alias yt='yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio" --merge-output-format mp4'
alias mp3="yt-dlp -x --embed-thumbnail --audio-format mp3"

# * mkv2mp4
alias mkv2mp4='mkv2mp4(){ ffmpeg -v quiet -stats -i "$@" -c copy -c:a aac -movflags +faststart "${@%%.*}.mp4" }; mkv2mp4'

# * GPG_KEY
export GPG_TTY=$(tty)

# * TR dil ayarları
export LC_ALL=tr_TR.UTF-8
export LANG=tr_TR.UTF-8

# Update zshrc
alias zrc='source ~/.zshrc'

# Directory navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias c='clear'

# List directory contents
alias ls='eza -al --color=always --group-directories-first --icons' # preferred listing
alias la='eza -a --color=always --group-directories-first --icons'  # all files and dirs
alias ll='eza -l --color=always --group-directories-first --icons'  # long format
alias lt='eza -aT --color=always --group-directories-first --icons' # tree listing
alias l.="eza -a | grep -e '^\.'"                                     # show only dotfiles

# File operations
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'
alias mkdir='mkdir -pv'

# Grep
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Network
alias wget='wget -c'
alias curl='curl -O -L -C - -#'
alias myip='wget -qO- ifconfig.io/ip ; echo'

# System info
alias df='df -h'
alias du='du -ch'
alias free='free -m'
alias top='btop'
alias psu='ps -U $USER -u $USER u'

# Disk usage
alias usage='du -ch --max-depth=1'

# Git
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m "☠"'
alias gp='git push -u origin main'
alias gl='git pull'
alias gco='git checkout'
alias gb='git branch'
alias gd='git diff'
alias gcl='git clone --depth 1'

# Archive operations
alias tarc='tar -czvf'
alias tarx='tar -xzvf'
alias tarl='tar -tzvf'
alias zipc='zip -r'
alias unzipc='unzip'
alias gz='gzip'
alias gunz='gunzip'
alias bz2='bzip2'
alias bunz2='bunzip2'

# Misc
alias h='history'
alias js='jobs -l'
alias path='echo -e ${PATH//:/\\n}'
alias now='date +"%T"'
alias nowdate='date +"%d-%m-%Y"'
alias week='date +"%V"'

# Safety
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
alias rm='rm -I --preserve-root'
alias shred='shred -u -v -n 35 -z'
alias sudo='run0 --background=44 --nice=10 --unit=sudounit'

# Make 'cd' also list directory contents
function cd() {
    builtin cd "$@" && ls
}

# Reload the .zshrc file
alias reload='source ~/.zshrc'

# Add custom PATH
export PATH="$HOME/bin:$PATH"

# Enable completions
autoload -U compinit
compinit

# Enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Load zsh-syntax-highlighting if installed
if [ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# Load zsh-autosuggestions if installed
if [ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
fi
