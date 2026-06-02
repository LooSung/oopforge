# Codex Plugin Manifest

Codex 플러그인 마켓플레이스 등록을 위한 매니페스트다.

현재 Phase 1에서는 `scripts/setup/install.sh`가 `~/.codex/skills/oopforge` 심볼릭 링크를 만든다.
Codex는 이 링크의 `SKILL.md`를 스킬 진입점으로 읽고 `/oopforge:craft` 프롬프트를 워크플로우로 라우팅한다.

Phase 2에서는 Codex 플러그인 경로로 설치할 수 있게 전환한다.
