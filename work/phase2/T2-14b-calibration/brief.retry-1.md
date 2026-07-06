# RETRY 1 — attempt-0 타임아웃 부검 (범위 축소: 캘리브레이션 코어만)
잔존물: rules-align/trust/typo.yaml에 감점 파라미터 수정 진행분 (커밋 안 됨 — 이어서 써라).
calibration-report.json·run-calibration.mjs 미산출. 31규칙 매핑표는 이 태스크에서 제거됨
(별도 태스크 T2-14c로 분리 — docs/rule-mapping.md는 절대 건드리지 말 것).

이 시도의 축소된 범위: 원본 브리프의 (1)(2)(3)만 — 골든셋+demo 전수 채점, calibration-report.json
(pass 최저·fail 최고·분리도), 분리도 미달 시 감점 파라미터만 조정+passLineHistory 이력.
계산 무거우면 채점 대상을 대표 표본(합격 10·불합격 10·demo 3장)으로 줄여도 된다 — 근거를 리포트에 기록.
결과: out/attempt-1/result.md
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
