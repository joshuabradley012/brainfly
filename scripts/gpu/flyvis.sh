#!/usr/bin/env bash
# Train experiments/flyvis_t2_scratch.py on a rented NVIDIA GPU box (RunPod, Vast.ai, Lambda, ...): any Linux machine
# with CUDA and Python 3.10+ you can SSH into. Rent the box in the provider's web console (a PyTorch/CUDA image, an
# RTX 4090, A10 or L4 is plenty, ~30 GB of disk), then drive it from this Mac:
#
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh setup             # copy the repo and flyvis's data, install, fetch Sintel
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh bench [RUN]       # seconds per iteration on that GPU (nothing saved)
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh start [RUN]       # copy RUN's checkpoint up and resume it there
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh status [RUN]      # the run's last log lines
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh pull [RUN]        # bring its checkpoint and .json home
#   HOST=root@1.2.3.4 scripts/gpu/flyvis.sh stop [RUN]
#
# RUN is main (flow/9100/000), control (9101), noaug (9102) or decoder000 (9103), as in flyvis_t2_scratch.py.
# Env: HOST (required), PORT (22; RunPod and Vast give other ports), KEY (an ssh identity file, optional).
# One run lives in one place at a time: start and pull refuse while this Mac is training the same run, since the two
# copies would write diverging checkpoints. Delete the box in the provider's console when the run is home; it bills
# by the hour until then.
set -euo pipefail
cd "$(dirname "$0")/../.."

CMD=${1:?usage: HOST=user@ip scripts/gpu/flyvis.sh setup|bench|start|status|pull|stop [RUN]}
RUN=${2:-main}
: "${HOST:?set HOST=user@ip for the GPU box}"
PORT=${PORT:-22}
SSH_OPTS=(-p "$PORT" -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30)
[ -n "${KEY:-}" ] && SSH_OPTS+=(-i "$KEY")
ssh_box() { ssh "${SSH_OPTS[@]}" "$HOST" "$@"; }
RSYNC=(rsync -az -e "ssh ${SSH_OPTS[*]}")

case "$RUN" in
  main) ID=9100; JSON=flyvis_t2_scratch.json; ARG="" ;;
  control) ID=9101; JSON=flyvis_t2_scratch_control.json; ARG=control ;;
  noaug) ID=9102; JSON=flyvis_t2_scratch_noaug.json; ARG=noaug ;;
  decoder000) ID=9103; JSON=flyvis_t2_scratch_decoder000.json; ARG=decoder000 ;;
  *) echo "unknown run $RUN (main, control, noaug, decoder000)" >&2; exit 2 ;;
esac
LOCAL_DATA=${FLY_DATA:-$HOME/fly-data}
RESULT=flyvis/results/flow/$ID/000
# Rented containers often see every core of the host but get a CPU quota (RunPod: 31 of 256), and torch starts a thread
# per visible core: two runs then thrash. THREADS (default 8) caps each run's threads.
REMOTE_ENV="export FLY_DATA=\$HOME/fly-data FLYVIS_ROOT_DIR=\$HOME/fly-data/flyvis OMP_NUM_THREADS=${THREADS:-8} MKL_NUM_THREADS=${THREADS:-8}; cd \$HOME/fly.ai; source .venv/bin/activate"

running_here() {   # is this Mac training RUN right now?
  if [ -z "$ARG" ]; then pgrep -f "flyvis_t2_scratch.py *$" >/dev/null
  else pgrep -f "flyvis_t2_scratch.py $ARG" >/dev/null; fi
}

case "$CMD" in
  setup)
    echo "copying the repository ..."
    "${RSYNC[@]}" --exclude .git --exclude .venv --exclude __pycache__ --exclude remote-out --exclude '*.npz' \
      ./ "$HOST:fly.ai/"
    echo "copying flyvis's models, connectome and renderings (Sintel itself is fetched on the box) ..."
    ssh_box 'mkdir -p $HOME/fly-data/flyvis'
    "${RSYNC[@]}" --exclude SintelDataSet "$LOCAL_DATA/flyvis/" "$HOST:fly-data/flyvis/"
    ssh_box bash -s <<'EOF'
set -euo pipefail
cd $HOME/fly.ai
python3 -m venv --system-site-packages .venv   # reuse the image's CUDA torch
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -e ".[flyvis]"
python -c "import torch; assert torch.cuda.is_available(), 'torch sees no CUDA GPU'; print('torch', torch.__version__, 'on', torch.cuda.get_device_name())"
export FLY_DATA=$HOME/fly-data FLYVIS_ROOT_DIR=$HOME/fly-data/flyvis
echo "fetching Sintel (~5 GB) ..."
python -c "from flyvis.datasets.sintel_utils import download_sintel; print(download_sintel())"
EOF
    echo "ready: HOST=$HOST scripts/gpu/flyvis.sh bench $RUN"
    ;;
  bench)
    ssh_box "$REMOTE_ENV; python scripts/gpu/bench.py $RUN ${ITERS:-300}"
    ;;
  start)
    if running_here; then echo "this Mac is training $RUN; stop it first (it resumes from its checkpoint)" >&2; exit 1; fi
    if [ -d "$LOCAL_DATA/$RESULT" ]; then
      echo "copying $RUN's checkpoint and log up ..."
      "${RSYNC[@]}" "$LOCAL_DATA/$RESULT/" "$HOST:fly-data/$RESULT/"
    fi
    [ -f "experiments/$JSON" ] && "${RSYNC[@]}" "experiments/$JSON" "$HOST:fly.ai/experiments/"
    ssh_box "$REMOTE_ENV; cd experiments; nohup python -u flyvis_t2_scratch.py $ARG >> ../flyvis_$RUN.log 2>&1 < /dev/null & echo started, pid \$!"
    echo "follow it: HOST=$HOST scripts/gpu/flyvis.sh status $RUN"
    ;;
  status)
    ssh_box "pgrep -af 'flyvis_t2_scratch.py' || echo 'not running'; tail -n ${LINES:-5} \$HOME/fly.ai/flyvis_$RUN.log"
    ;;
  pull)
    if running_here; then echo "this Mac is training $RUN; pulling would overwrite its checkpoint" >&2; exit 1; fi
    mkdir -p "$LOCAL_DATA/$RESULT"
    "${RSYNC[@]}" "$HOST:fly-data/$RESULT/" "$LOCAL_DATA/$RESULT/"
    "${RSYNC[@]}" "$HOST:fly.ai/experiments/$JSON" experiments/
    mkdir -p remote-out; "${RSYNC[@]}" "$HOST:fly.ai/flyvis_$RUN.log" remote-out/ 2>/dev/null || true
    echo "pulled $RUN; it resumes here from the same checkpoint"
    ;;
  stop)
    if [ -z "$ARG" ]; then ssh_box "pkill -f 'flyvis_t2_scratch.py *\$' && echo stopped || echo 'not running'"
    else ssh_box "pkill -f 'flyvis_t2_scratch.py $ARG' && echo stopped || echo 'not running'"; fi
    ;;
  *) echo "unknown command $CMD" >&2; exit 2 ;;
esac
