# TASK T3-5f-qa-fix (시각 QA fix 사이클)
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: a689adcb23c14a3478e176fea08777c45fccc97c
## 실측 결함 (fix 대상 — 전부 실제 채점·판정 결과)
opus 시각 QA 만장일치 fail(1,1,1): 슬라이드 3이 깨짐 — 빈 민트색 placeholder 박스(좌측 패널),
"Contact audit" 칩과 파란 바가 슬라이드 밖으로 넘침.
grader 73점(합격선 90), hard fail 5: color.background_text_readability, trust.source_ref_integrity,
trust.source_line_format, trust.data_timestamp_required, accessibility.reading_order_matches_visual.
카테고리 구멍: trust 40, alignment 45, structure 50.
## 목표
golden-compose 입력 픽스처와 (필요시) compose 바인딩 결함을 고쳐 E2E 덱이 정직하게 90점+hard fail 0을
달성하게 하라. 반드시 원인 순서로: (1) 슬라이드 3의 빈 슬롯 — 바인딩 누락인지 compose 버그인지 판별
(plan 바인딩 검사(run-plan-a)가 이 픽스처를 통과시켰다면 검사 구멍이므로 그것도 보강),
(2) 요소 넘침 — 템플릿 밖 좌표/크기 값 수정, (3) trust 3종 — 수치 슬라이드에 sourceRef 실존 참조·
출처 라인 형식·데이터 시점 표기 추가 (픽스처 콘텐츠 보강), (4) 가독성·읽기 순서 수정.
## 검증 체인 (expectedCommand)
cd incubator && node packages/deck-assembler/tests/run-plan-a.mjs && node packages/deck-assembler/tests/run-compose.mjs && node - <<'EOS'
import { writeComposeOutputs } from './packages/deck-assembler/src/compose/compose.mjs';
import { execFileSync } from 'node:child_process';
const c = await writeComposeOutputs('packages/deck-assembler/tests/golden-compose/input','packages/deck-assembler/qa/deck',{});
execFileSync('node',['packages/deck-grader/src/cli.mjs','packages/deck-assembler/qa/deck/slides','--out','packages/deck-assembler/qa/grade-report.json'],{stdio:'inherit'});
const r = (await import('node:fs')).readFileSync('packages/deck-assembler/qa/grade-report.json','utf8');
const d = JSON.parse(r);
if (d.totalScore < 90 || (d.hardFails||[]).length > 0) { console.error('FAIL', d.totalScore, d.hardFails); process.exit(1); }
console.log('PASS', d.totalScore);
EOS
## 산출
allowedWritePaths: incubator/packages/deck-assembler/ (픽스처·compose·plan 검사 보강), 골든 스냅샷 갱신 허용(사유 기록)
## 금지사항
채점 규칙·grader.yaml·contracts/ 수정 금지 (덱을 규칙에 맞추는 것이지 규칙을 덱에 맞추지 말 것).
점수 조작성 회피(예: 수치 삭제로 trust 규칙 우회) 금지 — 출처를 채워서 통과하라.
