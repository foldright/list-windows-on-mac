#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
from dataclasses import dataclass
from optparse import OptionParser
from typing import Iterable, Tuple, Any

# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
import Quartz  # type: ignore

__version__ = '1.1.0-dev'


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    def t(self) -> Tuple[int, int, int, int]:
        """
        tuple representation
        """
        return self.x, self.y, self.width, self.height

    def s(self) -> str:
        """
        tuple style string for output
        """
        return str(self.t())


@dataclass
class WindowInfo:
    pid: int
    win_id: int

    rect: Rect

    title: str
    subtitle: str


class _DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        from dataclasses import is_dataclass, asdict
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


def list_window_infos() -> Iterable[WindowInfo]:
    for w in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        bounds = w.valueForKey_('kCGWindowBounds')
        yield WindowInfo(
            pid=int(w.valueForKey_('kCGWindowOwnerPID')),
            win_id=int(w.valueForKey_('kCGWindowNumber')),
            rect=Rect(
                int(bounds.valueForKey_('X')), int(bounds.valueForKey_('Y')),
                int(bounds.valueForKey_('Width')), int(bounds.valueForKey_('Height')),
            ),
            title=str(w.valueForKey_('kCGWindowOwnerName') or ''),
            subtitle=str(w.valueForKey_('kCGWindowName') or '')
        )


def filter_window_infos(
    win_list: Iterable[WindowInfo],
    exclude_0_area: bool, keep_one_for_same_pid_rect: bool
) -> Iterable[WindowInfo]:
    if exclude_0_area:
        win_list = (w for w in win_list if w.rect.width > 0 and w.rect.height > 0)
    if keep_one_for_same_pid_rect:
        win_list = {(w.pid, w.rect.t()): w for w in win_list}.values()
    return win_list


def sorted_window_infos(win_list: Iterable[WindowInfo], sort_keys: Iterable[str]) -> Iterable[WindowInfo]:
    return sorted(
        win_list, key=lambda w: tuple(
            getattr(w, k) if hasattr(w, k) else getattr(w.rect, k)
            for k in sort_keys
        ) + (w.pid, w.win_id)
    )


def print_window_infos_table(win_list: Iterable[WindowInfo], no_headers: bool = False) -> None:
    from itertools import tee

    s_pid = 'PID'
    s_win_id = 'WinID'

    i_pid, i_win_id, i_rect = tee(win_list, 3)

    max_pid_chars = max(len(str(w.pid)) for w in i_pid)
    max_pid_chars = max(max_pid_chars, len(s_pid))

    max_wid_chars = max(len(str(w.win_id)) for w in i_win_id)
    max_wid_chars = max(max_wid_chars, len(s_win_id))

    max_rect_chars = max(len(w.rect.s()) for w in i_rect)

    # print head
    if not no_headers:
        print(f"{s_pid: >{max_pid_chars}}  {s_win_id: >{max_wid_chars}}"
              f"  {'(x, y, w, h)': <{max_rect_chars}}  [Title] SubTitle")
        print(f"{'-' * max_pid_chars}  {'-' * max_wid_chars}  {'-' * max_rect_chars}"
              f"  {'-' * (80 - max_pid_chars - max_wid_chars - max_rect_chars - 6)}")
    # print items
    for w in win_list:
        title_info = f"[{w.title}]{'' if not w.subtitle else ' ' + w.subtitle}"
        print(f"{w.pid: >{max_pid_chars}}  {w.win_id: >{max_wid_chars}}"
              f"  {w.rect.s(): <{max_rect_chars}}  {title_info}")


def window_infos_to_json(win_list: Iterable[WindowInfo]) -> str:
    from json import dumps
    return dumps(list(win_list), cls=_DataClassJSONEncoder, indent=2)


def print_window_infos_json(win_list: Iterable[WindowInfo]) -> None:
    print(window_infos_to_json(win_list))


def main() -> int:
    from dataclasses import fields
    supported_sort_keys = tuple(
        [f.name for f in fields(WindowInfo) if f.name != 'rect']
        + [f.name for f in fields(Rect)]
    )
    supported_sort_keys_str = ', '.join(supported_sort_keys)

    ############################################################
    # parse options
    ############################################################

    option_parser = OptionParser(
        '%prog [OPTION]...'
        '\nlist win_list info(rect, owner process id, window id, title) on macOS.'
        '\n\nExamples:'
        '\n  %prog'
        '\n  %prog --exclude-0-area'
        '\n  %prog --sort-key x --sort-key title'
        '\n  %prog --keep-one-for-same-pid-rect'
    )
    option_parser.add_option(
        '-Z', '--exclude-0-area', dest='exclude_0_area', default=False,
        action='store_true', help='exclude win_list with 0 area')
    option_parser.add_option(
        '-o', '--keep-one-for-same-pid-rect', dest='keep_one_for_same_pid_rect',
        default=False, action='store_true', help='keep only one window for same (pid, rect)')
    option_parser.add_option(
        '-k', '--sort-key', dest='sort_keys', metavar='SORT_KEY', default=[], action='append',
        help=f"sort key, can be {supported_sort_keys_str}; default sort key is (pid, win_id)")
    option_parser.add_option(
        '-H', '--no-headers', dest='no_headers', default=False,
        action='store_true', help='print no header line')
    option_parser.add_option(
        '--json', dest='json', default=False, action='store_true', help='print json format')

    options, _ = option_parser.parse_args()
    if illegal_sort_keys := tuple(k for k in options.sort_keys if k not in supported_sort_keys):
        print(f"Unsupported sort key: {', '.join(illegal_sort_keys)}!"
              f" supported sort keys: {supported_sort_keys_str}", file=sys.stderr)
        return 1

    ############################################################
    # biz logic
    ############################################################

    win_list = list_window_infos()
    win_list = filter_window_infos(win_list, options.exclude_0_area, options.keep_one_for_same_pid_rect)
    win_list = sorted_window_infos(win_list, options.sort_keys)
    if options.json:
        print_window_infos_json(win_list)
    else:
        print_window_infos_table(win_list, no_headers=options.no_headers)

    return 0


if __name__ == '__main__':
    sys.exit(main())
