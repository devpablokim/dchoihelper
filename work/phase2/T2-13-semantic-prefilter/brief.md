# TASK T2-13-semantic-prefilter (T2-13의 codex 몫만 — 판정식·루브릭은 fable 작성 완료)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 1d672a3e20639dfa15c8d359be88bdbabeaefb34
## 목표
(1) 의미론 대리지표 1차 필터 src/semantic-prefilter.mjs: deck-plan+copy.json을 받아
기존 도구(deck-copy title-lint, six-by-six, storyline titles-prelint)를 조합 호출해
"opus 판정 없이도 명백 불합격"인 슬라이드를 선별 (hard 판정 아님 — 후보 플래그만).
(2) 의미론 캘리브레이션 코퍼스: 결정론 라벨 가능한 synthetic 한국어 슬라이드 카피 셋 —
액션타이틀/MECE/원메시지 각 축의 명백 합격 5+ 명백 불합격 5 (라벨 근거를 manifest에 명시).
incubator/packages/deck-grader/calibration-semantic/ 에 저장.
## 입력
incubator/packages/deck-grader/semantic-gate.json (fable 작성 정본 — 수정 금지),
incubator/packages/deck-copy/src/, incubator/packages/deck-storyline/src/
## 산출
allowedWritePaths: incubator/packages/deck-grader/src/semantic-prefilter.mjs,
incubator/packages/deck-grader/calibration-semantic/, incubator/packages/deck-grader/tests/run-semantic-prefilter.mjs
## 합격기준
캘리브레이션 코퍼스의 명백 불합격이 prefilter에서 전부 플래그(누락 0) + 명백 합격 오플래그 20% 이하.
expectedCommand: cd incubator && node packages/deck-grader/tests/run-semantic-prefilter.mjs
## 금지사항
semantic-gate.json·rubrics·prompts 수정 금지. grader.yaml 수정 금지. contracts/ 수정 금지.
