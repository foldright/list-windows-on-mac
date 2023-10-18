# <div align="center">list windows info on macOS 🍎</div>

<p align="center">
<a href="https://github.com/foldright/list-windows-on-mac/actions/workflows/python-package.yml"><img src="https://img.shields.io/github/actions/workflow/status/foldright/list-windows-on-mac/python-package.yml?branch=master&logo=github&logoColor=white" alt="Github Workflow Build Status"></a>
<a href="https://github.com/foldright/list-windows-on-mac/stargazers"><img src="https://img.shields.io/github/stars/foldright/list-windows-on-mac" alt="GitHub Stars"></a>
<a href="https://github.com/foldright/list-windows-on-mac"><img src="https://img.shields.io/github/repo-size/foldright/list-windows-on-mac" alt="GitHub repo size"></a>
</p>

List windows info(rect, owner process id, windows id, title) on macOS.

## Prerequisites

*Note* if you run into error `No module named Quartz`, then run `pip install pyobjc-framework-Quartz` to install it;
or use recommended `virtual Python environments` to install it.

Tested on Python `3.7 ~ 3.12` macOS `12.6(GitHub Actions)/13.4(Personal MBP)`,

## Usage

```sh
$ python3 lswin.py
  PID  WinID  (x, y, w, h)           [Title] SubTitle
-----  -----  ---------------------  -------------------------------------------
  163      2  (2952, 0, 1, 1)        [Window Server]
  163    168  (0, 0, 1920, 24)       [Window Server] Menubar
  163    169  (0, 0, 1920, 24)       [Window Server]
  163    355  (0, -68, 1920, 24)     [Window Server] Menubar
  163    382  (2031, -44, 1920, 24)  [Window Server]
  187   1512  (0, -40, 1004, 30)     [loginwindow]
  187   6516  (751, 246, 417, 173)   [loginwindow]
  541    206  (360, 236, 1200, 824)  [Google Chrome.app]
  541    207  (0, 0, 1920, 24)       [Google Chrome.app]
  541    295  (400, 204, 1120, 876)  [Google Chrome.app]
  541  50925  (1173, 101, 367, 62)   [Google Chrome.app]
  541  52046  (-1, 1059, 640, 22)    [Google Chrome.app]
45424  35939  (0, 0, 1920, 24)       [Code]
45424  35958  (240, 131, 1440, 949)  [Code]
45424  35959  (100, 100, 1, 1)       [Code]
45424  35961  (535, 685, 260, 131)   [Code]
    ......


# more supported options see help
$ ./lswin.py -h
Usage: lswin.py [OPTION]...
list all windows title and their owner process ids.

Examples:
  lswin.py
  lswin.py --exclude-0-area
  lswin.py --sort-key x --sort-key title
  lswin.py --keep-one-for-same-pid-rect

Options:
  -h, --help            show this help message and exit
  -Z, --exclude-0-area  exclude windows with 0 area
  -o, --keep-one-for-same-pid-rect
                        keep only one window for same (pid, rect)
  -k SORT_KEY, --sort-key=SORT_KEY
                        sort key, can be pid, win_id, title, subtitle, x, y,
                        width, height; default sort key is (pid, win_id)
  -H, --no-headers      print no header line
```

## Known problems

Processes created by Safari browser will be displayed as same PID as main Safari process.

https://github.com/sjitech/mac_list_windows_pids/issues/1
