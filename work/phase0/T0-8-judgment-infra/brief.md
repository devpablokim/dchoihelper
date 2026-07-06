# TASK T0-8-judgment-infra

## 메타
taskType: code
determinismClass: canonicalized
mode: attended
baseCommit: 3bcb571b06dde0d283955e80a83a8181dd6baab4
schemaVersion: v0.1.0-draft

## 목표
모든 opus hard 게이트가 소비할 3표 다수결 판정 인프라를 구현한다.
완료는 "하니스가 판정 대상 1건에 대해 독립 3표를 스폰해 verdict/{1,2,3}.json과
다수결 final.json을 산출하고, final.json이 verdict.schema.json 검증을 통과하는
스모크가 캘리브레이션 셋에서 완주하는 상태"다. PLAN.md 5.4 프로토콜의 기계화가 본체다.

## 입력
- /home/seunghyeong/deck-factory/PLAN.md 5.3절, 5.4절 (판정 프로토콜 정본 — 정독 필수)
- /home/seunghyeong/deck-factory/incubator/docs/goldenset-freeze.md (캘리브레이션 셋 파생 기준, 특히 3.1 라벨 조작적 정의와 4.3 수량)

## 산출
allowedWritePaths:
- incubator/tools/orchestration/judge_harness.py — python3 표준 라이브러리만.
  기능: (a) --judge-cmd 템플릿 인자로 판정자 호출 명령을 주입받는다
  (기본값: claude -p 헤드리스 opus 호출 한 줄 — 실제 명령 문자열은 설정 파일
  judge_config.json에 두고 하드코딩 금지). (b) 판정 1건당 독립 프로세스 3회 호출
  (컨텍스트 공유 금지), 각 표를 verdict/{n}.json으로 저장. (c) 다수결 집계로
  verdict/final.json 생성. (d) canonicalize 함수 — timestamp/cost/runId 등 volatile
  필드를 제거한 canonical JSON 비교 지원. (e) 판정자 사전 검증 모드 —
  라벨된 쌍 셋을 돌려 일치율 계산·기록.
- incubator/contracts/verdict.schema.json — 필수 필드: rubricVersion, promptVersion,
  calibrationSetId, judgeQualification, scores[](표별 점수·근거), majority,
  softHard(soft|hard), mode(attended|unattended), costLog. PLAN.md 5.4와 정합.
- incubator/scripts/prompts/ — 고정 판정 프롬프트 템플릿 (의미론 3항목: 액션타이틀
  결론성·MECE·원메시지 + 범용 품질 판정 1종. 루브릭 파일을 참조하는 구조).
- incubator/docs/rubrics/ — 게이트별 앵커드 루브릭 (1/3/5점 앵커 서술).
- incubator/tools/orchestration/calibration/ — 캘리브레이션 셋: goldenset-freeze.md
  3.1의 결정론 조건(hard fail 6종 등)에 따라 합격 10건·불합격 10건 이상의
  synthetic 슬라이드 HTML 샘플과 라벨 manifest.json.
- incubator/tools/orchestration/tests/test_judge_harness.py — 판정자 호출을 mock한
  단위 테스트: 다수결 3분기(3:0, 2:1, 판정 실패), 스키마 검증, canonicalize,
  사전 검증 일치율 계산.

## 합격기준
WORKERS.md T0-8 스펙 인용: "샘플 판정 3표가 verdict/{1,2,3}.json으로 저장되고
final.json이 verdict.schema.json 검증을 통과하는 스모크 완주 + 캘리브레이션 셋
다수결 일치율 90% 이상 기록(5.4 임계값) 또는 미달 판정자 명시".
이 태스크의 codex 몫은 mock 판정자로 위 스모크와 테스트 전부 green까지.
실제 opus 캘리브레이션 실행은 fable이 후속 수행한다 (하니스가 --judge-cmd만 갈아끼우면
되는 구조가 합격 조건).
expectedCommand: cd incubator && python3 -m pytest tools/orchestration/tests/ -q (전부 pass, pytest 없으면 python3 tools/orchestration/tests/test_judge_harness.py)

## 금지사항
공통: deck-contracts 기존 스키마 수정 금지(verdict.schema.json 신규 추가만),
allowedWritePaths 밖 쓰기 금지, 외부 패키지 의존 금지(python3 stdlib만),
판정자 명령 하드코딩 금지(judge_config.json).
opus 실호출 금지 — 이 태스크는 mock까지다.

## 참조
- /home/seunghyeong/deck-factory/PLAN.md 5.4 (판정자 사전 검증 임계값·다수결 규약)
- /home/seunghyeong/deck-factory/WORKERS.md T0-8 스펙 (362~371행)
