One aspect of the REMnux project involves providing [Docker images of popular malware analysis tools](https://docs.remnux.org/#run-in-containers), with the goal of allowing investigators to conveniently utilize difficult-to-install applications without having to install the REMnux distro. You can [download and run existing images](https://docs.remnux.org/run-tools-in-containers/remnux-containers) and [contribute your own](https://docs.remnux.org/get-involved/add-or-update-tools/contribute-dockerfile) to the REMnux collection. You can also [run the REMnux distro as a Docker container](https://docs.remnux.org/install-distro/remnux-as-a-container) by using the prebuilt Docker image hosted in the REMNux repository on Docker Hub.

This Github repository hosts the Dockerfiles themselves. Workflows in this repository build the images on GitHub Actions and publish them to [Docker Hub](https://hub.docker.com/u/remnux/).

## Build and publish an image

Each tool image has its own workflow in `.github/workflows`, such as `radare2.yml`. That workflow calls the shared `build-image.yml` with the image's settings and smoke test. The workflow builds the image on GitHub's native runners for amd64 and, when the tool supports it, arm64. To publish an image, run its workflow from the repository's Actions tab:

1. Run it with **push** off. Each runner builds the image, runs the smoke test, and reports the build time and image size in the job summary.
2. If that run passes, run the workflow again with **push** on. Each runner uploads its image to Docker Hub, downloads it again, and runs the smoke test on the downloaded copy. The merge job then updates the tags, but only after the smoke test passes on every architecture.

The merge job writes each tag's previous digest to the job summary. To restore a previous image, run `docker buildx imagetools create -t remnux/<image>:<tag> remnux/<image>@<digest>`.

The workflows sign in to Docker Hub through the remnux organization's `github-remnux-docker` OIDC connection, which accepts only this repository's master branch. Each image's Docker Hub repository needs an image-push entry in that connection's ruleset. To add an image, copy an existing workflow, then change its settings, its test, and its list of architectures.

The `remnux-distro.yml` workflow builds and publishes the REMnux distro image, `remnux/remnux-distro`. Instead of a smoke test, it reports how the new image's packages differ from the published image and between architectures.
