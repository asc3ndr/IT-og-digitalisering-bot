#!/usr/bin/python3
from discord import activity
from pymongo import MongoClient
from datetime import datetime


TIME = lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class DigitDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.digit
        self.users = self.db.users
        self.courses = self.db.courses

        self.GUILD_ID = 685429376413597698
        self.WELCOME_CHANNEL_ID = 751175612671983646
        self.WELCOME_CHANNEL_MSG_ID = 751175811033333843
        self.NEWS_CHANNEL_ID = 686318504924020737
        self.DEV_CHANNEL_ID = 751435998935777401

    def add_course(
        self,
        _id: int,
        canvas: str,
        name: str,
        icon: str,
        role: str,
        token: str,
        channel_id: int,
        task_channel_id: int,
        announcement_channel_id: int,
        announcements=[],
        active=True,
    ):
        schema = {
            "_id": _id,
            "canvas": canvas,
            "name": name,
            "icon": icon,
            "role": role,
            "token": token,
            "channel_id": channel_id,
            "task_channel_id": task_channel_id,
            "announcement_channel_id": announcement_channel_id,
            "announcements": announcements,
            "active": active,
        }
        if not self.courses.find_one({"_id": _id}):
            return self.courses.insert_one(schema)
        return None

    def get_all_courses(self, key="") -> list:
        cursor = self.courses.find({})

        if not key == "":
            return [course[key] for course in cursor]
        return [course for course in cursor]

    def get_one_course(self, key: str, identifier: str) -> dict:
        return self.courses.find_one({key: identifier})

    def add_course_announcement(self, canvas: str, announcement_id: int) -> dict:
        return self.courses.update_one(
            {"canvas": canvas}, {"$push": {"announcements": announcement_id}}
        )

    def toggle_course_activity(self, role: str):
        if self.get_one_course("role", role)["active"]:
            print(f"[{TIME()}]\t{role.upper()} set to INACTIVE")
            return self.courses.update_one({"role": role}, {"$set": {"active": False}})
        elif not self.get_one_course("role", role)["active"]:
            print(f"[{TIME()}]\t{role.upper()} set to ACTIVE")
            return self.courses.update_one({"role": role}, {"$set": {"active": True}})

    def set_attr(self, filter: str, identifier: str, key: str, value):
        try:
            self.courses.update_one({filter: identifier}, {"$set": {key: value}})
        except:
            pass


if __name__ == "__main__":

    drop = True
    if drop:

        MongoClient("mongodb://localhost:27017/").drop_database("digit")

        x = DigitDB()

        x.add_course(
            1,
            "1141",
            "Bachelor i IT og digitalisering",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            0,
            686318504924020737,
            [
                20279,
                20037,
                20344,
                20584,
                20686,
                20735,
                21391,
                21450,
                21504,
                21703,
                21787,
                22154,
                22390,
                23778,
                23911,
                25700,
                25743,
                25782,
                25933,
            ],
            True,
        )

        x.add_course(
            2,
            "1140",
            "Bachelor i IT og digitalisering - 2019/22",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            0,
            686318504924020737,
            [],
            True,
        )

        x.add_course(
            3,
            "69",
            "Avdelingene for logistikk, \u00f8konomi og samfunnsfag",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            0,
            686318504924020737,
            [],
            True,
        )

        x.add_course(
            4,
            "65",
            "HiMolde Student Info",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            0,
            686318504924020737,
            [
                19588,
                19511,
                19440,
                19246,
                19244,
                19929,
                19930,
                19934,
                19935,
                19936,
                20138,
                20139,
                20839,
                21023,
                21024,
                21074,
                21075,
                21184,
                21250,
                21379,
                21393,
                21599,
                21603,
                21641,
                21651,
                21670,
                22042,
                22093,
                22094,
                22143,
                22148,
                22268,
                22346,
                22373,
                22591,
                22592,
                22682,
                22697,
                22894,
                22941,
                22942,
                22945,
                22984,
                22991,
                23123,
                23222,
                23336,
                23854,
                23859,
                23891,
                23987,
                23985,
                24149,
                24134,
                24097,
                24355,
                24437,
                24540,
                24659,
                24692,
                24719,
                24933,
                25069,
                25264,
                25281,
                25283,
                25285,
                25750,
                25777,
                25977,
                26014,
                26016,
            ],
            True,
        )

        x.add_course(
            5,
            "",
            "Practical Programming",
            "💻",
            "IBE151",
            "",
            747889611396612211,
            752619885745406074,
            760844593087643678,
            [],
            True,
        )

        x.add_course(
            6,
            "",
            "Information Technology",
            "🤖",
            "IBE110",
            "",
            747889362863259719,
            753524870947667968,
            760844694875275274,
            [],
            True,
        )

        x.add_course(
            7,
            "",
            "Forretningsprosesser",
            "📚",
            "IBE430",
            "",
            747890012045049990,
            753525998473183273,
            760844804325900288,
            [],
            True,
        )

        x.add_course(
            8,
            "",
            "Extended Reality",
            "🥽",
            "IBE320",
            "",
            747888306179670046,
            760560953821102121,
            760844292662624276,
            [],
            True,
        )

        x.add_course(
            9,
            "",
            "Matematikk",
            "🧮",
            "MAT100",
            "",
            747888102709919855,
            760838516342652938,
            760845435752677436,
            [],
            True,
        )

        x.add_course(
            10,
            "",
            "Agile Methods",
            "🎪",
            "IBE205",
            "",
            751178938323304469,
            760838010115325994,
            760844921325355050,
            [],
            True,
        )

        x.add_course(
            11,
            "",
            "Webutvikling",
            "🐵",
            "IBE102",
            "",
            685437347181101078,
            760839761820385280,
            760845116423274497,
            [
                22338,
                22271,
                22528,
                22550,
                23290,
                23499,
                23832,
                23851,
                23866,
                24125,
                24352,
                24544,
                24626,
                24696,
                24723,
                24893,
                24918,
                25094,
                25317,
                25790,
                25789,
                25785,
                25856,
                25857,
                25997,
            ],
            True,
        )

        x.add_course(
            12,
            "",
            "Virksomhetsdata",
            "📱",
            "IBE120",
            "",
            685437536637943819,
            760840286565040178,
            760845220610441236,
            [
                22494,
                22695,
                23106,
                23108,
                23131,
                23357,
                23415,
                23593,
                23712,
                23717,
                23847,
                23921,
                24062,
                24154,
                24153,
                24152,
                24221,
                24397,
                24577,
                24881,
                24880,
                24950,
                24949,
                25077,
                25207,
                25229,
                25786,
            ],
            True,
        )

        x.add_course(
            13,
            "",
            "Database",
            "🐧",
            "IBE211",
            "",
            685437701411045404,
            760839325398335529,
            760845011167608832,
            [
                22339,
                22252,
                22605,
                23321,
                23835,
                24674,
                25034,
                25041,
                25219,
                25316,
                25324,
                25638,
                25935,
            ],
            True,
        )

        x.add_course(
            14,
            "",
            "e-Business",
            "🌎",
            "LOG206",
            "",
            685437749301739520,
            760840801604599872,
            760845340323872838,
            [
                22329,
                22251,
                22413,
                22527,
                22536,
                22584,
                22723,
                23526,
                23701,
                23723,
                24215,
                24253,
                24400,
                24457,
                24596,
                24633,
                24945,
                25108,
                25129,
                25193,
                25868,
            ],
            True,
        )

        x.add_course(
            15,
            "",
            "Statistikk II",
            "💢",
            "MAT210",
            "",
            792789373510877195,
            792789061554929686,
            792788710180519956,
            [22786, 24282, 24283, 24463, 24837, 25235, 25974],
            True,
        )

        x.add_course(
            16,
            "",
            "Statistikk I",
            "💀",
            "MAT110",
            "",
            792940285629169714,
            792940176246046760,
            792939915239358474,
            [
                22666,
                22665,
                22655,
                22609,
                22556,
                22508,
                22465,
                22427,
                22698,
                22774,
                22775,
                22785,
                22825,
                22855,
                22908,
                22911,
                22913,
                22966,
                22986,
                23018,
                23035,
                23039,
                23066,
                23127,
                23194,
                23230,
                23316,
                23359,
                23404,
                23479,
                23482,
                23498,
                23548,
                23765,
                23774,
                23813,
                23869,
                23961,
                24187,
                24108,
                24102,
                24273,
                24331,
                24473,
                24474,
                24475,
                24484,
                24520,
                24708,
                24793,
                24807,
                24819,
                24889,
                25176,
                25336,
                25761,
                25766,
                25765,
                25784,
                25787,
                25798,
                25799,
                25803,
                25859,
            ],
            True,
        )

        x.add_course(
            17,
            "",
            "Mikro\u00f8konomi",
            "📈",
            "S\u00D8K200",
            "",
            792790466470084619,
            792790366385602560,
            792790324849541170,
            [
                22355,
                22567,
                22676,
                22677,
                22754,
                22809,
                22811,
                22882,
                23025,
                23093,
                23094,
                23209,
                23274,
                23428,
                23429,
                23462,
                23537,
                23564,
                23700,
                23899,
                23969,
                24037,
                24006,
                24082,
                24235,
                24455,
                24553,
                24554,
                24643,
                24732,
                24759,
                24920,
                24962,
                25021,
                25200,
                25308,
                25348,
                25349,
                25550,
                25731,
                25888,
            ],
            True,
        )

        x.add_course(
            18,
            "",
            "Innkj\u00f8psledelse",
            "💵",
            "LOG505",
            "",
            799317956378492930,
            799317873638113380,
            799317753348751360,
            [
                22711,
                22626,
                22531,
                22497,
                22842,
                22935,
                23234,
                23480,
                23514,
                23601,
                23602,
                23823,
                23970,
                24036,
                24192,
                24174,
                24147,
                24259,
                24337,
                24502,
                24705,
                24730,
                24877,
                24876,
                25074,
                25243,
                25685,
                25715,
                25876,
            ],
            True,
        )

        x.add_course(
            19,
            "",
            "Lager og Produksjon",
            "🚚",
            "SCM200",
            "",
            805542267619508265,
            805540151203594280,
            805539875851730954,
            [],
            True,
        )

    # Show Results
    # a = x.get_all_courses()
    # for course in a:
    #     print(course)
