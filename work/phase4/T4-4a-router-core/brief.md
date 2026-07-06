# TASK T4-4a-router-core (L3 얇은 라우터 — E2E 체인 글루 + 가드)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 9ab4f6eb71f93a2fca631b10f29a7b4dbb907b60
## 목표
deck-factory 파이프라인 라우터 CLI: input-envelope.json(브리프 포함, 계약 스키마)을 받아
전 단계를 파일 계약으로 체인한다.
단계: (1) doctor — 사용 기능별 환경 검사(core는 항상, charts/imagery/motion은 요청 시.
motion 부재는 경고 후 스킵 — 옵셔널 플러그인), (2) storyline — LLM 스텝은 외부 명령 템플릿
(llm_config.json의 {input}/{output} 치환 — judge-cmds 방식과 동일)로 위임, 산출 source-pack/claims/outline은
claims-validate로 게이트, (3) copy — LLM 스텝 후 title-lint·fact-guard·six-by-six 게이트,
반려는 reject-handler 경유(attempt 상한 계약), (4) chart/image 요청분 render-chart·prompt-compile 호출,
(5) plan(a~d) → compose → grader(90 게이트+semantic prefilter) → export.
가드: privacyMode(sensitive 이상이면 외부 LLM 명령에 경고 태그), unattended 모드 —
needsHumanReview 발생 시 멈추지 않고 draft 익스포트 + review-required 종료 코드(2).
## 입력
incubator/contracts/, incubator/packages/*/src (전부 소비만), incubator/tools/orchestration/judge-cmds/ (명령 템플릿 방식 참고)
## 산출
allowedWritePaths: incubator/packages/deck-factory/ (src/router.mjs, llm_config.json 기본값,
tests/run-router-e2e.mjs, tests/mock-llm/ — 결정론 mock LLM 명령: 고정 storyline/copy 픽스처 출력)
## 합격기준
WORKERS T4-4 완료 정의 1차의 기계분: mock LLM으로 브리프 1줄 envelope → exports/final/ 3포맷 산출
E2E green (grader 90+ 통과 덱) + unattended draft 경로 케이스(고의 needsHumanReview → exit 2 + draft 격리)
+ motion 요청 시 스킵 경고 케이스. 결정론: mock 체인 2회 실행 동일 산출.
expectedCommand: cd incubator && node packages/deck-factory/tests/run-router-e2e.mjs
## 금지사항
다른 패키지 수정 금지 (호출만). contracts/ 수정 금지. 실 LLM 호출 금지 (mock — 실사격은 fable 후속).
게이트 우회 경로 금지 (모든 단계 산출은 계약 검증 통과 후에만 다음 단계로).
