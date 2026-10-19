"""Build only the local runtime layer; this does not build a standalone Base image."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-image", default="java-case-056-env")
    parser.add_argument("--image", default="java-case-056-env:organized-local")
    args = parser.parse_args()
    image_dir = Path(__file__).resolve().parent / "image"
    subprocess.run(["docker", "image", "inspect", args.base_image], check=True,
                   stdout=subprocess.DEVNULL)
    return subprocess.call([
        "docker", "build", "--pull=false", "--build-arg", f"BASE_IMAGE={args.base_image}",
        "-t", args.image, str(image_dir),
    ])


if __name__ == "__main__":
    raise SystemExit(main())
