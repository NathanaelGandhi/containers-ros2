if [[ ! "$(id -un)" == 'root' ]] && [[ -n "$(id -g)" ]] && [[ -n "$(id -u)" ]]; then

    grep "^$(id -g)" < /etc/group || sudo addgroup --gid "$(id -g)" "$(id -un)"
    id -nG "$(id -g)" || sudo adduser --system --uid "$(id -u)" --gid "$(id -g)"  --disabled-password  "$(id -un)" --no-create-home

    sudo usermod -s /bin/bash "$(id -un)"
    sudo usermod -aG sudo "$(id -un)"
    echo "$(id -un) ALL=(ALL) NOPASSWD:ALL" | sudo tee "/etc/sudoers.d/$(id -un)" > /dev/null
    export HOME="/home/$(id -un)"
    sudo ln -s /root "$HOME"
    echo "Running as $(id -un) ($(id -u):$(id -g)) : bash"

    sudo -E -s -u  "$(id -un)" /bin/bash -c "cd \"/mnt/host\" 2>/dev/null || cd ~ ; bash"
else
    echo "--user='$(id -u)':'$(id -g)'='$(id -un)'"
    echo "cmd: 'bash'"
    echo "Running as ${USER:-root}: bash"
    bash
fi
