# TASK T2-14c-mapping (T2-14b에서 분리)
## 메타
taskType: research / determinismClass: nondeterministic / mode: attended / baseCommit: 63ef27cfb8d878a0badcf3e40131887d0e56a42e
## 목표
consulting-quality 31개 후보 규칙 → grader 구현 규칙 매핑표 docs/rule-mapping.md 작성.
각 행: 후보 규칙 요지 / 대응 grader 규칙 id(rules-*.yaml·hard fail·semantic gate) / 상태(구현|부분|미구현+사유).
## 입력
/home/seunghyeong/deck-factory/research/consulting-quality.md, incubator/packages/deck-grader/{rules-*.yaml,grader.yaml,semantic-gate.json,src/rules/}
## 산출
allowedWritePaths: incubator/packages/deck-grader/docs/rule-mapping.md
## 합격기준
31행 완비 + 참조한 규칙 id가 실존 (fable이 대조). 이모지·볼드(**) 금지.
expectedCommand: 없음 (research 태스크 — fable 대조 게이트)
## 금지사항
rules yaml·코드 수정 금지. 미구현을 구현으로 표기 금지.
