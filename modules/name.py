#!/usr/bin/env python3

import json
import sys
import os
from datetime import datetime
from io import BytesIO
from os.path import isfile
from pathlib import Path
from pprint import pprint
from colorama import init, Fore, Back, Style


import httpx
from PIL import Image
from geopy.geocoders import Nominatim

import config
from lib.banner import banner
import lib.gmaps as gmaps
import lib.youtube as ytb
from lib.utils import *
from unidecode import unidecode

structure = ["first!!", "f!!last!!", "f!!.last!!", "f!!_last!!", "last!!f!!", "last!!.f!!", "last!!_f!!", "l!!first!!",
             "l!!.first!!", "l!!_first!!", "first!!l!!", "first!!.l!!", "first!!_l!!", "last!!first!!",
             "last!!.first!!", "last!!_first!!", "first!!last!!", "first!!.last!!", "first!!_last!!", "first!!last!!1",
             "first!!last!!.1", "f!!last!!1", "f!!last!!.1", "first!!.last!!1", "first!!.last!!.1", "first!!last!!2",
             "first!!last!!.2", "f!!last!!2", "f!!last!!.2", "first!!.last!!2", "first!!.last!!.2"]


def prepare_emails(name, domain="gmail.com", birth_input=""):
    if birth_input:
        structure.append("last!!first!!" + birth_input)
        structure.append("first!!last!!" + birth_input)
        structure.append("f!!last!!" + birth_input)
        structure.append("f!!.last!!" + birth_input)
        structure.append("f!!_last!!" + birth_input)
        structure.append("first!!.l!!" + birth_input)
        structure.append("first!!_l!!" + birth_input)
        structure.append("last!!.first!!" + birth_input)
        structure.append("first!!.last!!" + birth_input)
        structure.append("last!!_first!!" + birth_input)
        structure.append("first!!_last!!" + birth_input)
        structure.append("last!!first!!" + birth_input[2:])
        structure.append("first!!last!!" + birth_input[2:])
        structure.append("f!!last!!" + birth_input[2:])
        structure.append("f!!.last!!" + birth_input[2:])
        structure.append("f!!_last!!" + birth_input[2:])
        structure.append("first!!.l!!" + birth_input[2:])
        structure.append("first!!_l!!" + birth_input[2:])
        structure.append("last!!.first!!" + birth_input[2:])
        structure.append("first!!.last!!" + birth_input[2:])
        structure.append("last!!_first!!" + birth_input[2:])
        structure.append("first!!_last!!" + birth_input[2:])
        structure.append("last!!first!!." + birth_input)
        structure.append("first!!last!!." + birth_input)
        structure.append("f!!last!!." + birth_input)
        structure.append("f!!.last!!." + birth_input)
        structure.append("f!!_last!!." + birth_input)
        structure.append("first!!.l!!." + birth_input)
        structure.append("first!!_l!!." + birth_input)
        structure.append("last!!.first!!." + birth_input)
        structure.append("first!!.last!!." + birth_input)
        structure.append("last!!_first!!." + birth_input)
        structure.append("first!!_last!!." + birth_input)
        structure.append("last!!first!!_" + birth_input)
        structure.append("first!!last!!_" + birth_input)
        structure.append("f!!last!!_" + birth_input)
        structure.append("f!!.last!!_" + birth_input)
        structure.append("f!!_last!!_" + birth_input)
        structure.append("first!!.l!!_" + birth_input)
        structure.append("first!!_l!!_" + birth_input)
        structure.append("last!!.first!!_" + birth_input)
        structure.append("first!!.last!!_" + birth_input)
        structure.append("last!!_first!!_" + birth_input)
        structure.append("first!!_last!!_" + birth_input)
        structure.append("last!!first!!." + birth_input[2:])
        structure.append("first!!last!!." + birth_input[2:])
        structure.append("f!!last!!." + birth_input[2:])
        structure.append("f!!.last!!." + birth_input[2:])
        structure.append("f!!_last!!." + birth_input[2:])
        structure.append("first!!.l!!." + birth_input[2:])
        structure.append("first!!_l!!." + birth_input[2:])
        structure.append("last!!.first!!." + birth_input[2:])
        structure.append("first!!.last!!." + birth_input[2:])
        structure.append("last!!_first!!." + birth_input[2:])
        structure.append("first!!_last!!." + birth_input[2:])
        structure.append("last!!first!!_" + birth_input[2:])
        structure.append("first!!last!!_" + birth_input[2:])
        structure.append("f!!last!!_" + birth_input[2:])
        structure.append("f!!.last!!_" + birth_input[2:])
        structure.append("f!!_last!!_" + birth_input[2:])
        structure.append("first!!.l!!_" + birth_input[2:])
        structure.append("first!!_l!!_" + birth_input[2:])
        structure.append("last!!.first!!_" + birth_input[2:])
        structure.append("first!!.last!!_" + birth_input[2:])
        structure.append("last!!_first!!_" + birth_input[2:])
        structure.append("first!!_last!!_" + birth_input[2:])

    possible_emails = []
    splitted_name = name.split(" ")
    first_name = unidecode(splitted_name[0].lower())
    last_name = unidecode(splitted_name[1].lower())

    found_first = False
    found_last = False
    for x in structure:
        if x.find("first!!") != -1:
            x = x.replace("first!!", first_name)
            found_first = True
        if x.find("last!!") != -1:
            x = x.replace("last!!", last_name)
            found_last = True
        if x.find("f!!") != -1:
            x = x.replace("f!!", first_name[0])
        if x.find("l!!") != -1:
            x = x.replace("l!!", last_name[0])
        possible_emails.append(x + "@" + domain)

    return possible_emails


def bruteforce_email(name, client, hangouts_auth,
                     hangouts_token, cookies):
    possible_emails = prepare_emails(name)


    for email in possible_emails:
        data = is_email_google_account(client, hangouts_auth, cookies, email,
                                       hangouts_token)

        if data:
            for match in data['matches']:
                # print(match['personId'][0])
                print( Fore.GREEN + email + Fore.RESET)
                # return match['lookupId']
        else:
            print(Fore.RED + email + Fore.RESET)

    return ""

def name_hunt(name):
    banner()

    if not name:
        exit("Please give a valid name.")

    if not isfile(config.data_path):
        exit("Please generate cookies and tokens first, with the check_and_gen.py script.")

    internal_auth = ""
    internal_token = ""

    cookies = {}

    with open(config.data_path, 'r') as f:
        out = json.loads(f.read())
        internal_auth = out["internal_auth"]
        internal_token = out["keys"]["internal"]
        cookies = out["cookies"]
        hangouts_auth = out["hangouts_auth"]
        hangouts_token = out["keys"]["hangouts"]

    client = httpx.Client(cookies=cookies, headers=config.headers)

    is_within_docker = within_docker()
    if is_within_docker:
        print("[+] Docker detected, profile pictures will not be saved.")

    geolocator = Nominatim(user_agent="nominatim")

    # get name & other info
    print("Trying to find email...")
    email_based_on_gaiaid = bruteforce_email(name=name, client=client, hangouts_auth=hangouts_auth,
                     hangouts_token=hangouts_token, cookies=cookies)