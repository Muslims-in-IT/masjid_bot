#!/bin/bash
cd /opt/masjid_bot
nohup python masjid_bot.py >>bot.out 2>>bot.err & echo $! > is_bot.pid
