# deck-factory 리빌드 — 큰 틀 + Phase 0 적대 감사

작성: 2026-07-05 (Fable). 착수: **Fable 복귀 시**. 진행 방식: **매 단계 사용자 컨펌**.
배경: 직전 "완료" 보고가 과장 — 규칙 점수(97점)는 통과했으나 시각적으로 밋밋하고,
이미지 실생성·gn-voice 윤문·차트 픽셀·시각 채점이 껍데기/미배선. 사용자 신뢰 0 상태.

---

## 모델 배정 기준 (고정)

| 모델 | 언제 | 근거 |
|---|---|---|
| **codex** (codex exec 스폰, PARALLEL=15) | 텍스트/코드 기계 작업 — 빌드·수리·grep·테스트 실행·URL 검증·대량 변환 | 제일 쌈. 단 **이미지를 못 봄** — 픽셀 검수 불가 |
| **sonnet** | 픽셀 눈검수가 낀 기계 작업 — 렌더 확인·콘택트시트 검수·PDF 래스터 판독 | 이미지 Read 가능한 최저 단가 |
| **opus** | 판정·디렉션 — 진위 판정·시각 5축 채점·크리에이티브 방향·리포트 대조 | 취향/판단 품질 |
| **fable** | 오케스트레이션 + **최종 적대 검수만** | 스웜 상속 금지(비쌈) |

**재감사(증거 게이트) 기준** — 다음이면 verdict 기각 후 그 항목만 재감사(가능하면 딴 모델로):
1. evidence에 실행한 명령+실출력 없음 (말로만 판정)
2. REAL 판정인데 evidence/ 아래 증거 파일 없음
3. 픽셀 관련 주장인데 PNG 증거 없음
4. verdict와 증거가 모순 (증거는 실패인데 REAL 등)

## 관통 원칙 (5)
1. **픽셀이 진실.** 규칙 점수 ≠ 완료. 콘택트 시트를 눈/opus로 봐야 통과.
2. **사람이 루프 안에.** 후보 N개 → 골라(sprite-gen/card-shorts g17 WARN 경로).
3. **모놀리스는 touch-to-split.** 지금 안 쪼갬. 건드릴 때만 쪼갬. 새 코드는 처음부터 작게(~300줄).
4. **비파괴 사이드카.** 편집은 원본 안 건드리고 `*.edit.json`.
5. **opus=디렉터.** 취향·구성·판정=opus. sonnet=텍스트. codex=빌드. fable=오케스트레이션.

---

## Phase 0 — 적대 감사 (착수 전 게이트 · 전제: 전부 껍데기다)

**규칙:** 모든 auditor는 "이 컴포넌트는 가짜"를 기본값으로 시작. `REAL` 판정은
**증거(실행 흔적·픽셀·실파일)로만**. 코드 존재는 증거 아님. 판정: `REAL / PARTIAL / SHELL / FALSE-CLAIM`.
워커: **컴포넌트당 opus 적대 auditor 1, 격리 병렬.** 산출: `audit/audit-report.json`.

### 컴포넌트별 반증 테스트 (11)
| 컴포넌트 | 반증 테스트(이걸 통과 못하면 SHELL) |
|---|---|
| deck-tokens | 8프리셋으로 각각 렌더 1장 → **색만이 아니라 구조가 다르게** 보이나? |
| deck-storyline | source-pack URL이 **실존**하나(열어봄)? 날조면 FALSE-CLAIM |
| deck-copy | 일부러 나쁜 카피 주입 → **실제로 반려**되나? |
| deck-layouts | image/chart 템플릿이 **실렌더**되나, 死장인가? |
| deck-charts | writePng 켜면 **진짜 차트 픽셀** 나오나? PNG 열어 확인 |
| deck-imagery | 실제 PNG 산출 0장 재확인 → SHELL 확정 |
| deck-motion | 껍데기 확정(빈 src) |
| deck-assembler | 같은 입력 → **같은 해시**(결정론 재현)? |
| deck-grader | **캘리브레이션 공격**: 일부러 못생긴 덱(휑함·저대비·오버플로) 주입 → **여전히 90+면 grader 무효 증명** |
| deck-editor | 라우터 미호출 확정. 단독 실행은 되나? |
| deck-factory | E2E 재실행 → 리포트의 **97.04 재현**되나? 안 되면 리포트 거짓 |

### 메타 감사 (3)
- **테스트 무결성:** 49개 테스트가 실동작 검증인가, stub/vacuous인가? 각 assert 대상 명시.
- **리포트 대조:** COMPLETION-REPORT + README 주장 **한 줄씩** → REAL/PARTIAL/FALSE + 증거 인용.
- **영상:** birth-90s/hook-30s가 실렌더 mp4이고 주장 내용과 일치하나?

### 산출
`audit/audit-report.json` — 컴포넌트별 verdict + 증거 + **리포트 거짓 항목 목록**.
→ 이걸 근거로 COMPLETION-REPORT·README를 **정정**하고, 아래 Phase 1~5의 실제 시작선을 확정.

---

## Phase 1~5 (감사 결과로 조정됨)
| # | 단계 | 방식 | 워커 | 완료 기준 |
|---|---|---|---|---|
| 1 | 비주얼 시스템 이식 | 템플릿이 surface·보더·카드·틴트 다 쓰게 리빌드(**유일한 밑바닥 신규**) | opus설계→codex빌드 | before/after 콘택트 시트 "진짜 디자인" |
| 2 | 픽셀 QA 루프 | card-shorts 게이트17 + g17 판정 이식·16:9 적응 | opus | 밋밋 슬라이드 실제 반려됨 |
| 3 | 이미지 실생성 | `codex_imagegen_runner`+`lowmem_matte` 이식, deck-imagery 배선 | codex | 덱에 이미지 실제로 박힘 |
| 4 | gn-voice 윤문 | copy 뒤 윤문 게이트 배선 | sonnet+gn-voice | 카피가 사용자 문체 |
| 5 | 차트 픽셀화 + 수정기 | writePng:true + editor 마감 배선(이때 1582줄 분해) | codex | 차트 보임 + bbox 수정 가능 |

## 재사용 소스 (검증된 물건)
- **card-shorts** `~/.claude/skills/card-shorts/`: `imagegen/codex_imagegen_runner.py`(실생성),
  `imagegen/lowmem_matte.py`(컷아웃), `gates/g05,g06,g09,g11,g13,g15,g16`(픽셀 게이트),
  `gates/g17_judge_protocol.md`(opus 5축 시각판정, WARN→A/B→사용자픽).
- **sprite-gen** (github aldegad/sprite-gen): 후보풀+사람픽, 콘택트시트 QA, 사이드카 비파괴 편집, state-row 정체성 락(옵션).
