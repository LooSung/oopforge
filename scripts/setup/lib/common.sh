#!/usr/bin/env bash
#
# OOPforge setup scripts — shared helpers.

cyan() { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red() { printf "\033[31m%s\033[0m\n" "$*"; }

oopforge_pack_dir() {
  local setup_dir="$1"
  cd "$setup_dir/../.." && pwd
}
