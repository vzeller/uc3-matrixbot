from os import environ as env
from dokuwiki import DokuWiki, DokuWikiError
import struct
import asyncio
import wiki_pw
import json
import os
import sys
from typing import Optional

from nio import AsyncClient, ClientConfig, InviteEvent, LoginResponse, MatrixRoom, RoomMessageText, crypto

import botconf

STORE_FOLDER = "data/"
SESSION_DETAILS_FILE = "credentials.json"


# This client stores login credentials into SESSION_DETAILS_FILE.
class CustomEncryptedClient(AsyncClient):
    def __init__(
        self,
        homeserver,
        user="",
        device_id="",
        store_path="",
        config=None,
        ssl=None,
        proxy=None,
    ):
        # Calling super.__init__ means we're running the __init__ method
        # defined in AsyncClient, which this class derives from. That does a
        # bunch of setup for us automatically
        super().__init__(
            homeserver,
            user=user,
            device_id=device_id,
            store_path=store_path,
            config=config,
            ssl=ssl,
            proxy=proxy,
        )

        # if the store location doesn't exist, we'll make it
        if store_path and not os.path.isdir(store_path):
            os.mkdir(store_path)

    async def login(self) -> None:
        """Log in either using credentials or (if possible) using the
        session details file.
        """
        # Restore the previous session if we can
        # See the "restore_login.py" example if you're not sure how this works
        if os.path.exists(SESSION_DETAILS_FILE) and os.path.isfile(
            SESSION_DETAILS_FILE
        ):
            try:
                with open(SESSION_DETAILS_FILE, "r") as f:
                    config = json.load(f)
                    self.access_token = config["access_token"]
                    self.user_id = config["user_id"]
                    self.device_id = config["device_id"]

                    # This loads our verified/blacklisted devices and our keys
                    self.load_store()
                    print(
                        f"Logged in using stored credentials: {self.user_id} on {self.device_id}"
                    )

            except IOError as err:
                print(f"Couldn't load session from file. Logging in. Error: {err}")
            except json.JSONDecodeError:
                print("Couldn't read JSON file; overwriting")

        # We didn't restore a previous session, so we'll log in with a password
        if not self.user_id or not self.access_token or not self.device_id:
            # this calls the login method defined in AsyncClient from nio
            resp = await super().login(botconf.password)

            if isinstance(resp, LoginResponse):
                print("Logged in using a password; saving details to disk")
                self.__write_details_to_disk(resp)
            else:
                print(f"Failed to log in: {resp}")
                sys.exit(1)

    def trust_devices(self, user_id: str, device_list: Optional[str] = None) -> None:
        """Trusts the devices of a user.
        If no device_list is provided, all of the users devices are trusted. If
        one is provided, only the devices with IDs in that list are trusted.
        Arguments:
            user_id {str} -- the user ID whose devices should be trusted.
        Keyword Arguments:
            device_list {Optional[str]} -- The full list of device IDs to trust
                from that user (default: {None})
        """

        print(f"{user_id}'s device store: {self.device_store[user_id]}")

        # The device store contains a dictionary of device IDs and known
        # OlmDevices for all users that share a room with us, including us.

        # We can only run this after a first sync. We have to populate our
        # device store and that requires syncing with the server.
        for device_id, olm_device in self.device_store[user_id].items():
            if device_list and device_id not in device_list:
                # a list of trusted devices was provided, but this ID is not in
                # that list. That's an issue.
                print(
                    f"Not trusting {device_id} as it's not in {user_id}'s pre-approved list."
                )
                continue

            if user_id == self.user_id and device_id == self.device_id:
                # skip own device
                continue

            self.verify_device(olm_device)
            print(f"Trusting {device_id} from user {user_id}")


    @staticmethod
    def __write_details_to_disk(resp: LoginResponse) -> None:
        """Writes login details to disk so that we can restore our session later
        without logging in again and creating a new device ID.
        Arguments:
            resp {LoginResponse} -- the successful client login response.
        """
        with open(SESSION_DETAILS_FILE, "w") as f:
            json.dump(
                {
                    "access_token": resp.access_token,
                    "device_id": resp.device_id,
                    "user_id": resp.user_id,
                },
                f,
            )


class Callbacks:
    wiki = DokuWiki('https://wiki.muc.ccc.de', 'spyderman', 'Your_Friendly_Neighbourhood_Passord',cookieAuth=True)
# bytearray(str(wiki_pw),'utf-8'), cookieAuth=True)
# https://www.dokuwiki.org/plugin:struct:remote_api
# https://python-dokuwiki.readthedocs.io/en/latest/#structs

    wiki.structs.get_data('workshop:python')
#wiki.structs.get_data('workshop:python', 'event')
#wiki.structs.get_aggregation_data(['event'], ['name', 'startDate'])

    global data

    data = wiki.structs.get_aggregation_data(
        ['event'], 
        ['name', 'startDate'], 
        [{'condition': 'event.startDate >= $TODAY$'}], 
        'event.startDate'
    )
    def __init__(self, client: AsyncClient):
        self.client = client
    async def message_callback(self, room: MatrixRoom, event: RoomMessageText) -> None:
        if event.sender == botconf.mxid:
            return
        if event.body[0] == "!":
#            await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": "teststring"},ignore_unverified_devices=True)
            if event.body[1:5] == "help":
                await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": "Im a matrix bot. For help contact B4ckBOne. ZZ"},ignore_unverified_devices=True)
            if event.body[1:5] == "root":
                await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": "root"},ignore_unverified_devices=True)
            if event.body[1:5] == "root":
                await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": "root"},ignore_unverified_devices=True)
            if event.body[1:5] == "root":
                await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": "root"},ignore_unverified_devices=True)
            global data
            if event.body[1:6] == "heute":
                await self.client.room_send(room_id=room.room_id,message_type="m.room.message",content={"msgtype": "m.text", "body": str(data)},ignore_unverified_devices=True)

#        await self.client.room_send(
#            room_id=room.room_id,dotfiles
#            message_type="m.room.message",
#            content={"msgtype": "m.text", "body": event.body},
#            ignore_unverified_devices=True,
#        )

    async def invite_callback(self, room: MatrixRoom, sender):
        print(f"received invite for {room.room_id}")
        await self.client.join(room.room_id)


async def main() -> None:
    config = ClientConfig(store_sync_tokens=True)
    client = CustomEncryptedClient(
        botconf.homeserver,
        botconf.mxid,
        store_path=STORE_FOLDER,
        config=config,
    )

    await client.login()
    
    callbacks = Callbacks(client)
    client.add_event_callback(callbacks.message_callback, RoomMessageText)
    client.add_event_callback(callbacks.invite_callback, InviteEvent)

    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.get_event_loop().run_until_complete(main())
