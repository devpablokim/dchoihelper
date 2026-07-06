# TASK T2-4-prompt-compiler
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 7f62805eb8a6ef89d1f4f449ead65ca9a3ec1f68
## 목표
deck-imagery C12 확장 프롬프트 컴파일러: image-brief(contracts/image-brief.schema.json)를 받아
gpt-image 프롬프트 문자열로 컴파일하는 순수 함수 모듈. 규칙: (1) 슬라이드 배경용은 텍스트/글자 절대
금지 문구와 네거티브 스페이스(텍스트 안전 영역) 지시 포함, (2) tokens.json의 브랜드 컬러를 HEX로 명시,
(3) 끝에 AR 토큰(16:9), (4) 긍정형 지시 위주(공냥 킷 티어드 네거티브 사상 — ~/.claude/skills/image-prompt/SKILL.md 의 C12 절 참고 가능하면 읽고 반영), (5) 산출 jsonl 스키마 {id,prompt,size}.
## 입력
incubator/contracts/{image-brief.schema.json,tokens.schema.json}, /home/seunghyeong/.claude/skills/image-prompt/SKILL.md (읽기만)
## 산출
allowedWritePaths: incubator/packages/deck-imagery/src/prompt-compile.mjs, incubator/packages/deck-imagery/tests/run-compile.mjs, incubator/packages/deck-imagery/tests/briefs/, incubator/packages/deck-imagery/package.json
## 합격기준
브리프 픽스처 전수: 컴파일 결정론(2회 동일) + 금지 규칙 위반 0(스냅샷) + jsonl 스키마 검증.
expectedCommand: cd incubator && node packages/deck-imagery/tests/run-compile.mjs
## 공통 금지사항
contracts/ 수정 금지. npm 신규 설치 금지. allowedWritePaths 밖 쓰기 금지. 상수 하드코딩 금지.
## 공통 완료 규약
expectedCommand 직접 실행 green 확인 후 result.md 기록.
