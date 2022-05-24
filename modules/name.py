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

structure = ["first!!last!!2", "first!!last!!.2", "f!!last!!2", "f!!last!!.2", "first!!.last!!2", "first!!.last!!.2", "first!!last!!12", "first!!last!!.12", "f!!last!!12", "f!!last!!.12", "first!!.last!!12", "first!!.last!!.12", "first!!last!!22", "first!!last!!.22", "f!!last!!22", "f!!last!!.22", "first!!.last!!22", "first!!.last!!.22", "first!!last!!32", "first!!last!!.32", "f!!last!!32", "f!!last!!.32", "first!!.last!!32", "first!!.last!!.32", "first!!last!!42", "first!!last!!.42", "f!!last!!42", "f!!last!!.42", "first!!.last!!42", "first!!.last!!.42", "first!!last!!52", "first!!last!!.52", "f!!last!!52", "f!!last!!.52", "first!!.last!!52", "first!!.last!!.52", "first!!last!!62", "first!!last!!.62", "f!!last!!62", "f!!last!!.62", "first!!.last!!62", "first!!.last!!.62", "first!!last!!72", "first!!last!!.72", "f!!last!!72", "f!!last!!.72", "first!!.last!!72", "first!!.last!!.72", "first!!last!!82", "first!!last!!.82", "f!!last!!82", "f!!last!!.82", "first!!.last!!82", "first!!.last!!.82", "first!!last!!92", "first!!last!!.92", "f!!last!!92", "f!!last!!.92", "first!!.last!!92", "first!!.last!!.92", "first!!last!!102", "first!!last!!.102", "f!!last!!102", "f!!last!!.102", "first!!.last!!102", "first!!.last!!.102", "first!!last!!112", "first!!last!!.112", "f!!last!!112", "f!!last!!.112", "first!!.last!!112", "first!!.last!!.112", "first!!last!!122", "first!!last!!.122", "f!!last!!122", "f!!last!!.122", "first!!.last!!122", "first!!.last!!.122", "first!!last!!132", "first!!last!!.132", "f!!last!!132", "f!!last!!.132", "first!!.last!!132", "first!!.last!!.132", "first!!last!!142", "first!!last!!.142", "f!!last!!142", "f!!last!!.142", "first!!.last!!142", "first!!.last!!.142", "first!!last!!152", "first!!last!!.152", "f!!last!!152", "f!!last!!.152", "first!!.last!!152", "first!!.last!!.152", "first!!last!!162", "first!!last!!.162", "f!!last!!162", "f!!last!!.162", "first!!.last!!162", "first!!.last!!.162", "first!!last!!172", "first!!last!!.172", "f!!last!!172", "f!!last!!.172", "first!!.last!!172", "first!!.last!!.172", "first!!last!!182", "first!!last!!.182", "f!!last!!182", "f!!last!!.182", "first!!.last!!182", "first!!.last!!.182", "first!!last!!192", "first!!last!!.192", "f!!last!!192", "f!!last!!.192", "first!!.last!!192", "first!!.last!!.192", "first!!last!!202", "first!!last!!.202", "f!!last!!202", "f!!last!!.202", "first!!.last!!202", "first!!.last!!.202", "first!!last!!212", "first!!last!!.212", "f!!last!!212", "f!!last!!.212", "first!!.last!!212", "first!!.last!!.212", "first!!last!!222", "first!!last!!.222", "f!!last!!222", "f!!last!!.222", "first!!.last!!222", "first!!.last!!.222", "first!!last!!232", "first!!last!!.232", "f!!last!!232", "f!!last!!.232", "first!!.last!!232", "first!!.last!!.232", "first!!last!!242", "first!!last!!.242", "f!!last!!242", "f!!last!!.242", "first!!.last!!242", "first!!.last!!.242", "first!!last!!252", "first!!last!!.252", "f!!last!!252", "f!!last!!.252", "first!!.last!!252", "first!!.last!!.252", "first!!last!!262", "first!!last!!.262", "f!!last!!262", "f!!last!!.262", "first!!.last!!262", "first!!.last!!.262", "first!!last!!272", "first!!last!!.272", "f!!last!!272", "f!!last!!.272", "first!!.last!!272", "first!!.last!!.272", "first!!last!!282", "first!!last!!.282", "f!!last!!282", "f!!last!!.282", "first!!.last!!282", "first!!.last!!.282", "first!!last!!292", "first!!last!!.292", "f!!last!!292", "f!!last!!.292", "first!!.last!!292", "first!!.last!!.292", "first!!last!!302", "first!!last!!.302", "f!!last!!302", "f!!last!!.302", "first!!.last!!302", "first!!.last!!.302", "first!!last!!312", "first!!last!!.312", "f!!last!!312", "f!!last!!.312", "first!!.last!!312", "first!!.last!!.312", "first!!last!!322", "first!!last!!.322", "f!!last!!322", "f!!last!!.322", "first!!.last!!322", "first!!.last!!.322", "first!!last!!332", "first!!last!!.332", "f!!last!!332", "f!!last!!.332", "first!!.last!!332", "first!!.last!!.332", "first!!last!!342", "first!!last!!.342", "f!!last!!342", "f!!last!!.342", "first!!.last!!342", "first!!.last!!.342", "first!!last!!352", "first!!last!!.352", "f!!last!!352", "f!!last!!.352", "first!!.last!!352", "first!!.last!!.352", "first!!last!!362", "first!!last!!.362", "f!!last!!362", "f!!last!!.362", "first!!.last!!362", "first!!.last!!.362", "first!!last!!372", "first!!last!!.372", "f!!last!!372", "f!!last!!.372", "first!!.last!!372", "first!!.last!!.372", "first!!last!!382", "first!!last!!.382", "f!!last!!382", "f!!last!!.382", "first!!.last!!382", "first!!.last!!.382", "first!!last!!392", "first!!last!!.392", "f!!last!!392", "f!!last!!.392", "first!!.last!!392", "first!!.last!!.392", "first!!last!!402", "first!!last!!.402", "f!!last!!402", "f!!last!!.402", "first!!.last!!402", "first!!.last!!.402", "first!!last!!412", "first!!last!!.412", "f!!last!!412", "f!!last!!.412", "first!!.last!!412", "first!!.last!!.412", "first!!last!!422", "first!!last!!.422", "f!!last!!422", "f!!last!!.422", "first!!.last!!422", "first!!.last!!.422", "first!!last!!432", "first!!last!!.432", "f!!last!!432", "f!!last!!.432", "first!!.last!!432", "first!!.last!!.432", "first!!last!!442", "first!!last!!.442", "f!!last!!442", "f!!last!!.442", "first!!.last!!442", "first!!.last!!.442", "first!!last!!452", "first!!last!!.452", "f!!last!!452", "f!!last!!.452", "first!!.last!!452", "first!!.last!!.452", "first!!last!!462", "first!!last!!.462", "f!!last!!462", "f!!last!!.462", "first!!.last!!462", "first!!.last!!.462", "first!!last!!472", "first!!last!!.472", "f!!last!!472", "f!!last!!.472", "first!!.last!!472", "first!!.last!!.472", "first!!last!!482", "first!!last!!.482", "f!!last!!482", "f!!last!!.482", "first!!.last!!482", "first!!.last!!.482", "first!!last!!492", "first!!last!!.492", "f!!last!!492", "f!!last!!.492", "first!!.last!!492", "first!!.last!!.492", "first!!last!!502", "first!!last!!.502", "f!!last!!502", "f!!last!!.502", "first!!.last!!502", "first!!.last!!.502", "first!!last!!512", "first!!last!!.512", "f!!last!!512", "f!!last!!.512", "first!!.last!!512", "first!!.last!!.512", "first!!last!!522", "first!!last!!.522", "f!!last!!522", "f!!last!!.522", "first!!.last!!522", "first!!.last!!.522", "first!!last!!532", "first!!last!!.532", "f!!last!!532", "f!!last!!.532", "first!!.last!!532", "first!!.last!!.532", "first!!last!!542", "first!!last!!.542", "f!!last!!542", "f!!last!!.542", "first!!.last!!542", "first!!.last!!.542", "first!!last!!552", "first!!last!!.552", "f!!last!!552", "f!!last!!.552", "first!!.last!!552", "first!!.last!!.552", "first!!last!!562", "first!!last!!.562", "f!!last!!562", "f!!last!!.562", "first!!.last!!562", "first!!.last!!.562", "first!!last!!572", "first!!last!!.572", "f!!last!!572", "f!!last!!.572", "first!!.last!!572", "first!!.last!!.572", "first!!last!!582", "first!!last!!.582", "f!!last!!582", "f!!last!!.582", "first!!.last!!582", "first!!.last!!.582", "first!!last!!592", "first!!last!!.592", "f!!last!!592", "f!!last!!.592", "first!!.last!!592", "first!!.last!!.592", "first!!last!!602", "first!!last!!.602", "f!!last!!602", "f!!last!!.602", "first!!.last!!602", "first!!.last!!.602", "first!!last!!612", "first!!last!!.612", "f!!last!!612", "f!!last!!.612", "first!!.last!!612", "first!!.last!!.612", "first!!last!!622", "first!!last!!.622", "f!!last!!622", "f!!last!!.622", "first!!.last!!622", "first!!.last!!.622", "first!!last!!632", "first!!last!!.632", "f!!last!!632", "f!!last!!.632", "first!!.last!!632", "first!!.last!!.632", "first!!last!!642", "first!!last!!.642", "f!!last!!642", "f!!last!!.642", "first!!.last!!642", "first!!.last!!.642", "first!!last!!652", "first!!last!!.652", "f!!last!!652", "f!!last!!.652", "first!!.last!!652", "first!!.last!!.652", "first!!last!!662", "first!!last!!.662", "f!!last!!662", "f!!last!!.662", "first!!.last!!662", "first!!.last!!.662", "first!!last!!672", "first!!last!!.672", "f!!last!!672", "f!!last!!.672", "first!!.last!!672", "first!!.last!!.672", "first!!last!!682", "first!!last!!.682", "f!!last!!682", "f!!last!!.682", "first!!.last!!682", "first!!.last!!.682", "first!!last!!692", "first!!last!!.692", "f!!last!!692", "f!!last!!.692", "first!!.last!!692", "first!!.last!!.692", "first!!last!!702", "first!!last!!.702", "f!!last!!702", "f!!last!!.702", "first!!.last!!702", "first!!.last!!.702", "first!!last!!712", "first!!last!!.712", "f!!last!!712", "f!!last!!.712", "first!!.last!!712", "first!!.last!!.712", "first!!last!!722", "first!!last!!.722", "f!!last!!722", "f!!last!!.722", "first!!.last!!722", "first!!.last!!.722", "first!!last!!732", "first!!last!!.732", "f!!last!!732", "f!!last!!.732", "first!!.last!!732", "first!!.last!!.732", "first!!last!!742", "first!!last!!.742", "f!!last!!742", "f!!last!!.742", "first!!.last!!742", "first!!.last!!.742", "first!!last!!752", "first!!last!!.752", "f!!last!!752", "f!!last!!.752", "first!!.last!!752", "first!!.last!!.752", "first!!last!!762", "first!!last!!.762", "f!!last!!762", "f!!last!!.762", "first!!.last!!762", "first!!.last!!.762", "first!!last!!772", "first!!last!!.772", "f!!last!!772", "f!!last!!.772", "first!!.last!!772", "first!!.last!!.772", "first!!last!!782", "first!!last!!.782", "f!!last!!782", "f!!last!!.782", "first!!.last!!782", "first!!.last!!.782", "first!!last!!792", "first!!last!!.792", "f!!last!!792", "f!!last!!.792", "first!!.last!!792", "first!!.last!!.792", "first!!last!!802", "first!!last!!.802", "f!!last!!802", "f!!last!!.802", "first!!.last!!802", "first!!.last!!.802", "first!!last!!812", "first!!last!!.812", "f!!last!!812", "f!!last!!.812", "first!!.last!!812", "first!!.last!!.812", "first!!last!!822", "first!!last!!.822", "f!!last!!822", "f!!last!!.822", "first!!.last!!822", "first!!.last!!.822", "first!!last!!832", "first!!last!!.832", "f!!last!!832", "f!!last!!.832", "first!!.last!!832", "first!!.last!!.832", "first!!last!!842", "first!!last!!.842", "f!!last!!842", "f!!last!!.842", "first!!.last!!842", "first!!.last!!.842", "first!!last!!852", "first!!last!!.852", "f!!last!!852", "f!!last!!.852", "first!!.last!!852", "first!!.last!!.852", "first!!last!!862", "first!!last!!.862", "f!!last!!862", "f!!last!!.862", "first!!.last!!862", "first!!.last!!.862", "first!!last!!872", "first!!last!!.872", "f!!last!!872", "f!!last!!.872", "first!!.last!!872", "first!!.last!!.872", "first!!last!!882", "first!!last!!.882", "f!!last!!882", "f!!last!!.882", "first!!.last!!882", "first!!.last!!.882", "first!!last!!892", "first!!last!!.892", "f!!last!!892", "f!!last!!.892", "first!!.last!!892", "first!!.last!!.892", "first!!last!!902", "first!!last!!.902", "f!!last!!902", "f!!last!!.902", "first!!.last!!902", "first!!.last!!.902", "first!!last!!912", "first!!last!!.912", "f!!last!!912", "f!!last!!.912", "first!!.last!!912", "first!!.last!!.912", "first!!last!!922", "first!!last!!.922", "f!!last!!922", "f!!last!!.922", "first!!.last!!922", "first!!.last!!.922", "first!!last!!932", "first!!last!!.932", "f!!last!!932", "f!!last!!.932", "first!!.last!!932", "first!!.last!!.932", "first!!last!!942", "first!!last!!.942", "f!!last!!942", "f!!last!!.942", "first!!.last!!942", "first!!.last!!.942", "first!!last!!952", "first!!last!!.952", "f!!last!!952", "f!!last!!.952", "first!!.last!!952", "first!!.last!!.952", "first!!last!!962", "first!!last!!.962", "f!!last!!962", "f!!last!!.962", "first!!.last!!962", "first!!.last!!.962", "first!!last!!972", "first!!last!!.972", "f!!last!!972", "f!!last!!.972", "first!!.last!!972", "first!!.last!!.972", "first!!last!!982", "first!!last!!.982", "f!!last!!982", "f!!last!!.982", "first!!.last!!982", "first!!.last!!.982", "first!!last!!992", "first!!last!!.992", "f!!last!!992", "f!!last!!.992", "first!!.last!!992", "first!!.last!!.992"]


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
                     hangouts_token, cookies, gaiaID):
    possible_emails = prepare_emails(name)


    for email in possible_emails:
        data = is_email_google_account(client, hangouts_auth, cookies, email,
                                       hangouts_token)

        if data:
            for match in data['matches']:
                print( Fore.GREEN + email + Fore.RESET)
                if match['personId'][0] == gaiaID:
                    print(Fore.GREEN + "MATCH!!!!!!!!" + Fore.RESET)
                # return match['lookupId']
        else:
            print(Fore.RED + email + Fore.RESET)

    return ""

def name_hunt(name, gaiaID):
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
                     hangouts_token=hangouts_token, cookies=cookies, gaiaID=gaiaID)