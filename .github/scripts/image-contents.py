#!/usr/bin/env python3
"""List what a remnux-distro image contains, so a build can be compared with another one.

  image-contents.py oci <archive> <arch> <out>   image in an OCI archive (docker buildx --output type=oci)
  image-contents.py hub <repo:tag> <arch> <out>  image on Docker Hub, read anonymously
  image-contents.py size <image@digest> <arch>   compressed size of an image in a registry
  image-contents.py diff <old> <new> <old-label> <new-label>

oci and hub write one line per installed Debian package ("deb <name> <version>") and per
entry in /opt and /usr/local/bin ("path <path>") to <out>, and print the compressed size
of the image's layers in bytes. diff prints a Markdown comparison of two such lists.
"""
import json
import subprocess
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request

ACCEPT = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])


def child(doc, arch):
    """Pick the linux/<arch> entry of an image index. Attestations list unknown/unknown."""
    entries = doc.get("manifests", [])
    for d in entries:
        p = d.get("platform") or {}
        if p.get("os") == "linux" and p.get("architecture") == arch:
            return d
    if len(entries) == 1 and not entries[0].get("platform"):
        return entries[0]
    sys.exit(f"no linux/{arch} image in the index")


def manifest(load, doc, arch):
    """Follow image indexes down to the image manifest for arch."""
    while "manifests" in doc:
        doc = json.load(load(child(doc, arch)["digest"]))
    return doc


def contents(load, doc, arch, out):
    layers = manifest(load, doc, arch)["layers"]
    status, paths = None, set()
    for layer in layers:
        with load(layer["digest"]) as blob, tarfile.open(fileobj=blob, mode="r|*") as t:
            for m in t:
                name = m.name[2:] if m.name.startswith("./") else m.name
                parts = name.rstrip("/").split("/")
                base = parts[-1]
                # Whiteouts are handled simply. That's enough here: the image is one layer on
                # top of ubuntu, whose /opt and /usr/local/bin are empty, and that layer
                # includes the complete dpkg status file.
                if base.startswith(".wh."):
                    path = "/".join(parts[:-1] + [base[4:]])
                    paths = {p for p in paths if p != path and not p.startswith(path + "/")}
                    continue
                if name == "var/lib/dpkg/status" and m.isfile():
                    status = t.extractfile(m).read().decode("utf-8", "replace")
                if (len(parts) == 2 and parts[0] == "opt") or \
                        (len(parts) == 4 and parts[:3] == ["usr", "local", "bin"]):
                    paths.add(name.rstrip("/"))
    if status is None:
        sys.exit("no /var/lib/dpkg/status in the image")
    lines = [f"path {p}" for p in paths]
    for stanza in status.split("\n\n"):
        f = {}
        for line in stanza.splitlines():
            if line[:1] not in (" ", "\t") and ":" in line:
                k, v = line.split(":", 1)
                f[k] = v.strip()
        if "Package" in f and f.get("Status", "").endswith(" installed"):
            a = f.get("Architecture", "")
            name = f["Package"] if a in (arch, "all") else f"{f['Package']}:{a}"
            lines.append(f"deb {name} {f.get('Version', '')}")
    with open(out, "w") as fh:
        fh.write("\n".join(sorted(lines)) + "\n")
    print(sum(layer["size"] for layer in layers))


def oci(archive, arch, out):
    with tarfile.open(archive) as t:
        def load(digest):
            return t.extractfile("blobs/" + digest.replace(":", "/"))
        contents(load, json.load(t.extractfile("index.json")), arch, out)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def hub(ref, arch, out):
    repo, tag = ref.rsplit(":", 1)
    opener = urllib.request.build_opener(NoRedirect)

    def get(path):
        # Get a fresh token for each request: a layer download can outlast one.
        token_url = ("https://auth.docker.io/token?service=registry.docker.io"
                     f"&scope=repository:{repo}:pull")
        token = json.load(urllib.request.urlopen(token_url, timeout=60))["token"]
        url = f"https://registry-1.docker.io/v2/{repo}/{path}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": ACCEPT})
        try:
            return opener.open(req, timeout=300)
        except urllib.error.HTTPError as e:
            # Blobs redirect to a CDN that rejects the registry's token, so follow without it.
            if e.code in (301, 302, 303, 307, 308):
                return urllib.request.urlopen(urllib.parse.urljoin(url, e.headers["Location"]), timeout=300)
            raise

    # Manifests come from the manifests endpoint and layers from the blobs endpoint, so
    # resolve the image manifest here and let contents() read only layers.
    doc = manifest(lambda digest: get("manifests/" + digest), json.load(get("manifests/" + tag)), arch)
    contents(lambda digest: get("blobs/" + digest), doc, arch, out)


def size(ref, arch):
    def inspect(r):
        res = subprocess.run(["docker", "buildx", "imagetools", "inspect", "--raw", r],
                             check=True, capture_output=True, text=True)
        return json.loads(res.stdout)
    repo = ref.split("@", 1)[0]
    doc = inspect(ref)
    while "manifests" in doc:
        doc = inspect(f"{repo}@{child(doc, arch)['digest']}")
    print(sum(layer["size"] for layer in doc["layers"]))


def diff(old_path, new_path, old_label, new_label):
    def read(path):
        debs, paths = {}, set()
        for line in open(path):
            kind, _, rest = line.rstrip("\n").partition(" ")
            if kind == "deb":
                name, _, version = rest.partition(" ")
                debs[name] = version
            elif kind == "path":
                paths.add(rest)
        return debs, paths

    (od, op), (nd, np) = read(old_path), read(new_path)
    changed = sorted(k for k in od.keys() & nd.keys() if od[k] != nd[k])
    print(f"### {new_label} compared with {old_label}\n")
    print(f"- Debian packages: {len(od)} in {old_label}, {len(nd)} in {new_label}, "
          f"{len(nd.keys() - od.keys())} only in {new_label}, {len(od.keys() - nd.keys())} only in "
          f"{old_label}, {len(changed)} at a different version")
    print(f"- Entries in /opt and /usr/local/bin: {len(op)} in {old_label}, {len(np)} in {new_label}\n")
    sections = [
        (f"Packages only in {new_label}", sorted(nd.keys() - od.keys())),
        (f"Packages only in {old_label}", sorted(od.keys() - nd.keys())),
        ("Packages at a different version", [f"{k} {od[k]} -> {nd[k]}" for k in changed]),
        (f"/opt and /usr/local/bin entries only in {new_label}", sorted(np - op)),
        (f"/opt and /usr/local/bin entries only in {old_label}", sorted(op - np)),
    ]
    for title, items in sections:
        print(f"<details><summary>{title} ({len(items)})</summary>\n\n```")
        print("\n".join(items))
        print("```\n</details>\n")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"oci": oci, "hub": hub, "size": size, "diff": diff}[cmd](*args)
