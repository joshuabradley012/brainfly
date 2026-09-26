"""brainfly's command line: `brainfly download | build | info`, or `python -m brainfly ...`."""
from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .data import DATA, FILES, RELEASE_URL, download, has_data


def _info(data: Path) -> None:
    from .brain import cuda_available

    print(f"brainfly {__version__}")
    print(f"data folder: {data}")
    for name in FILES:
        path = data / name
        size = f"{path.stat().st_size / 1e6:,.0f} MB" if path.exists() else "missing"
        print(f"  {name}: {size}")
    if not has_data(data):
        print("  `brainfly download` fetches them (creating a FlyBrain does too)")
    print("cuda:", "available" if cuda_available() else 'not available (pip install "brainfly[gpu]")')


def main(argv: list[str] | None = None) -> None:
    cli = argparse.ArgumentParser(prog="brainfly", description="The MaleCNS fruit fly connectome as a network you can run.")
    cli.add_argument("--version", action="version", version=f"brainfly {__version__}")
    commands = cli.add_subparsers(dest="command", required=True)
    get = commands.add_parser("download", help="fetch the prebuilt network files (~260 MB)")
    get.add_argument("--url", default=RELEASE_URL, help="where the files are (default this project's release, or $BRAINFLY_DATA_URL)")
    get.add_argument("--force", action="store_true", help="fetch them again even if they're there")
    commands.add_parser("build", help="fetch MaleCNS v1.0 (~1.1 GB) and build the network files from it")
    commands.add_parser("info", help="show the data folder and whether a GPU can be used")
    for command in commands.choices.values():
        command.add_argument("--data", type=Path, default=DATA, help=f"the data folder (default {DATA}, or $FLY_DATA)")
    args = cli.parse_args(argv)
    if args.command == "download":
        download(args.data, args.url, force=args.force)
        print(f"network files in {args.data}")
    elif args.command == "build":
        try:
            from .build import build
        except ImportError as err:
            raise SystemExit(f'building needs pandas, pyarrow and openpyxl ({err}): pip install "brainfly[build]"')
        build(args.data)
    else:
        _info(args.data)


if __name__ == "__main__":
    main()
