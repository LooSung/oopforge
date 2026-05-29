#!/usr/bin/env bash
#
# OOPforge bootstrap installer
#   Clone or update ~/.oopforge, then run install.sh.
#
set -euo pipefail

REPO_URL="${OOPFORGE_REPO_URL:-https://github.com/LooSung/oopforge.git}"
INSTALL_DIR="${OOPFORGE_HOME:-$HOME/.oopforge}"
BRANCH="${OOPFORGE_BRANCH:-main}"

cyan()  { printf "\033[36m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*"; }

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    red "필수 명령을 찾을 수 없습니다: $1"
    exit 1
  fi
}

clone_or_update() {
  if [ -d "$INSTALL_DIR/.git" ]; then
    cyan "==> 기존 OOPforge 업데이트: $INSTALL_DIR"
    git -C "$INSTALL_DIR" fetch --quiet origin "$BRANCH"
    git -C "$INSTALL_DIR" checkout --quiet "$BRANCH"
    git -C "$INSTALL_DIR" pull --ff-only --quiet origin "$BRANCH"
    return
  fi

  if [ -e "$INSTALL_DIR" ]; then
    red "설치 경로가 이미 존재하지만 git 저장소가 아닙니다: $INSTALL_DIR"
    yellow "다른 경로를 쓰려면 OOPFORGE_HOME=/path/to/oopforge 로 실행하세요."
    exit 1
  fi

  cyan "==> OOPforge clone: $INSTALL_DIR"
  git clone --quiet --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
}

require git

clone_or_update
chmod +x "$INSTALL_DIR/install.sh" "$INSTALL_DIR/uninstall.sh"

cyan "==> install.sh 실행"
"$INSTALL_DIR/install.sh"

if [ -f "$INSTALL_DIR/doctor.sh" ]; then
  cyan "==> doctor.sh 실행"
  chmod +x "$INSTALL_DIR/doctor.sh"
  "$INSTALL_DIR/doctor.sh"
fi

green "==> OOPforge bootstrap 완료"
