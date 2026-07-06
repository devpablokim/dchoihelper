# TASK T2-17-p6-integration (needs: T2-7~9, T2-10 — 전부 integrated 확인됨)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 1ff09773372dd331a0d3e52febcc2d056d436efa
## 목표
P6 도구들(title-lint, fact-guard/six-by-six/speech-time, reject-handler)을 synthetic이 아닌
실제 통합 코퍼스(packages/deck-storyline/corpus/demo-topic-1/ — T2-10 산출 정본)로 재검증한다.
(1) demo-topic-1의 outline/claims에서 copy.json 초안을 기계 생성(간단 변환 스크립트 — LLM 아님),
(2) P6 전 도구를 이 copy.json에 실행해 통합 리포트 산출(각 도구 결과 + 교차 일관성:
fact-guard의 sourceRef 대조가 claims-validate와 같은 결론인지),
(3) opus 판정용 패키지 생성 — 타이틀 테스트(제목 시퀀스)·팩트체크(주장 vs claims 원문) 대상 텍스트.
## 입력
incubator/packages/deck-copy/, incubator/packages/deck-storyline/corpus/demo-topic-1/, incubator/contracts/copy.schema.json
## 산출
allowedWritePaths: incubator/packages/deck-copy/tests/integration/ (변환 스크립트, run-integration.mjs, 리포트, opus 판정 패키지 subject-*.txt)
## 합격기준
통합 리포트 green (도구 전부 실행 + 교차 일관성 일치) + copy.json이 스키마 검증 통과 + 판정 패키지 2종 생성.
opus 판정은 fable 후속.
expectedCommand: cd incubator && node packages/deck-copy/tests/integration/run-integration.mjs
## 금지사항
P6 도구·코퍼스 원본 수정 금지 (소비만). contracts/ 수정 금지.
