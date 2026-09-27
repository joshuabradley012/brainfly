#!/usr/bin/env bash
# Run a list of brainfly jobs on throwaway Hetzner Cloud boxes and bring the results home. Each line
# of JOBS is a shell command run from the repository root with the box's Python first on PATH, e.g.
#   python experiments/rest_fc.py
# (blank lines and lines starting with # are skipped). The boxes pull the jobs, in the file's order,
# from one queue on the first box, SLOTS at a time each, every job with THREADS numba threads:
# HybridBrain runs its trials in parallel, so THREADS = the number of trials suits it. Jobs must write
# distinct files. When every job has ended, the files the jobs changed under experiments/ are copied
# into this tree (never over a newer local file), their logs go to DEST, and the boxes are deleted.
# The boxes are deleted on any exit but a SIGKILL, results pulled first where the boxes still answer.
#
#   JOBS=jobs.txt SERVER_TYPES="cpx62 cpx32" scripts/remote/run.sh
#
# Env: JOBS (required), SERVER_TYPES (one box per word; default WORKERS (1) boxes of SERVER_TYPE
# (cpx62: 16 shared vCPU at €0.25 an hour). The account allows 20 vCPU in all, e.g. cpx62 + cpx32 at
# €0.31 an hour, and 4 IPv4 addresses, so at most 4 boxes), LOCATION (fsn1), NAME (brainfly-lab;
# NAME-1..N for several boxes), IMAGE (auto = the newest snapshot from image.sh, none = plain
# ubuntu-24.04, ~15 min slower with the upload, or a snapshot id), THREADS (8), SLOTS (a box's vCPUs /
# THREADS, at least 1),
# DEST (./remote-out), MAX_HOURS (8: then pull what there is and stop), KEEP=1 to leave the boxes
# running, REUSE=1 to use running boxes with those names. Needs the hcloud CLI with a context
# selected, ~/.ssh/id_ed25519(.pub) and rsync.
#
# Every box carries the labels brainfly=1,pool=NAME:  hcloud server list -l brainfly=1  shows strays;
#   hcloud server delete $(hcloud server list -l brainfly=1 -o noheader -o columns=name)  removes them.
set -euo pipefail
cd "$(dirname "$0")/../.."
source scripts/remote/common.sh
: "${JOBS:?set JOBS to a file of commands, one per line}"
WORKERS=${WORKERS:-1}
SERVER_TYPE=${SERVER_TYPE:-cpx62}
if [ -n "${SERVER_TYPES:-}" ]; then read -r -a types <<< "$SERVER_TYPES"
else types=(); for _ in $(seq 1 "$WORKERS"); do types+=("$SERVER_TYPE"); done; fi
LOCATION=${LOCATION:-fsn1}
NAME=${NAME:-brainfly-lab}
IMAGE=${IMAGE:-auto}
THREADS=${THREADS:-8}
DEST=${DEST:-$PWD/remote-out}
MAX_HOURS=${MAX_HOURS:-8}
TIMEOUT=$(command -v timeout >/dev/null && echo "timeout 60" || true)

queue=$(mktemp)
grep -v -e '^[[:space:]]*$' -e '^[[:space:]]*#' "$JOBS" | awk '{printf "%d\t%s\n", NR, $0}' > "$queue"
njobs=$(wc -l < "$queue" | tr -d ' ')
[ "$njobs" -gt 0 ] || { echo "no jobs in $JOBS"; exit 1; }
declare -a names=() slots=() ips=()
for i in "${!types[@]}"; do
  if [ "${#types[@]}" -eq 1 ]; then names+=("$NAME"); else names+=("$NAME-$((i + 1))"); fi
  vcpus=$(hcloud server-type describe "${types[$i]}" -o 'format={{.Cores}}')
  slots+=("${SLOTS:-$(( vcpus / THREADS > 0 ? vcpus / THREADS : 1 ))}")
done

pull() {
  local i=0 ip
  mkdir -p "$DEST"
  for ip in "${ips[@]}"; do
    rsync -az -e "$RSYNC_SSH" --exclude 'queue*' root@"$ip":/root/remote-out/ "$DEST/${names[$i]}/" || true
    rsync -azu -e "$RSYNC_SSH" --exclude __pycache__ root@"$ip":/root/brainfly/experiments/ experiments/ || true
    i=$((i + 1))
  done
  cat "$DEST"/*/status.log 2>/dev/null | sort -k2n > "$DEST/status.log" || true
}
finish() {
  local rc=$?
  trap - EXIT INT TERM HUP
  if [ "${pulled:-0}" = 0 ] && [ "${launched:-0}" = 1 ]; then echo "pulling what there is ..."; pull; fi
  if [ "${KEEP:-0}" = 1 ]; then echo "servers kept: ${names[*]} (${ips[*]}); delete with: hcloud server delete ${names[*]}"
  else for n in "${names[@]}"; do hcloud server delete "$n" >/dev/null 2>&1 && echo "server $n deleted"; done; fi
  rm -f "$queue"
  exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT TERM HUP

ensure_key
if [ "$IMAGE" = auto ]; then
  IMAGE=$(hcloud image list --type snapshot -l brainfly-image=1 -o noheader -o columns=id,created | sort -k2 | tail -1 | awk '{print $1}')
  [ -n "$IMAGE" ] || IMAGE=none
fi
if [ "${REUSE:-0}" = 1 ]; then
  for n in "${names[@]}"; do ips+=("$(hcloud server ip "$n")"); done
  echo "reusing ${names[*]} (${ips[*]})"
else
  write_cloud_init /tmp/brainfly-cloud-init.yml
  base=(--image "$IMAGE"); [ "$IMAGE" = none ] && base=(--image ubuntu-24.04 --user-data-from-file /tmp/brainfly-cloud-init.yml)
  echo "creating ${types[*]} in $LOCATION from ${IMAGE/none/ubuntu-24.04} ..."
  for i in "${!names[@]}"; do
    hcloud server create --name "${names[$i]}" --type "${types[$i]}" --location "$LOCATION" "${base[@]}" \
      --ssh-key "$KEY_NAME" --label brainfly=1 --label "pool=$NAME" >/dev/null &
  done
  wait
  for n in "${names[@]}"; do
    hcloud server describe "$n" >/dev/null 2>&1 || { echo "server $n was not created (see the errors above)"; exit 1; }
    ips+=("$(hcloud server ip "$n")")
  done
  echo "servers: ${names[*]} at ${ips[*]}; waiting for them to boot ..."
  for ip in "${ips[@]}"; do wait_ready "$ip"; done
fi

t=$SECONDS
echo "syncing the tree and ~/fly-data, installing where pyproject.toml changed ..."
for ip in "${ips[@]}"; do (sync_tree "$ip" && sync_data "$ip" && install "$ip") & done
for job in $(jobs -p); do wait "$job" || { echo "ERROR: a box failed to sync or install"; exit 1; }; done
echo "  ready in $((SECONDS - t)) s"

# One queue for the pool, on the first box: the others claim from it over ssh with a throwaway key.
QUEUE_HOST=${ips[0]}
for ip in "${ips[@]}"; do $SSH@"$ip" 'rm -rf /root/remote-out && mkdir -p /root/remote-out' & done; wait
rsync -az -e "$RSYNC_SSH" "$queue" root@"$QUEUE_HOST":/root/remote-out/queue.txt
if [ "${#ips[@]}" -gt 1 ]; then
  qkey=$(mktemp -d)/queue
  ssh-keygen -q -t ed25519 -N "" -f "$qkey"
  for ip in "${ips[@]}"; do rsync -az -e "$RSYNC_SSH" "$qkey" root@"$ip":/root/.ssh/queue & done; wait
  $SSH@"$QUEUE_HOST" "cat >> /root/.ssh/authorized_keys && mkdir -p /etc/ssh/sshd_config.d && printf 'MaxStartups 100\n' > /etc/ssh/sshd_config.d/90-lab.conf && (systemctl reload ssh || true)" < "$qkey.pub"
  for ip in "${ips[@]}"; do $SSH@"$ip" 'chmod 600 /root/.ssh/queue' & done; wait
  rm -rf "$(dirname "$qkey")"
fi

# Detached (setsid nohup, in a subshell), so a dropped connection or a killed launcher can't stop a job.
echo "running $njobs job(s) on ${#ips[@]} box(es), (${slots[*]}) at a time, $THREADS threads per job ..."
for i in "${!ips[@]}"; do
  ip=${ips[$i]}; q=local; [ "$ip" = "$QUEUE_HOST" ] || q=$QUEUE_HOST
  $TIMEOUT $SSH@"$ip" "cd /root/brainfly && for s in \$(seq 1 ${slots[$i]}); do (setsid nohup env QUEUE=$q THREADS=$THREADS bash scripts/remote/worker.sh > /root/remote-out/worker-\$s.log 2>&1 < /dev/null &); done" \
    || echo "WARNING: the launch on $ip didn't confirm"
done
launched=1
sleep 5

running() {    # 0: a worker is still running somewhere; 1: none is; 2: a box didn't answer
  local ip out rc=1
  for ip in "${ips[@]}"; do
    out=$($SSH@"$ip" 'pgrep -f "[s]cripts/remote/worker.sh" >/dev/null && echo yes || echo no' 2>/dev/null) || out=""
    case "$out" in yes) return 0;; no) ;; *) rc=2;; esac
  done
  return $rc
}
count() {
  local ip d=0 f=0 x
  for ip in "${ips[@]}"; do
    x=$($SSH@"$ip" 'grep -c "^done" /root/remote-out/status.log 2>/dev/null; true' 2>/dev/null); d=$((d + ${x:-0}))
    x=$($SSH@"$ip" 'grep -c "^FAILED" /root/remote-out/status.log 2>/dev/null; true' 2>/dev/null); f=$((f + ${x:-0}))
  done
  echo "$d of $njobs done, $f failed"
}
fails=0; last=""; deadline=$((SECONDS + MAX_HOURS * 3600))
while :; do
  rc=0; running || rc=$?
  if [ "$rc" = 1 ]; then break; fi
  if [ "$SECONDS" -ge "$deadline" ]; then echo "ERROR: still running after MAX_HOURS=$MAX_HOURS"; exit 1; fi
  if [ "$rc" = 2 ]; then
    fails=$((fails + 1))
    [ "$fails" -ge 10 ] && { echo "ERROR: a box hasn't answered for 10 polls"; exit 1; }
    sleep 30; continue
  fi
  fails=0; c=$(count)
  [ "$c" != "$last" ] && { echo "  $(date +%H:%M) $c"; last=$c; }
  sleep 20
done
echo "  $(date +%H:%M) $(count) — finished; pulling results ..."
pull; pulled=1
cat "$DEST/status.log"
echo "results: experiments/ (changed files) and $DEST (logs: <box>/job-<id>.log)"
[ "$(grep -c '^done' "$DEST/status.log")" = "$njobs" ]
