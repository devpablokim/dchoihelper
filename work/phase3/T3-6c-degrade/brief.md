# TASK T3-6c-degrade (P9 subtask c — 에디터 트랙 종결)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: c2c7d0c3de6d3538e72b94f8c41b35f93aa477a1
## 목표
에디터 3단계: (1) 임의 HTML degrade — slide-html 계약 밖의 임의 HTML을 열었을 때
편집 가능한 범위(텍스트 노드만)로 강등 동작 + 계약 위반 목록 표시,
(2) 재compose 차단 — edit-manifest가 존재하는 덱에 compose 재실행 요청 시
--discard-edits 플래그 없으면 거부 (편집본 덮어쓰기 방지, PLAN P9 계약),
(3) 거부 시 안내 메시지에 무엇이 유실될지(편집 내역 수) 명시.
## 입력
incubator/packages/deck-editor/, incubator/contracts/{edit-manifest.schema.json,slide-html.contract.md}
## 산출
allowedWritePaths: incubator/packages/deck-editor/src/, incubator/packages/deck-editor/tests/run-degrade.mjs, incubator/packages/deck-editor/tests/fixtures-degrade/
## 합격기준
WORKERS T3-6c 게이트: 임의 HTML 케이스(강등 동작+위반 목록) + --discard-edits 없는 덮어쓰기 거부 케이스
+ 플래그 동반 시 진행 케이스. 기존 에디터 테스트 2종 회귀 green.
expectedCommand: cd incubator && node packages/deck-editor/tests/run-degrade.mjs && node packages/deck-editor/tests/run-bbox-undo.mjs
## 금지사항
contracts/ 수정 금지. 기존 API 파괴 금지.
