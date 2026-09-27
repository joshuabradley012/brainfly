# Shared by image.sh and run.sh (sourced from the repository root): ssh options, the cloud-init that
# readies a plain Ubuntu box, and the steps that bring a box up to date with this tree.

KEY_NAME=${KEY_NAME:-$(whoami)-lab}
# Throwaway boxes get recycled IPs, so host keys are neither pinned nor remembered.
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes -o ServerAliveInterval=30"
SSH="ssh $SSH_OPTS -o ConnectTimeout=10 root"
RSYNC_SSH="ssh $SSH_OPTS"
FLY_DATA_LOCAL=${FLY_DATA:-$HOME/fly-data}

ensure_key() {
  hcloud ssh-key describe "$KEY_NAME" >/dev/null 2>&1 \
    || hcloud ssh-key create --name "$KEY_NAME" --public-key-from-file ~/.ssh/id_ed25519.pub >/dev/null
}

# A plain ubuntu-24.04 box: rsync, a compiler (brian2's tests build C++), uv. Snapshots keep
# /root/.lab-ready, so the same readiness probe works for boxes made from one.
write_cloud_init() {
  cat > "$1" <<'CI'
#cloud-config
package_update: true
packages: [rsync, build-essential]
runcmd:
  - curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
  - touch /root/.lab-ready
CI
}

# wait_ready IP: until cloud-init is done, at most 20 minutes (an endless wait outlived its boxes in
# openfront's lab, and then acted on new boxes that were given the same IP).
wait_ready() {
  local tries=0
  until $SSH@"$1" test -f /root/.lab-ready 2>/dev/null; do
    tries=$((tries + 1))
    [ "$tries" -ge 240 ] && { echo "ERROR: $1 not ready after 20 min"; return 1; }
    sleep 5
  done
}

# sync_tree IP: the sources, tests and experiments (a few MB; not .venv, .git or caches).
sync_tree() {
  rsync -az --delete -e "$RSYNC_SSH" \
    --exclude .venv --exclude .git --exclude __pycache__ --exclude '*.egg-info' --exclude .pytest_cache \
    --exclude remote-out --exclude .claude --exclude '*.log' \
    ./ root@"$1":/root/brainfly/
}

# sync_data IP: ~/fly-data as experiments read it. Not the raw archives that only building needs
# (MaleCNS's 3.7 GB roi_elements.feather, Turner et al.'s tarball: their products, region_weights.npz
# and turner2021/, go instead) nor the 1 GB connectome table, which install() has the box fetch from
# MaleCNS's bucket, much faster than an upload from here. Nothing on the box is deleted.
sync_data() {
  rsync -az -e "$RSYNC_SSH" \
    --exclude raw/roi_elements.feather --exclude raw/data_TurnerMannClandinin.tar.gz \
    --exclude raw/connectome-weights-male-cns-v1.0-minconf-0.5.feather --exclude '*.part' \
    "$FLY_DATA_LOCAL"/ root@"$1":/root/fly-data/
}

# install IP: brainfly and all its extras but the GPU one into /root/venv, only when pyproject.toml
# changed since the last install there (torch from its CPU-only index: the default Linux wheel pulls
# in ~3 GB of CUDA), then any MaleCNS source file the box lacks.
install() {
  $SSH@"$1" 'set -e; cd /root/brainfly; h=$(sha256sum pyproject.toml | cut -c1-16)
    if [ ! -f /root/venv/.pyproject-$h ]; then
      [ -d /root/venv ] || uv venv -q /root/venv --python 3.12
      export VIRTUAL_ENV=/root/venv
      uv pip install -q torch --index-url https://download.pytorch.org/whl/cpu
      uv pip install -q -e ".[flyvis,body,build,test]"
      rm -f /root/venv/.pyproject-*; touch /root/venv/.pyproject-$h
    fi
    FLY_DATA=/root/fly-data /root/venv/bin/python -c "from brainfly.build import download_all; from brainfly.data import DATA; download_all(DATA / \"raw\")" >/dev/null'
}
