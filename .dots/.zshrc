export ZSH="$HOME/.oh-my-zsh"

#ZSH_THEME="agnoster"

eval "$(starship init zsh)"

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
)

source $ZSH/oh-my-zsh.sh



alias p="python3"
alias c="clear"
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
