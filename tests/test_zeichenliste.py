#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tests.model import AnkiDeck, AnkiNote

READ_ONLY_TAG = "nur_lesen"

# Note that the ordering matters, as it is used to determine if a note covers a specific unit in the "future"

ZEICHENLISTE_A11 = {
    "eh_0": ("零一二三四五六七八九十", ""),
    "eh_1": ("我你他她们好叫姓什么名字中文请问认识高兴对不起", "呢"),
    "eh_2": ("早上但是住在哪里北京日本美英国明星吗", "德柏林"),
    "eh_3": ("也爸妈弟妹都做工作的和家学生哥姐老师医院", "记者照片校"),
    "eh_4": ("高帅酷谁知道多大喜欢海现运动员岁出地可爱电子", "真年轻漂亮邮箱籍龄"),
    "eh_5": ("手机话号码少公园路可以打给收到学址房间新", "发送退寓谢"),
    "eh_6": ("吃饭去那几月今天星期真的没问题怎么样跟见面看书班", "餐厨派"),
}

ZEICHENLISTE_A12 = {
    "eh_7": ("半菜唱歌到点午影分开有门跟朋友时太晚要音乐语", "听写周末邮始刻跑步卡"),
    "eh_8": ("白本市心贵黑红钱件裤块来买衣服每店儿百错物", "双超购价色试售货便宜"),
    "eh_9": ("东西南远边铁方近前后离米先行走左右", "租站钟附联系楼往银局交通平"),
    "eh_10": ("喜欢火车共汽还些当然坐旅游自骑馆第", "厅参观暑假景它需颜利船览爬拍"),
    "eh_11": (
        "足网球比赛想希望过会泳男能候场性别休其踢雪乒乓",
        "体育格队兰赢跳舞闲卷冲浪滑蹦极",
    ),
    "eh_12": ("城从算回飞机玩或觉得历史千说应该只主意习", "实加坡兵俑"),
}

ZEICHENLISTEN = {
    "a1.1": ZEICHENLISTE_A11,
    "a1.2": ZEICHENLISTE_A12,
}

LEVELS = list(ZEICHENLISTEN.keys())

OPTIONAL_UNITS = [
    # Pairs of (level, unit)
    ("a1.2", "eh_9"),
    ("a1.2", "eh_10"),
    ("a1.2", "eh_11"),
    ("a1.2", "eh_12"),
]


def test_zeichenliste_plausible():
    for level, zl in ZEICHENLISTEN.items():
        for unit, chars in zl.items():
            assert " " not in chars
            for ch in chars[0] + chars[1]:
                assert ord(ch) >= 0x2E80  # Start of first CJK unicode block


def test_mithanzi_field_not_empty(note: AnkiNote):
    req_readonly = READ_ONLY_TAG in note.tags
    req_zl = "zeichenliste" in note.tags

    if not req_zl and not req_readonly:
        return  # Not relevant for us

    assert (
        note.fields["MitHanzi"] != ""
    ), f"Note {note} requires hanzi, but MitHanzi flag field is not set"


def test_zeichenliste_exists(deck: AnkiDeck):
    remaining = {}
    n = 0
    all_chars = set()
    all_chars_ro = set()
    for level, ldat in ZEICHENLISTEN.items():
        for unit, chars in ldat.items():
            remaining[(n, level, unit)] = chars
            all_chars.update(chars[0])
            all_chars_ro.update(chars[1])
            n += 1
    print(
        f"Checking a total of {len(remaining)} units containing {len(all_chars)} chars (+{len(all_chars_ro)} read only)"
    )
    print(f"Mandatory characters: {''.join(all_chars)}")
    print(f"Read-only characters: {''.join(all_chars_ro)}")

    all_units = list(remaining.keys())

    for note in deck.notes:
        req_readonly = READ_ONLY_TAG in note.tags
        req_zl = "zeichenliste" in note.tags

        if not req_zl and not req_readonly:
            continue  # Not relevant for us

        chars = note.fields["Hanzi"]

        units = list(filter(lambda tag: tag.startswith("eh_"), note.tags))
        assert len(units) == 1, f"{note} should only have one unit tag"
        cur_unit = units[0]

        levels = list(filter(lambda tag: tag in LEVELS, note.tags))
        assert len(levels) == 1, f"{note} should only have one level tag"
        cur_level = levels[0]

        n_s = list(
            map(
                lambda udat: udat[0],
                filter(
                    lambda udat: udat[1] == cur_level and udat[2] == cur_unit, all_units
                ),
            )
        )
        assert (
            len(n_s) == 1
        ), f"{note} level and unit could not be found in unit list {all_units}"
        cur_n = n_s[0]

        # print(
        #     f"{note.fields['Hanzi']}\t level: {cur_level} unit: {cur_unit} n: {cur_n} {len(remaining)}"
        # )

        new_remaining = {}
        for (n, level, unit), (rem_zl, rem_readonly) in list(remaining.items()):
            if n >= cur_n:
                # Remove chars from any units after the one the note is tagged for

                for ch in chars:
                    if ch in rem_readonly:
                        rem_readonly = rem_readonly.replace(ch, "")

                    if req_zl and ch in rem_zl:
                        rem_zl = rem_zl.replace(ch, "")

            if rem_readonly != "" or rem_zl != "":
                new_remaining[(n, level, unit)] = (rem_zl, rem_readonly)
        remaining = new_remaining

    missing = {k: v for k, v in remaining.items() if (k[1], k[2]) not in OPTIONAL_UNITS}
    chars = set()
    if len(missing) != 0:
        print(f"{len(missing)} mandatory unit(s) have characters missing:")
        for unit, (mandatory, readonly) in missing.items():
            print(f"Unit {unit}: mandatory: '{mandatory}', readonly: {readonly}'")
            chars.update(mandatory)
            chars.update(readonly)

    chars_mandatory = set(chars)

    if (len(remaining) - len(missing)) != 0:
        print(
            f"Also, {len(remaining)-len(missing)} optional unit(s) are missing characters: "
        )
        for unit, (mandatory, readonly) in {
            k: v for k, v in remaining.items() if (k[1], k[2]) in OPTIONAL_UNITS
        }.items():
            print(f"Unit {unit}: mandatory: '{mandatory}', readonly: {readonly}'")
            chars.update(mandatory)
            chars.update(readonly)

    if len(missing) != 0:
        pytest.fail(
            f"Missing {len(chars_mandatory)} characters in {len(missing)} units ({len(chars)} including optional units): "
            f"{missing}\nCharacters: {''.join(chars)}"
        )
