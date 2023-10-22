import random
from typing import List

from lswin import Rect, WindowInfo, filter_window_infos, sorted_window_infos

_mocked_win_list: List[WindowInfo] = [
    WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
               title='title101', subtitle='subtitle13'),
    WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
               title='title101', subtitle='subtitle11'),
    WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
               title='title101', subtitle='subtitle11'),

    WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
               title='title202', subtitle='subtitle21'),
]

_shuffled_win_list = _mocked_win_list[:]
random.shuffle(_shuffled_win_list)


def test_filter_window_infos():
    assert list(filter_window_infos(_mocked_win_list, exclude_0_area=True, keep_one_for_same_pid_rect=False)) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(filter_window_infos(_mocked_win_list, exclude_0_area=False, keep_one_for_same_pid_rect=True)) == [
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(filter_window_infos(_mocked_win_list, exclude_0_area=True, keep_one_for_same_pid_rect=True)) == [
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]


def test_sorted_window_infos():
    assert list(sorted_window_infos(_shuffled_win_list, sort_keys=['pid', 'win_id'])) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(sorted_window_infos(_shuffled_win_list, sort_keys=['x', 'y'])) == [
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(sorted_window_infos(_shuffled_win_list, sort_keys=['width', 'height'])) == [
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(sorted_window_infos(_shuffled_win_list, sort_keys=['title', 'subtitle'])) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
