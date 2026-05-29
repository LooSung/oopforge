# OpenCode Experimental Support

OpenCode 지원은 experimental / opt-in 으로 둔다.

기본 설치(`./install.sh`)는 Claude Code와 Codex CLI를 우선 대상으로 한다.
OpenCode까지 설치하려면 명시적으로 실행한다:

```bash
INSTALL_OPENCODE=1 ./install.sh
```

검사도 opt-in 이다:

```bash
CHECK_OPENCODE=1 ./doctor.sh
```

현재 동작은 `skills/` 디렉토리를 `~/.config/opencode/skills/oopforge` 로
심볼릭 링크하는 수준이다. OpenCode 마켓플레이스나 플러그인 포맷이 안정화되면
이 디렉토리에 매니페스트를 추가한다.
