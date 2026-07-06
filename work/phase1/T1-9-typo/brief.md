# TASK T1-9-typo
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 45c8f935c1a01849afd58bc301b6a11c4221f662 / schemaVersion: v0.1.0-draft
## 목표
deck-grader 규칙군 1차 중 타이포그래피 규칙군: 본문 폰트 하한(configured body floor), 폰트 패밀리 수 상한, 슬라이드당 단어/글자 수 상한, 행간·자간 하한, 제목/본문 크기 위계 를 구현한다. 규칙 선정은 /home/seunghyeong/deck-factory/research/consulting-quality.md 의 채점 후보와 PLAN.md 5.3·P8절에서 도출하고 선정 근거를 규칙 파일 상단 주석에 남겨라.
## 입력
incubator/packages/deck-grader/src/ (T0-4 뼈대 — 파서·리포트 재사용, 수정 금지), incubator/contracts/deck-constants.json, /home/seunghyeong/deck-factory/research/consulting-quality.md
## 산출
allowedWritePaths: incubator/packages/deck-grader/src/rules/typo.mjs, incubator/packages/deck-grader/rules-typo.yaml(규칙군 설정 조각 — grader.yaml 직접 수정 절대 금지, 통합은 별도 태스크), incubator/packages/deck-grader/tests/fixtures/typo/, incubator/packages/deck-grader/tests/run-typo.mjs
## 합격기준
WORKERS.md T1-9 게이트: 규칙별 양성/음성 케이스 + 골든 리포트 스냅샷 일치. 규칙군 내 각 규칙마다 위반 픽스처 1+ 정상 픽스처 1, 오검출 0.
expectedCommand: cd incubator/packages/deck-grader && node tests/run-typo.mjs
## 공통 금지사항
contracts/ 수정 금지. 외부 패키지 의존 금지 (node 내장/python3 stdlib만). allowedWritePaths 밖 쓰기 금지.
루트 공유 파일(incubator/package.json 등) 수정 금지 — 필요하면 deps-request.json에 기록만.
임계값·상수 하드코딩 금지: incubator/contracts/deck-constants.json 로드.
## 공통 완료 규약
완료 시 expectedCommand를 직접 실행해 green을 확인하고, 그 출력과 작업 요약을 result.md(-o 회수 파일)에 담아라.
## 추가 금지
grader.yaml, src/rules/ 밖 기존 src 파일, 다른 규칙군 파일 수정 금지 (3태스크 병렬 격리).
