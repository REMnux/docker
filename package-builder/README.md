# REMnux Package Builder

Docker container for building Debian packages for the REMnux PPA using `dpkg-buildpackage`. Provides clean-room build isolation on Ubuntu Noble (24.04).

## Build the Image

```bash
docker build -t remnux/package-builder:noble -f package-builder/Dockerfile.noble package-builder/
```

## Run

Mount the distro repo and (optionally) your GPG key:

```bash
docker run --rm -it \
  -v /path/to/distro:/distro \
  -v ~/.gnupg:/root/.gnupg:ro \
  remnux/package-builder:noble /bin/bash
```

## Typical Workflow

Inside the container:

```bash
cd /distro/ppasrc/packagename/packagename-0.1.1-noble

# Install any additional build dependencies:
apt-get update && apt-get install -y <deps>

# Test build locally (unsigned):
dpkg-buildpackage -us -uc

# Create signed source package for Launchpad:
debuild -S -k<KEYID> -d

# Upload to Launchpad PPA:
dput -f ppa:remnux/stable ../packagename_0.1.1_source.changes
```

## Security Notes

- No secrets or GPG keys are baked into the image.
- Mount GPG keys at runtime with `:ro` (read-only).
- Signing should only happen locally, never in CI without proper secret management.

## Architecture

The Dockerfile is architecture-neutral. Build natively on arm64 when needed; `ubuntu:24.04` auto-resolves to the host architecture.
