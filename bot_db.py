#!/usr/bin/python3
from pymongo import MongoClient

# from Crypto.Cipher import AES

# key = b"Sixteen byte key"
# cipher = AES.new(key, AES.MODE_EAX)
# nonce = cipher.nonce
# ciphertext, tag = cipher.encrypt_and_digest(b"THEPASSWORD")
# print(nonce, ciphertext, tag)

# cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
# plaintext = cipher.decrypt(ciphertext)
# try:
#     cipher.verify(tag)
#     print("The message is authentic:", plaintext.decode("utf-8"))
# except ValueError:
#     print("Key incorrect or message corrupted")


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
            753524870947667968,
            752619885745406074,
            753525998473183273,
            760560953821102121,
            760838010115325994,
            760839325398335529,
            760839761820385280,
            760840286565040178,
            760840801604599872,
            760838516342652938,
            792790366385602560,
            792789061554929686,
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

    MongoClient("mongodb://localhost:27017/").drop_database("digit")

    # Initialize
    x = DigitDB()

    # Bachelor i IT og digitalisering
    x.add_course(
        1141,
        "Bachelor i IT og digitalisering",
        "🐋",
        "Student",
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
        ],
    )
    # Bachelor i IT og digitalisering - 2019/22
    x.add_course(
        1140,
        "Bachelor i IT og digitalisering - 2019/22",
        "🐋",
        "Student",
        685434530193997834,
        686318504924020737,
    )
    # Avdelingene for logistikk, økonomi og samfunnsfag
    x.add_course(
        69,
        "Avdelingene for logistikk, \u00f8konomi og samfunnsfag",
        "🐋",
        "Student",
        685434530193997834,
        686318504924020737,
    )
    # HiMolde Student Info
    x.add_course(
        65,
        "HiMolde Student Info",
        "🐋",
        "Student",
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
        ],
    )

    ### 1 YEAR ###
    # Webutvikling
    x.add_course(
        1, "Webutvikling", "🐵", "IBE102", 685437347181101078, 760845116423274497,
    )
    # Virksomhetsdata
    x.add_course(
        2, "Virksomhetsdata", "🐓", "IBE120", 685437536637943819, 760845220610441236,
    )
    # Databaser
    x.add_course(
        3, "Database", "🐧", "IBE211", 685437701411045404, 760845011167608832,
    )
    # e-Business
    x.add_course(
        4, "e-Business", "🍌", "LOG206", 685437749301739520, 760845340323872838,
    )

    ### 2 YEAR ###
    # Statistikk II
    x.add_course(
        1904, "Statistikk II", "🍎", "MAT210", 792789373510877195, 792788710180519956,
    )
    # Statistikk I
    x.add_course(
        5, "Statistikk I", "🐙", "MAT200", 792940285629169714, 792939915239358474,
    )
    # Mikroøkonomi
    x.add_course(
        1861,
        "Mikro\u00f8konomi",
        "🍡",
        "S\u00D8K200",
        792790466470084619,
        792790324849541170,
    )

    # Show Results
    # a = x.get_all_courses()
    # for course in a:
    #     print(course)
