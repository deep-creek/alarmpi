#!/usr/bin/python3

from dataclasses import dataclass
import argparse


@dataclass
class Settings:
    password : str = '135'
    test_mode : bool = False
    alarm_duration : int = 90

def _init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
        description="Raspberry PI based alarm system"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0.1"
    )
    parser.add_argument('--test-mode', help='Enable test-mode. This disables the alarm sound. Default=off', action="store_true")
    parser.add_argument('--password', help='The password to enter for disarming the alarm system', default='135')
    parser.add_argument('--alarmDuration', help='Number of seconds the alarm should sound and the blinding lights should light', default=90, type=int)
    return parser

def get_settings():
    parser = _init_argparse()
    args = parser.parse_args()

    return Settings(args.password
                        , args.test_mode
                        , args.alarmDuration)
