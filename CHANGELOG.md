# Changelog

모든 변경은 여기에 기록한다. [Keep a Changelog](https://keepachangelog.com/) 형식.

## [Unreleased]

### Added
- 기본 README 언어를 영어로 전환하고 한국어, 일본어, 중국어 README를 추가.
- 에이전트 자동 로딩을 위한 루트 지시 파일 `AGENTS.md`, `CLAUDE.md` 추가.
- 기본 README를 Quickstart, Installation, Basic Workflow, What's Inside, Philosophy 중심으로 재구성.
- 워크플로우 스킬 `delivery-plan`, `test`, `refactor` 추가.
- README에 권장 workflow 순서와 단일 명령 사용 예시 추가.
- Java/Python Skeleton 기본 패키지 구조를 Splearn-style Spring, Clean FastAPI layout으로 정리.

## [0.1.0] - 2026-05-29

### Added
- 초기 구조 (`skills/`, `agents/`, `commands/`)
- 메타 스킬: `skills/_meta/skill-template.md`
- 워크플로우 스킬: discovery, design, skeleton, implement
- OOP 스킬: aggregate-root, value-object, application-service, repository-port
- Java 스킬: spring-hexagonal-layout, jpa-repository
- Python 스킬: pydantic-value-object, clean-fastapi-layout
- Subagent: `ddd-architect`
- Slash commands: discovery, design, skeleton, implement
- `install.sh`, `uninstall.sh` (Claude Code, Codex CLI, OpenCode 자동 감지)
