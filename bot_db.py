#!/usr/bin/python3
from pymongo import MongoClient


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
        self.COURSE_TASK_CHANNEL_IDS = [
            753524870947667968,  # Information Technology
            752619885745406074,  # Practical Programming
            753525998473183273,  # Forretningsprosesser
            760560953821102121,  # Virtuel Virkelighet
            760838010115325994,  # Agile Methods
            760839325398335529,  # Databaser
            760839761820385280,  # Webutvikling
            760840286565040178,  # Virksomhetsdata
            760840801604599872,  # E-Business
            760838516342652938,  # Matematikk
            792790366385602560,  # Mikroøkonomi
            792789061554929686,  # Statistikk 2
            792940176246046760,  # Statistikk 1
            799317873638113380,  # Innkjøpsledelse og Forhandlinger
        ]

    def add_user(self, _id):
        schema = {"_id": _id}
        if not self.users.find_one(schema):
            return self.users.insert_one(schema)
        return None

    def get_user(self, filter: str, identifier: str):
        return self.users.find_one({filter: identifier})

    def add_course(
        self,
        _id: int,
        name: str,
        icon: str,
        role: str,
        token: str,
        channel_id: int,
        announcement_channel_id: int,
        announcements=[],
        active=True,
    ):
        schema = {
            "_id": _id,
            "name": name,
            "icon": icon,
            "role": role,
            "token": token,
            "channel_id": channel_id,
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
        return self.courses.find_one({filter: identifier})

    def add_course_announcement(self, _id, announcement_id: int) -> dict:
        return self.courses.update_one(
            {"_id": _id}, {"$push": {"announcements": announcement_id}}
        )

    def set_course_activity(self, _id, state):
        return self.courses.update_one({"_id": _id}, {"$set", {"active": state}})


if __name__ == "__main__":

    drop = False
    if drop:

        MongoClient("mongodb://localhost:27017/").drop_database("digit")

        # Initialize
        x = DigitDB()

        # Bachelor i IT og digitalisering
        x.add_course(
            1141,
            "Bachelor i IT og digitalisering",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
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
            ],
        )
        # Bachelor i IT og digitalisering - 2019/22
        x.add_course(
            1140,
            "Bachelor i IT og digitalisering - 2019/22",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            686318504924020737,
        )
        # Avdelingene for logistikk, økonomi og samfunnsfag
        x.add_course(
            69,
            "Avdelingene for logistikk, \u00f8konomi og samfunnsfag",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
            686318504924020737,
        )
        # HiMolde Student Info
        x.add_course(
            65,
            "HiMolde Student Info",
            "🐋",
            "Student",
            "AMR",
            685434530193997834,
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
            ],
        )

        ### 1 YEAR ###
        # Webutvikling
        x.add_course(
            1906,
            "Webutvikling",
            "🐵",
            "IBE102",
            "SIG",
            685437347181101078,
            760845116423274497,
            [22338, 22271, 22528, 22550],
        )
        # Virksomhetsdata
        x.add_course(
            1925,
            "Virksomhetsdata",
            "🐓",
            "IBE120",
            "SIG",
            685437536637943819,
            760845220610441236,
            [22494, 22695],
        )
        # Databaser
        x.add_course(
            1913,
            "Database",
            "🐧",
            "IBE211",
            "SIG",
            685437701411045404,
            760845011167608832,
            [22339, 22252, 22605],
        )
        # e-Business
        x.add_course(
            1944,
            "e-Business",
            "🍌",
            "LOG206",
            "SIG",
            685437749301739520,
            760845340323872838,
            [22329, 22251, 22413, 22527, 22536, 22584, 22723],
        )

        ### 2 YEAR ###
        # Statistikk II
        x.add_course(
            1904,
            "Statistikk II",
            "🍎",
            "MAT210",
            "AMR",
            792789373510877195,
            792788710180519956,
            [22786],
        )
        # Statistikk I
        x.add_course(
            1901,
            "Statistikk I",
            "🐙",
            "MAT110",
            "AMR",
            792940285629169714,
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
            ],
        )
        # Mikroøkonomi
        x.add_course(
            1861,
            "Mikro\u00f8konomi",
            "🍡",
            "S\u00D8K200",
            "AMR",
            792790466470084619,
            792790324849541170,
            [22355, 22567, 22676, 22677, 22754],
        )
        # Innkjøpsledelse og Forhandlinger
        x.add_course(
            1835,
            "Innkj\u00f8psledelse",
            "💸",
            "LOG505",
            "KNU",
            799317956378492930,
            799317753348751360,
            [22711, 22626, 22531, 22497],
        )
        # Lager og Produksjonsplanlegging
        x.add_course(
            1918,
            "Lager og Produksjon",
            "🚚",
            "SCM200",
            "",
            805542267619508265,
            805539875851730954,
        )

    # Show Results
    # a = x.get_all_courses()
    # for course in a:
    #     print(course)
