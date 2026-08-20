# Claude Code Plugin Manifest

이 디렉토리는 OOPforge를 **Claude Code 플러그인 마켓플레이스** 에 등록하기 위한 매니페스트를 담는다.

1.x에서 지원하는 경로는 심볼릭 링크 설치와 `/oopforge:craft`다.
`scripts/ci/harness-smoke.sh live claude`가 positive/negative activation을
검사한다. 마켓플레이스 공개 후에는 다음
명령으로 설치할 수 있도록 준비한다:

```text
/plugin marketplace add LooSung/oopforge
/plugin install oopforge
```

## 멀티 하네스 로드맵

| 하네스 | 디렉토리 | 상태 |
|---|---|---|
| Claude Code | `.claude-plugin/` | symlink + command 지원, marketplace 미공개 |
| Codex CLI | `.codex-plugin/` | global skill 지원 |
| Cursor | `.cursor-plugin/` | explicit local plugin 지원 |

Multi-harness packaging follows OOPforge's own portable layout (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`).

Reference (packaging layout): [obra/superpowers](https://github.com/obra/superpowers)
