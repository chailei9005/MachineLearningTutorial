#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 科室名称映射至科室号
CLINIC_NAME_TO_NO = {
    u"妇科": u"1",
    u"儿科": u"2",
    u"内科": u"3",
    u"皮肤性病科": u"4",
    u"营养科": u"6",
    u"骨伤科": u"7",
    u"男科": u"8",
    u"外科": u"9",
    u"肿瘤及防治科": u"11",
    u"中医科": u"12",
    u"口腔颌面科": u"13",
    u"耳鼻咽喉科": u"14",
    u"眼科": u"15",
    u"整形美容科": u"16",
    u"精神心理科": u"17",
    u"产科": u"21",
    u"报告解读科": u"22",
    u"基因检测科": u"19",
    u"耳科": u"ja",
    u"心电图科": u"qe",
    u"肿瘤外科": u"mb",
    u"肿瘤中医科": u"md",
    u"心血管内科": u"ab",
    u"消化内科": u"ad",
    u"鼻科": u"jb",
    u"新生儿科": u"fb",
    u"咽喉科": u"jc",
    u"内镜科": u"qc",
    u"血液病科": u"ah",
    u"超声科": u"qf",
    u"麻醉科": u"qg",
    u"肿瘤内科": u"ma",
    u"呼吸内科": u"aa",
    u"普外科": u"bi",
    u"中医妇科": u"oc",
    u"体检中心": u"qh",
    u"中医男科": u"od",
    u"烧伤科": u"be",
    u"预防保健科": u"qi",
    u"神经外科": u"bc",
    u"中医外科": u"ob",
    u"介入与放疗中心": u"mc",
    u"肝胆外科": u"bd",
    u"神经内科": u"ac",
    u"精神科": u"na",
    u"肛肠科": u"bh",
    u"性病科": u"hb",
    u"病理科": u"qd",
    u"创伤科": u"cc",
    u"心脏与血管外科": u"bb",
    u"小儿科": u"fa",
    u"胸外科": u"ba",
    u"肾内科": u"ae",
    u"检验科": u"qa",
    u"感染科": u"ai",
    u"中医儿科": u"oe",
    u"心理科": u"nb",
    u"泌尿外科": u"bg",
    u"关节科": u"cb",
    u"甲状腺乳腺外科": u"bj",
    u"中医内科": u"oa",
    u"风湿免疫科": u"ag",
    u"皮肤科": u"ha",
    u"脊柱科": u"ca",
    u"放射科": u"qb",
    u"康复科": u"bf",
    u"内分泌与代谢科": u"af"
}

# 科室号到名称的映射
CLINIC_NO_TO_NAME = {
    u"1": u"妇科",
    u"2": u"儿科",
    u"3": u"内科",
    u"4": u"皮肤性病科",
    u"6": u"营养科",
    u"7": u"骨伤科",
    u"8": u"男科",
    u"9": u"外科",
    u"11": u"肿瘤及防治科",
    u"12": u"中医科",
    u"13": u"口腔颌面科",
    u"14": u"耳鼻咽喉科",
    u"15": u"眼科",
    u"16": u"整形美容科",
    u"17": u"精神心理科",
    u"19": u"基因检测科",
    u"21": u"产科",
    u"22": u"报告解读科",
    u"aa": u"呼吸内科",
    u"ab": u"心血管内科",
    u"ac": u"神经内科",
    u"ad": u"消化内科",
    u"ae": u"肾内科",
    u"af": u"内分泌与代谢科",
    u"ag": u"风湿免疫科",
    u"ah": u"血液病科",
    u"ai": u"感染科",
    u"aj": u"内科基层全科",
    u"ba": u"胸外科",
    u"bb": u"心脏与血管外科",
    u"bc": u"神经外科",
    u"bd": u"肝胆外科",
    u"be": u"烧伤科",
    u"bf": u"康复科",
    u"bg": u"泌尿外科",
    u"bh": u"肛肠科",
    u"bi": u"普外科",
    u"bj": u"甲状腺乳腺外科",
    u"bk": u"外科基层全科",
    u"ca": u"脊柱科",
    u"cb": u"关节科",
    u"cc": u"创伤科",
    u"cd": u"骨伤科基层全科",
    u"fa": u"小儿科",
    u"fb": u"新生儿科",
    u"fc": u"儿科基层全科",
    u"ha": u"皮肤科",
    u"hb": u"性病科",
    u"hc": u"皮肤科基层全科",
    u"ja": u"耳科",
    u"jb": u"鼻科",
    u"jc": u"咽喉科",
    u"jd": u"耳鼻咽喉科基层全科",
    u"ma": u"肿瘤内科",
    u"mb": u"肿瘤外科",
    u"mc": u"介入与放疗中心",
    u"md": u"肿瘤中医科",
    u"me": u"肿瘤及防治科基层全科",
    u"na": u"精神科",
    u"nb": u"心理科",
    u"nc": u"精神心理科基层全科",
    u"oa": u"中医内科",
    u"ob": u"中医外科",
    u"oc": u"中医妇科",
    u"od": u"中医男科",
    u"oe": u"中医儿科",
    u"of": u"中医科基层全科",
    u"qa": u"检验科",
    u"qb": u"放射科",
    u"qc": u"内镜科",
    u"qd": u"病理科",
    u"qe": u"心电图科",
    u"qf": u"超声科",
    u"qg": u"麻醉科",
    u"qh": u"体检中心",
    u"qi": u"预防保健科",
    u"qj": u"报告解读科基层全科"
}

# 二级科室到线上分诊科室的映射
CLINIC_NO_TO_ONLINE = {
    u"1": u"1",
    u"6": u"6",
    u"8": u"8",
    u"13": u"13",
    u"15": u"15",
    u"16": u"16",
    u"21": u"21",
    u"19": u"ab",
    u"aa": u"aa",
    u"ab": u"ab",
    u"ac": u"ac",
    u"ad": u"ad",
    u"ae": u"ae",
    u"af": u"af",
    u"ag": u"ag",
    u"ah": u"ah",
    u"ai": u"ai",
    u"ba": u"ba",
    u"bb": u"bb",
    u"bc": u"bc",
    u"bd": u"bd",
    u"be": u"be",
    u"bf": u"bf",
    u"bg": u"bg",
    u"bh": u"bh",
    u"bi": u"bi",
    u"bj": u"bj",
    u"ca": u"7",
    u"cb": u"7",
    u"cc": u"7",
    u"fa": u"fa",
    u"fb": u"fb",
    u"ha": u"ha",
    u"hb": u"hb",
    u"ja": u"14",
    u"jb": u"14",
    u"jc": u"14",
    u"ma": u"11",
    u"mb": u"11",
    u"mc": u"11",
    u"md": u"11",
    u"na": u"na",
    u"nb": u"nb",
    u"oa": u"12",
    u"ob": u"12",
    u"oc": u"12",
    u"od": u"12",
    u"oe": u"12",
    u"qa": u"22",
    u"qb": u"22",
    u"qc": u"22",
    u"qd": u"22",
    u"qe": u"22",
    u"qf": u"22",
    u"qg": u"22",
    u"qh": u"22",
    u"qi": u"22"
}

# 映射粗分科室, 37个->16
# Author: C.L. Wang
CLINIC_NO_TO_ROUGH = {
    u"1": u"1",  # -> 妇科
    u"21": u"1",  # -> 产科->妇科

    u"fa": u"2",  # -> 小儿科->儿科
    u"fb": u"2",  # -> 新生儿科->儿科
    u"6": u"2",  # -> 营养科->儿科

    u"ha": u"ha",  # -> 皮肤科, 一级科室, 皮肤性病科(4)
    u"hb": u"ha",  # -> 性病科->皮肤科
    u"16": u"ha",  # -> 整形美容科->皮肤科
    u"be": u"ha",  # -> 烧伤科->皮肤科

    u"7": u"7",  # -> 骨伤科
    u"bi": u"7",  # -> 普外科->骨伤科
    u"ba": u"7",  # -> 胸外科->骨伤科
    u"ag": u"7",  # -> 风湿免疫科->骨伤科
    u"bf": u"7",  # -> 康复科->骨伤科

    u"ad": u"ad",  # -> 消化内科
    u"ai": u"ad",  # -> 感染科->消化内科
    u"bd": u"ad",  # -> 肝胆外科->消化内科

    u"aa": u"aa",  # -> 呼吸内科
    u"14": u"aa",  # -> 耳鼻咽喉科->呼吸内科

    u"8": u"8",  # -> 男科
    u"bg": u"8",  # -> 泌尿外科->男科
    u"ae": u"8",  # -> 肾内科->男科

    u"12": u"12",  # -> 中医科

    u"ac": u"ac",  # -> 神经内科
    u"bc": u"ac",  # -> 神经外科->神经内科

    u"13": u"13",  # -> 口腔颌面科

    u"bj": u"bj",  # -> 甲状腺乳腺外科
    u"af": u"bj",  # -> 内分泌与代谢科->甲状腺乳腺外科

    u"15": u"15",  # -> 眼科

    u"ab": u"ab",  # -> 心血管内科
    u"bb": u"ab",  # -> 心脏与血管外科-> 心血管内科

    u"nb": u"17",  # -> 心理科->精神心理科
    u"na": u"17",  # -> 精神科->精神心理科

    u"22": u"22",  # -> 报告解读科
    u"11": u"22",  # -> 肿瘤及防治科->报告解读科
    u"ah": u"22",  # -> 血液病科-报告解读科

    u"bh": u"bh",  # -> 肛肠科
}

# 顶级科室列表, 16个
ROUGH_CLINIC_NO_LIST = [u'1', u'2', u"ha", u"7", u"ad", u"aa", u"8", u"12", u"ac", u"13",
                        u"bj", u"15", u"ab", u"17", u"22", u"bh"]

# 粗分科室的复合科室, 12个, 去掉中医科\口腔颌面科\眼科\肛肠科
ROUGH_CMP_CLINIC_NO_LIST = [u"1", u"2", u"ha", u"7", u"ad", u"aa",
                            u"8", u"ac", u"bj", u"ab", u"17", u"22"]

# 线上科室列表, 37个
ONLINE_CLINIC_NO_LIST = [u'1', u'21',
                         u'fa', u'fb', u'6',
                         u'ha', u'hb', u'16', u'be',
                         u'7', u'bi', u'ba', u'ag', u'bf',
                         u'ad', u'ai', u'bd',
                         u'aa', u'14',
                         u'8', u'bg', u'ae',
                         u'12',
                         u'ac', u'bc',
                         u'13',
                         u'bj', u'af',
                         u'15',
                         u'ab', u'bb',
                         u'nb', u'na',
                         u'22', u'11', u'ah',
                         u'bh']

# 二级科室59个，标准，增加骨伤科和耳鼻咽喉科
CLINIC_NO_LIST = ["1", "6", "7", "8", "13", "14", "15", "16", "21", "19",
                  "aa", "ab", "ac", "ad", "ae", "af", "ag", "ah", "ai", "ba",
                  "bb", "bc", "bd", "be", "bf", "bg", "bh", "bi", "bj", "ca",
                  "cb", "cc", "fa", "fb", "ha", "hb", "ja", "jb", "jc", "ma",
                  "mb", "mc", "md", "na", "nb", "oa", "ob", "oc", "od", "oe",
                  "qa", "qb", "qc", "qd", "qe", "qf", "qg", "qh", "qi"]

IMG_STATE_ALL_LIST = ['empty', 'has_image']
SEX_ALL_LIST = [u'男', u'女', u'无性']
AGE_ALL_LIST = [u'新生儿', u'小儿', u'少年', u'青年', u'中年', u'老年', u'无年龄']

# 一级科室18个
FIRST_CLINICS = ["1", "2", "3", "4", "6", "7", "8", "9", "11", "12",
                 "13", "14", "15", "16", "17", "21", "19", "22"]

# 二级科室49个
SECOND_CLINICS = ["aa", "ab", "ac", "ad", "ae", "af", "ag", "ah", "ai", "ba",
                  "bb", "bc", "bd", "be", "bf", "bg", "bh", "bi", "bj", "ca",
                  "cb", "cc", "fa", "fb", "ha", "hb", "ja", "jb", "jc", "ma",
                  "mb", "mc", "md", "na", "nb", "oa", "ob", "oc", "od", "oe",
                  "qa", "qb", "qc", "qd", "qe", "qf", "qg", "qh", "qi"]


class ClinicUtils(object):
    @classmethod
    def clinic_no_to_rough(cls, clinic_no):
        """
        将科室号转换为训练分诊使用的科室号
        """
        online_no = clinic_no
        if clinic_no in CLINIC_NO_TO_ONLINE:
            online_no = CLINIC_NO_TO_ONLINE[clinic_no]  # 先转换为线上科室

        if online_no in CLINIC_NO_TO_ROUGH:
            return CLINIC_NO_TO_ROUGH[online_no]  # 再转换为粗分科室
        else:
            return clinic_no

    @classmethod
    def clinic_no_to_online(cls, clinic_no):
        """
        将科室号转换为线上分诊使用的科室号
        """
        if clinic_no in CLINIC_NO_TO_ONLINE:
            return CLINIC_NO_TO_ONLINE[clinic_no]
        else:
            return clinic_no

    @classmethod
    def clinic_no_to_name(cls, clinic_no):
        """
        将科室号转换为科室名
        """
        return CLINIC_NO_TO_NAME.get(clinic_no, u"")

    @classmethod
    def clinic_name_to_no(cls, name):
        """
        将科室号转换为科室名
        """
        return CLINIC_NAME_TO_NO.get(name, u"")

    @classmethod
    def get_rough_list(cls, clinic):
        """
        获取粗分科室集合
        :param clinic: 科室
        :return: 粗分科室集合
        """
        rough_list = list()
        for k, v in CLINIC_NO_TO_ROUGH.iteritems():
            if v == clinic:
                rough_list.append(k)
        return rough_list

    @classmethod
    def get_similar_clinics(cls, clinic):
        similar_clinics = list()

        # 映射为线上分诊科室, 并添加相似科室
        if clinic not in CLINIC_NO_TO_ROUGH:
            clinic = CLINIC_NO_TO_ONLINE[clinic]
            similar_clinics.append(clinic)

        # 获取粗分科室
        rough_clinic = CLINIC_NO_TO_ROUGH[clinic]

        # 加入粗分科室
        if rough_clinic != clinic:
            similar_clinics.append(rough_clinic)

        # 再加入粗分科室下的子科室
        for key, value in CLINIC_NO_TO_ROUGH.iteritems():
            if value == rough_clinic and key != value and key != clinic:
                similar_clinics.append(key)

        return similar_clinics


if __name__ == '__main__':
    print ClinicUtils.clinic_no_to_rough(u'11')
