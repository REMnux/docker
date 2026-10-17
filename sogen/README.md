This Docker image encapsulates [Sogen](https://github.com/momo5502/sogen), a Windows user-mode emulator for Linux. Sogen runs the real Windows system DLLs on an emulated CPU, so you can trace a program's API calls and syscalls, debug it over GDB from outside the emulated process, take snapshots, and make runs reproducible.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/sogen

Before running the application, create ~/workdir on your host.

## The emulation root

Sogen needs an emulation root: a directory with the Windows system DLLs, registry hives, and API set map that the emulated program will see. The image doesn't include one, because Microsoft owns those files. When you open a shell in the container and no root exists in your working directory, a message explains how to get one. You have two options:

- Run `get-sogen-root` inside the container. It downloads the prebuilt root that the Sogen project publishes at sogen.dev (about 180 MB, 520 MB unpacked) into `~/workdir/root`. You do this once, since you keep the root in your working directory on the host. The Sogen project captures this root on a GitHub Actions Windows runner, so the emulated system reports that runner's computer name, such as `runnervm0xl3a`. A sample that checks for such names calls for the second option.
- Build your own root on a Windows system with `create-root.bat` from the Sogen repository, then copy the resulting `root` directory into `~/workdir`. The [Sogen wiki](https://github.com/momo5502/sogen/wiki/Run-The-Emulator) explains the steps.

## Analyzing a sample

Copy the sample into `~/workdir` and run:

    analyzer sample.exe

The `analyzer` command in the image is a small wrapper around Sogen's analyzer. When you don't name an emulation root, it passes the one in your working directory. When the program you name is a Windows executable on the host, it maps that file to `c:\` inside the emulated Windows and runs it from there, whatever the file's extension. Pass `-e` or `-p` yourself to make either choice, and the wrapper passes your arguments through. Sogen runs native Windows executables. In my tests, .NET assemblies stopped with error 0x80131700, because the .NET runtime files are absent from the prebuilt root.

Useful options include `-v` for verbose logging, `--report run.jsonl` for a machine-readable event log, `-c` to quiet the loader output, `-s` to print only the program's own output, and `--reproducible` to stub clocks. Run `analyzer --help` for the full list. The emulated program's sockets stay inside the emulator unless you add `--network live`. The container's own network is a separate matter. Add `--network none` to `docker run` when the container itself should stay offline.

## Debugging with GDB or IDA

Publish the debug port on loopback when you start the container, then start the analyzer in debug mode and bind to all interfaces inside the container:

    docker run --rm -it -p 127.0.0.1:28960:28960 -v ~/workdir:/home/nonroot/workdir remnux/sogen
    analyzer -d --bind 0.0.0.0 --port 28960 sample.exe

Connect from the host with `target remote 127.0.0.1:28960` in GDB, or with IDA's remote GDB debugger.

## Notes

The image builds Sogen from a pinned commit, recorded in `/opt/sogen/COMMIT`, with the Unicorn CPU backend. It runs on amd64 and arm64 systems, such as Apple Silicon Macs. The container runs as the user `nonroot`. On a Linux host where that user can't write to your working directory, add `--user $(id -u):$(id -g)` to `docker run`. A container is weak isolation for malware. Run it on a system you'd be willing to rebuild, and keep the emulated program offline unless you need it to reach the network.
