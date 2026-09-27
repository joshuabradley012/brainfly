#!/usr/bin/env bash
# Benchmark Hetzner server types side by side on the current brain: one box per type in TYPES, each
# brought up to date (x86 from the newest snapshot; arm from plain Ubuntu, installing and uploading
# ~/fly-data, which takes ~15 min), then scripts/remote/bench_current.py with THREADS numba threads
# (default: the box's vCPUs). Prints each box's trial-seconds per wall second; the boxes are deleted
# however it ends. Keep the sum of vCPUs within the account's quota (20).
#
#   TYPES="cx33 cpx32 cax21" scripts/remote/compare.sh      (a type@location, e.g. cax21@hel1, picks its location)
set -euo pipefail
cd "$(dirname "$0")/../.."
source scripts/remote/common.sh
read -r -a types <<< "${TYPES:-cx33 cpx32 cax21}"
LOCATION=${LOCATION:-fsn1}
IMAGE=$(hcloud image list --type snapshot -l brainfly-image=1 -o noheader -o columns=id,created | sort -k2 | tail -1 | awk '{print $1}')
names=()
finish() { for n in "${names[@]}"; do hcloud server delete "$n" >/dev/null 2>&1 && echo "server $n deleted"; done; }
trap finish EXIT
ensure_key
write_cloud_init /tmp/brainfly-cloud-init.yml
for tl in "${types[@]}"; do
  t=${tl%@*}; loc=$LOCATION; [ "$tl" != "$t" ] && loc=${tl#*@}
  n="brainfly-bench-$t"; names+=("$n")
  arch=$(hcloud server-type describe "$t" -o 'format={{.Architecture}}')
  if [ "$arch" = arm ] || [ -z "$IMAGE" ]; then img=(--image ubuntu-24.04 --user-data-from-file /tmp/brainfly-cloud-init.yml); else img=(--image "$IMAGE"); fi
  hcloud server create --name "$n" --type "$t" --location "$loc" "${img[@]}" --ssh-key "$KEY_NAME" --label brainfly=1 --label pool=bench >/dev/null &
done
wait
bench() {
  local n=$1 ip cores
  ip=$(hcloud server ip "$n"); cores=$(hcloud server describe "$n" -o 'format={{.ServerType.Cores}}')
  wait_ready "$ip" && sync_tree "$ip" && sync_data "$ip" && install "$ip" || { echo "$n: setup failed"; return; }
  $SSH@"$ip" "cd /root/brainfly && FLY_DATA=/root/fly-data NUMBA_NUM_THREADS=${THREADS:-$cores} /root/venv/bin/python scripts/remote/bench_current.py 2>&1 | grep -v -i warn | tail -5" | sed "s/^/$n: /"
}
for n in "${names[@]}"; do bench "$n" & done
wait
