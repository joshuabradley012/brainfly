#!/usr/bin/env bash
# Box side of run.sh: claim jobs from the queue until it's empty and run each, one at a time. run.sh
# starts SLOTS of these per box. A job's output goes to OUT/job-<id>.log and its outcome to
# OUT/status.log ("done <id> <seconds>s <box>" or "FAILED <id> rc=<code> <seconds>s <box>").
#
# Env: QUEUE (local, or the address of the box holding the queue), THREADS (numba threads per job),
# OUT (/root/remote-out)
set -uo pipefail
cd /root/brainfly
OUT=${OUT:-/root/remote-out}
QUEUE=${QUEUE:-local}
export PATH=/root/venv/bin:$PATH NUMBA_NUM_THREADS=${THREADS:-8} FLY_DATA=/root/fly-data PYTHONUNBUFFERED=1
TAKE='cd /root/remote-out && flock queue.lock sh -c "head -n 1 queue.txt; sed -i 1d queue.txt"'

# claim: print the next "id<TAB>command" line, or nothing when the queue is empty. Retries a
# queue box that doesn't answer, so a network blip can't end a worker with jobs left.
claim() {
  local tries=0 line
  while :; do
    if [ "$QUEUE" = local ]; then line=$(sh -c "$TAKE") && { echo "$line"; return 0; }
    else line=$(ssh -i /root/.ssh/queue -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR \
                   -o BatchMode=yes -o ConnectTimeout=10 root@"$QUEUE" "$TAKE") && { echo "$line"; return 0; }
    fi
    tries=$((tries + 1)); [ "$tries" -ge 20 ] && return 1
    sleep 15
  done
}

while line=$(claim) && [ -n "$line" ]; do
  id=${line%%$'\t'*}; cmd=${line#*$'\t'}
  start=$(date +%s)
  bash -c "$cmd" > "$OUT/job-$id.log" 2>&1 < /dev/null; rc=$?
  secs=$(( $(date +%s) - start ))
  if [ "$rc" = 0 ]; then echo "done $id ${secs}s $(hostname)"; else echo "FAILED $id rc=$rc ${secs}s $(hostname)"; fi >> "$OUT/status.log"
done
