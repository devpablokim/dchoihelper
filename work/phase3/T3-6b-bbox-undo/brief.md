# TASK T3-6b-bbox-undo (P9 subtask b)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 1d6f208bc7764a694600b794c52c12127838653b
## 목표
에디터 2단계: (1) bbox 편집 — /api/apply 확장으로 슬롯 위치·크기 패치(px, 슬라이드 밖 이탈 거부),
(2) undo 1단계 — 직전 편집 1회 되돌리기(편집 전 스냅샷 보관, edit-manifest에 undo 기록),
(3) 미리보기 — GET /preview/:slideId 가 현재 편집 상태 HTML 반환.
## 입력
incubator/packages/deck-editor/ (T3-6a 산출 — src 확장), incubator/contracts/edit-manifest.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-editor/src/, incubator/packages/deck-editor/tests/run-bbox-undo.mjs, incubator/packages/deck-editor/tests/fixtures-bbox/
## 합격기준
WORKERS T3-6b 게이트: 편집→재채점 왕복(bbox 패치 후 grader hard fail 검사 재실행 케이스) + undo 케이스
(패치→undo→원상 diff 0) + 이탈 거부 케이스. T3-6a 테스트 회귀 green.
expectedCommand: cd incubator && node packages/deck-editor/tests/run-bbox-undo.mjs && node packages/deck-editor/tests/run-api.mjs
## 금지사항
contracts/ 수정 금지. T3-6a의 기존 API 계약 파괴 금지 (확장만). degrade 처리는 T3-6c 몫.
