#!/bin/bash
set -ex

# Ray doesn't publish combiend aarch64 & amd64 images because idk.
RAY_VERSION=2.38.0-py311
RAY_IMAGE=holdenk/ray:${RAY_VERSION}

BUILDX_CMD=${BUILDX_CMD:-push}
PLATFORM=${PLATFORM:-linux/amd64,linux/arm64}

pull_or_build_image() {
	local image=$1
	local ray_version=$2
	local dockerfile=$3

	docker pull "${image}" || docker buildx build --platform="${PLATFORM}" -t "${image}" . -f "${dockerfile}" "${BUILDX_CMD}" --build-arg RAY_VERSION="${ray_version}"
}
export RAY_VERSION

pull_or_build_image "${RAY_IMAGE}" "${RAY_VERSION}" "k8s/ray/RayDockerfile"

# Using the amd64/arm64 ray container as a base put together a container with the FHI code and libs in it.
COMBINED_IMAGE=holdenk/fhi-ray:${FHI_VERSION}
pull_or_build_image "${COMBINED_IMAGE}" "${RAY_VERSION}" "k8s/ray/CombinedDockerfile"