import random
from typing import List

from pytest import fixture

from lswin import Rect, WindowInfo, filter_window_infos, sorted_window_infos, window_infos_to_json


def _mocked_win_list() -> List[WindowInfo]:
    return [
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]


@fixture
def mocked_win_list() -> List[WindowInfo]:
    return _mocked_win_list()


@fixture
def shuffled_win_list() -> List[WindowInfo]:
    shuffled = _mocked_win_list()
    random.shuffle(shuffled)
    return shuffled


def test_filter_window_infos(mocked_win_list: List[WindowInfo]) -> None:
    assert list(filter_window_infos(mocked_win_list, exclude_0_area=True, keep_one_for_same_pid_rect=False)) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(filter_window_infos(mocked_win_list, exclude_0_area=False, keep_one_for_same_pid_rect=True)) == [
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(filter_window_infos(mocked_win_list, exclude_0_area=True, keep_one_for_same_pid_rect=True)) == [
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]


def test_sorted_window_infos(shuffled_win_list: List[WindowInfo], mocked_win_list: List[WindowInfo]) -> None:
    assert list(sorted_window_infos(shuffled_win_list, sort_keys=['pid', 'win_id'])) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]
    assert list(sorted_window_infos(shuffled_win_list, sort_keys=['x', 'y'])) == mocked_win_list
    assert list(sorted_window_infos(shuffled_win_list, sort_keys=['width', 'height'])) == mocked_win_list
    assert list(sorted_window_infos(shuffled_win_list, sort_keys=['title', 'subtitle'])) == [
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=12, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=101, win_id=13, rect=Rect(x=0, y=0, width=0, height=100),
                   title='title101', subtitle='subtitle13'),

        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]


def test_window_infos_to_json() -> None:
    assert window_infos_to_json([
        WindowInfo(pid=101, win_id=11, rect=Rect(x=1, y=20, width=10, height=200),
                   title='title101', subtitle='subtitle11'),
        WindowInfo(pid=202, win_id=21, rect=Rect(x=10, y=15, width=100, height=100),
                   title='title202', subtitle='subtitle21'),
    ]) == r'''[
  {
    "pid": 101,
    "win_id": 11,
    "rect": {
      "x": 1,
      "y": 20,
      "width": 10,
      "height": 200
    },
    "title": "title101",
    "subtitle": "subtitle11"
  },
  {
    "pid": 202,
    "win_id": 21,
    "rect": {
      "x": 10,
      "y": 15,
      "width": 100,
      "height": 100
    },
    "title": "title202",
    "subtitle": "subtitle21"
  }
]'''
