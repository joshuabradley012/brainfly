#!/usr/bin/env bash
# Bake the Hetzner snapshot that run.sh boots boxes from: Python 3.12 with brainfly and its extras
# (torch CPU-only), the MaleCNS source tables and the data experiments read from ~/fly-data, so a
# box is working about a minute after it's created instead of after ~5 minutes of installing and
# uploading. run.sh picks the newest snapshot labelled brainfly-image=1, and brings a box up to date
# itself (it re-installs when pyproject.toml differs and syncs ~/fly-data), so a stale snapshot only
# costs minutes. Snapshots cost about €0.01 per GB a month; old ones:
#   hcloud image list --type snapshot -l brainfly-image=1;  hcloud image delete <id>
#
#   scripts/remote/image.sh            # env: SERVER_TYPE (cpx22), LOCATION (fsn1), KEY_NAME
set -euo pipefail
cd "$(dirname "$0")/../.."
source scripts/remote/common.sh
SERVER_TYPE=${SERVER_TYPE:-cpx22}
LOCATION=${LOCATION:-fsn1}
NAME=brainfly-image-builder

ensure_key
write_cloud_init /tmp/brainfly-cloud-init.yml
echo "creating $NAME ($SERVER_TYPE, $LOCATION) ..."
hcloud server create --name "$NAME" --type "$SERVER_TYPE" --image ubuntu-24.04 --location "$LOCATION" \
  --ssh-key "$KEY_NAME" --label brainfly=1 --user-data-from-file /tmp/brainfly-cloud-init.yml >/dev/null
# The builder is deleted however the script ends.
trap 'hcloud server delete "$NAME" >/dev/null 2>&1 && echo "builder $NAME deleted"' EXIT
IP=$(hcloud server ip "$NAME")
wait_ready "$IP"
t=$SECONDS; sync_tree "$IP"; sync_data "$IP"; echo "uploaded tree and data in $((SECONDS - t)) s"
t=$SECONDS; install "$IP"; echo "installed in $((SECONDS - t)) s"
$SSH@"$IP" 'rm -f /root/.ssh/known_hosts && sync'
hcloud server shutdown "$NAME" >/dev/null
until [ "$(hcloud server describe "$NAME" -o 'format={{.Status}}')" = off ]; do sleep 3; done
echo "creating snapshot ..."
out=$(hcloud server create-image --type snapshot --description "brainfly-lab $(date +%Y-%m-%d) $(git rev-parse --short HEAD)" \
  --label brainfly-image=1 "$NAME")
IMG=$(echo "$out" | grep -oE '(Image|image:) *[0-9]+' | grep -oE '[0-9]+' | head -1 || true)
[ -n "$IMG" ] || IMG=$(hcloud image list --type snapshot -l brainfly-image=1 -o noheader -o columns=id,created | sort -k2 | tail -1 | awk '{print $1}')
echo "snapshot $IMG ready; run.sh uses it (IMAGE=auto)"
