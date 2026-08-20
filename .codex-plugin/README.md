# Codex Plugin Manifest

Codex 플러그인 마켓플레이스 등록을 위한 매니페스트다.

현재 `scripts/setup/install.sh`가
`~/.codex/skills/oopforge` 심볼릭 링크를 만든다.
Codex는 이 링크의 `SKILL.md`를 스킬 진입점으로 읽고
`Use OOPforge craft: …` 프롬프트를 워크플로우로 라우팅한다.

Codex의 `/`는 내장 명령용이므로 `/oopforge:craft`를 사용하지 않는다.
`scripts/ci/harness-smoke.sh live codex`가 global skill positive control과
격리된 no-skill negative control을 검사한다.
