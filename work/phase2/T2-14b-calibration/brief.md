# TASK T2-14b-calibration (needs: T2-14a)
## 메타
taskType: code / determinismClass: canonicalized / mode: attended / baseCommit: 63ef27cfb8d878a0badcf3e40131887d0e56a42e
## 목표
1단계 캘리브레이션: (1) synthetic 골든셋(calibration/ 20샘플 + calibration-semantic)과
examples/demo-phase1 덱을 T2-14a 집계기로 전수 채점, (2) 라벨 대비 점수 분포 리포트
(pass 라벨 최저점, fail 라벨 최고점, 잠정 합격선 90의 분리도) calibration-report.json 산출,
(3) 분리도가 나쁘면(pass 최저 < fail 최고) 가중치가 아니라 규칙별 감점 함수 파라미터를 조정하고
이력을 grader.yaml passLineHistory에 추가, (4) consulting-quality 31규칙 → grader 규칙 매핑표
docs/rule-mapping.md 작성 (미구현 규칙은 "미구현/사유" 정직 표기).
## 입력
incubator/packages/deck-grader/ 전체, /home/seunghyeong/deck-factory/research/consulting-quality.md
## 산출
allowedWritePaths: incubator/packages/deck-grader/calibration-report.json, incubator/packages/deck-grader/docs/rule-mapping.md, incubator/packages/deck-grader/grader.yaml(passLineHistory 추가만), incubator/packages/deck-grader/src/rules/*.yaml 아닌 감점 파라미터 파일이 있으면 그것, incubator/packages/deck-grader/tests/run-calibration.mjs
## 합격기준
calibration-report.json 산출 + 분리도 양성(pass 최저 > fail 최고) + 매핑표 31행 완비.
expectedCommand: cd incubator && node packages/deck-grader/tests/run-calibration.mjs
## 금지사항
가중치(categories) 수정 금지 — 감점 함수 파라미터만. 라벨 조작 금지. contracts/ 수정 금지.
