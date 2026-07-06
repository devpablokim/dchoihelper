# deck-factory 워커 실행 계획서

PLAN.md(마스터플랜, 정본)의 실행 설계 문서.
PLAN.md는 워커 역할(codex=코드, opus=판단 게이트, sonnet=테스트, fable=오케스트레이션)과
동시성(codex 15, manim 4~6)만 정한다. 이 문서는 그 아래층 —
태스크 분해 단위, 브리프 작성, 스폰 명령, 게이트 루프, 실패 회수 — 를 정의한다.
모순 발생 시 PLAN.md가 우선하고 이 문서를 고친다.

작성일: 2026-07-03. 개정 1차: 외부 크리틱(workers-critique.md) 반영 —
반영·기각 내역은 10절.


## 0. 인프라 재사용·확장·신규 판단 기준

종전의 "신규 인프라 발명 금지" 전제는 폐기한다.
발명 금지는 바퀴 재발명을 막는 데는 유효했지만,
기존 도구의 소관이 아닌 결함(의존성 강제 부재, attempt 미분리, 판정 하니스 부재)을
규약 문장으로 때우는 부작용을 만들었다. 대신 아래 3분류로 판단한다.

- 재사용: 기존 도구가 그 일을 이미 한다.
  예 — codex 스폰·격리·회수는 codex-spawn, 단계 게이트·resume은 forge 러너,
  이미지 배치 생성은 codex-imagegen. 재구축 금지.
- 확장: 기존 도구가 80%를 하고 20%가 부족하다.
  래퍼 또는 기능 추가로 해결한다. 원본은 건드리지 않고 wrapper를 만든다.
  예 — codex-spawn의 out-존재 skip을 attempt-분리 skip으로 바꾸는 wrapper.
- 신규: 기존 도구 소관이 아니다.
  정식 빌드 태스크로 입력/산출/합격기준 스펙을 박고 만든다.
  예 — DAG 태스크 러너(forge stages.json은 직렬 전용이라 80% 미달),
  opus 다수결 판정 하니스, 비LLM 렌더 잡 큐, 한도/예산 감시기.

공통 규칙:
- 확장·신규 인프라는 반드시 분배표의 정식 태스크(Phase 0~1)로 편입한다.
  규약 문장만 쓰고 구현 태스크가 없는 인프라는 존재하지 않는 것으로 간주한다.
- 재사용·확장 대상 러너는 홈 디렉토리 mutable 경로에 의존하지 않는다 —
  Phase 0에서 리포의 tools/orchestration/에 vendoring하고
  원본 버전·체크섬을 기록한다 (T0-9). 실행은 vendored 사본으로만 한다.

재사용 자산 원본 위치 (vendoring 소스):
- skill-forge 러너: ~/behavior-skill-analysis/drafts/doc-readability-linter/forge/skill_forge_runner.py
  (stages.json 단계 선언 → codex exec 워커 + 게이트 → state/*.done 재개)
- skill-forge 플레이북: 같은 디렉토리 SKILL-FORGE-PLAYBOOK.md (모델 배정, 병렬/순차 판단, 안티패턴)
- codex-spawn 스킬: ~/.claude/skills/codex-spawn/SKILL.md + codex_spawn_runner.py
- codex-imagegen 스킬: 이미지 배치 전용 (P5 생성 실행)

이번 크리틱에서 도출된 확장·신규 인프라와 태스크 매핑:

| 인프라 | 분류 | 태스크 |
|---|---|---|
| codex-spawn attempt-분리 wrapper + 러너 vendoring | 확장 | T0-9 |
| DAG 태스크 러너 (work/dag.json 소비) | 신규 | T0-10 |
| opus 3표 다수결 판정 하니스 + verdict.schema.json | 신규 | T0-8 |
| 비LLM 렌더 잡 큐 (manim/헤드리스, 세마포어) | 신규 | T1-7 |
| 한도/예산 감시기 (중단점 저장 + 재개 명령) | 신규 | T1-8 |


## 1. 워커 유형과 실행 기반

### 1.0 모델 예산 원칙 — codex 우선 (2026-07-03 사용자 지시로 개정)

기본 워커는 codex다. 코드 구현만이 아니라 조사·진단·문서 수정·감사·크리틱·리팩터 등
"답을 찾는" 작업 전부를 codex exec로 먼저 보낸다
(분석·조사는 -s read-only, 수정은 -s workspace-write).
Phase 0 계획 단계에서 실증됨 — 계획 적대심사·재심사 6회를 전부 codex가 수행했고 품질이 유지됐다.

claude 계열은 codex가 구조적으로 못 하는 것에만 쓴다:
- opus 판정: 5.4 hard 게이트 전용. 실행도 서브에이전트가 아니라
  judge_harness.py + judge-cmds/judge_opus.sh(claude -p 헤드리스) 경유가 표준 —
  Phase 0 승격 재판정에서 실증됨. codex에게 게이트 판정을 시키지 않는 원칙은 유지
  (판정 품질이 계약이므로).
- 웹 증거 수집: 브라우저/MCP/우회가 필요한 리서치(라이선스 스냅샷 등)만 claude 워커.
  codex 샌드박스는 네트워크가 막혀 있고, 안전 규정상 bypass를 쓰지 않기 때문.
- 테스트 작성(구 sonnet 몫): 기본 codex로 대체한다. red-first 격리 요건은
  "구현과 다른 codex 세션 + allowedWritePaths 분리"로 충족한다 (1.2의 순서 규칙은 동일 적용).

fable(메인 세션)은 1.3의 4역할(브리프·스폰/회수·게이트 소집·통합) 밖의 일을 직접 하지 않는다.
특히 3턴 이상 걸릴 조사·진단·수정은 fable이 bash로 파고들지 말고 codex read-only 태스크로 위임한다.
게이트 확인(expectedCommand 1회 실행, 마커 기록)은 예외 — 위임 왕복이 더 비싸다.

실행 명령 (T0-9 wrapper 경유가 표준. 직접 호출 시에도 아래 형식 준수):

    codex exec --skip-git-repo-check --ephemeral \
      -s workspace-write \
      -C /home/seunghyeong/deck-factory/work/<phase>/<task-id>/wt \
      -o /home/seunghyeong/deck-factory/work/<phase>/<task-id>/out/attempt-<N>/result.md \
      "$(cat /home/seunghyeong/deck-factory/work/<phase>/<task-id>/brief.md)"

- 경로 절대화: cwd, brief, out, schema 경로는 전부 절대 경로로 생성한다.
  상대 -o는 cwd(worktree) 기준으로 해석돼 회수가 깨질 수 있다.
- preflight 쓰기 검증: wrapper가 스폰 전에 out/attempt-<N>/에
  실제 파일을 생성해 쓰기 가능함을 확인한다. 실패 시 스폰 0건으로 중단.
  샌드박스가 cwd 밖 쓰기를 막는 환경에서는 결과 파일을 worktree 내부의
  지정 경로(wt/.out/result.md)에 쓰게 하고, wrapper가 게이트 전에
  out/attempt-<N>/으로 복사한다 — 어느 경로든 게이트 입력은 out/attempt-<N>/뿐이다.
- attempt 분리: 시도마다 out/attempt-0/, out/attempt-1/, ... 로 출력 경로를 분리한다.
  같은 경로 덮어쓰기 금지 — 실패 산출물이 성공처럼 skip되는 경로를 차단한다 (6절 skip 기준).
- 결과 회수는 -o 파일로만 한다. stdout 파싱 금지 (회수 레이스 제거).
- 병렬 실행은 T0-9 wrapper(vendored codex_spawn_runner 기반)로 —
  tasks.jsonl 한 줄 = 태스크 한 개 {id, prompt, cwd, out, schema?} (경로 전부 절대).
  PARALLEL 상한은 15 (PLAN.md 4절 codex 동시성).
  P4 배치(씬 코드 생성 포함)만 4~6으로 하향 (GPU/OOM, PLAN.md P4).
- 샌드박스: 분석/조사는 -s read-only, 파일 수정은 -s workspace-write + worktree 격리.
  --dangerously-bypass-approvals-and-sandbox는 쓰지 않는다 (codex-spawn §5 안전 규정).
- 구조화 결과가 필요한 태스크(예: 라이선스 표, 매핑표)는 --output-schema로 JSON 강제.
- 순차 단계 실행(단일 코어 작업)은 vendored skill_forge_runner의 stages.json으로 —
  runner가 codex exec 호출, 게이트, done 마커, 재개를 처리한다.
  태스크 간 의존은 forge가 아니라 DAG 러너(2.3) 소관이다.

선택 기준: 산출물이 코드/스크립트/템플릿/설정 파일인 모든 태스크.
스키마 설계·트레이드오프 판단이 본체인 태스크에는 쓰지 않는다.

### 1.2 claude 워커 — opus / sonnet 서브에이전트

Claude Code의 Agent 도구로 스폰한다. fable(메인 세션)이 브리프 파일 경로를 프롬프트에 넣어 호출하고,
서브에이전트의 최종 메시지가 아니라 지정된 산출 파일(판정 JSON, 테스트 코드)을 정본으로 회수한다.

- opus 서브에이전트: 판단 게이트 전담.
  적용 대상은 PLAN.md 5.4의 적용 목록 (P1 스타일 타일, P2 템플릿 시각 판정, P3 한글 렌더,
  P4 3b1b 스타일, P5 무드/브랜드, P6 타이틀 테스트·압축 팩트체크, P8 의미론 2차,
  P10 claims 팩트체크, Phase 5 블라인드 비교).
  모든 판정은 5.4 프로토콜 필수이며, 그 실체는 T0-8 judgment-infra 산출물이다 —
  앵커드 루브릭 파일, scripts/prompts/의 고정 프롬프트, 캘리브레이션 셋,
  판정자 사전 검증(일치율 90%) 결과, verdict.schema.json.
  T0-8 완료 전에는 어떤 opus hard 게이트도 스폰하지 않는다 (dag.json needs로 강제).
  판정 3회는 서브에이전트 3개를 별도 스폰해 컨텍스트를 격리한다.
  판정 결과는 work/<phase>/<task-id>/verdict/{1,2,3}.json으로 저장하고
  T0-8의 집계 하니스가 다수결을 집계해 verdict/final.json을 쓴다.
  final.json은 verdict.schema.json 검증을 통과해야만 게이트 입력으로 인정한다 —
  스키마는 rubricVersion, promptVersion, calibrationSetId, judgeQualification,
  표별 점수·근거, 다수결 결과, soft/hard 구분, 비용 로그 필드를 요구한다.
- sonnet 서브에이전트: 테스트 작성·실행 전담.
  red-first가 지정된 code 태스크는 3태스크로 분리해 순서를 강제한다 —
  sonnet-test-freeze(실패 테스트 작성·동결) → codex-implement → sonnet-regression(회귀 실행).
  sonnet이 쓰는 테스트 경로는 sonnet 브리프의 allowedWritePaths에 고정하고,
  같은 경로를 codex 브리프의 금지사항에 넣는다 (동시 수정 차단).
  API 시그니처가 고정되기 전에는 테스트 병렬 착수 금지 —
  골든 .in/.out 파일 작성만 코어와 병렬 안전 (플레이북 §3 반쪽 병렬 주의).
- 적대 검증(5.1 게이트)도 opus 서브에이전트 — 경계 입력/모호 브리프 공격,
  발견 결함은 sonnet이 실패 테스트로 고정한 뒤 codex 재작업.

선택 기준: 판단(opus) 또는 테스트(sonnet)가 산출물인 태스크.
opus에게 코드 구현을 시키지 않고, codex에게 게이트 판정을 시키지 않는다 (플레이북 §2).

### 1.3 fable — 오케스트레이터 (메인 세션)

실행자가 아니라 조율자. 직접 하는 일은 네 가지뿐이다.
- 브리프 작성: 태스크마다 brief.md를 파일로 저장 (3절 표준 포맷) + dag.json 등록 (2.3).
- 스폰과 회수: DAG 러너/wrapper 실행, claude 서브에이전트 호출, 산출 파일 존재 확인.
- 게이트 소집: 검증 스크립트 실행 결과 + sonnet 테스트 결과 + opus 판정을 모아 pass/fail 확정.
- 통합과 에스컬레이션: worktree 머지 + 통합 게이트, 재작업 브리프 갱신, 상한 도달 시 개입 판단.

컨텍스트 예산(PLAN.md 7절): 워커 산출물 본문을 메인 컨텍스트로 읽지 않는다.
매니페스트 요약 30줄 또는 4KB 중 작은 쪽만 수신, 초과분은 파일 경로로 대체.
게이트 판정은 스크립트 종료 코드와 verdict/final.json만 소비한다.


## 2. 태스크 분해 원칙

### 2.1 태스크 크기와 타입 정의

워커 1태스크 = 파일 계약으로 닫히는 최소 단위.
"닫힌다"의 정의: 태스크의 산출 파일이 deck-contracts 스키마(또는 4절 합격기준의 검사 스크립트)로
독립 검증 가능하고, 다른 태스크의 미완성 산출물을 읽지 않아도 게이트를 돌 수 있다.

태스크 타입 6분류 — 모든 태스크는 브리프와 dag.json에 taskType을 명시하고,
타입별 셀 변형(4절)을 따른다:

| taskType | 본체 | 대표 게이트 |
|---|---|---|
| code | 코드/스크립트/템플릿 구현 | 테스트 green + determinismClass별 검증 |
| test | 테스트·픽스처 작성 (red-first freeze 포함) | 실패 케이스가 실제로 red인지 확인 |
| judgment | 판단·판정·동결 문서 (T0-5, T5-2, T5-4류) | verdict 스키마 검증 + 다수결 기록. 해시 게이트 없음 |
| research | 조사·수집 (라이선스, 약관, 레퍼런스) | 구조화 산출 스키마 + evidence 경로 존재. 해시 게이트 없음 |
| render | 비LLM 렌더 실행 (manim, Playwright 매트릭스) | 잡 큐(T1-7) 경유 + artifact 존재 + 해시 |
| integration | 머지·루트 공유 파일·통합 게이트 | 통합 브랜치 게이트 green (순차 전용) |

표준 단위 예시 (PLAN.md 4절에서 도출):
- 차트 엔진 어댑터 1개 = 1태스크 (P3, 엔진당 1워커 — PLAN.md 워커 배정 명시)
- 레이아웃 템플릿 4종 묶음 = 1태스크 (P2, 20종 = 5태스크 — archetype 계열별로 묶는다)
- grader 규칙 1군(카테고리) = 1태스크 (P8, 6카테고리)
- 토큰 프리셋 1종 상수 추출 = 1태스크 (P1)
- 검증기/린터 1개 = 1태스크 (P6 액션 타이틀 린터, P10 커버리지 검사기 등)
- manim 씬 1개 렌더 = 렌더 큐 잡 1개 (P4 배치, render 타입)

크기 하한: 200줄급 단일 코어 리팩터/구현은 쪼개지 않고 통짜 1태스크로 —
쪼개면 통합·계약 디버깅이 병렬 이득을 잡아먹는다 (플레이북 §5 과병렬 안티패턴).
스키마 확정, plan 단계 해소 루프 같은 판단 연쇄 작업은 애초에 병렬 대상이 아니다 (5절에 순차 명시).
단 순차라도 내부 관심사가 여럿이면 sequential subtask로 쪼개고
subtask마다 골든 케이스 1개를 고정한다 (T3-2, T3-6이 이 경우 — 5절).

크기 상한 (Phase 0 실증 2026-07-03 — 원인은 계정 한도가 아니라 태스크 크기):
codex exec 1턴이 감당 못 하는 다산출 태스크는 도중 사망하거나 행이 된다.
실측 — 소형 T0-3(스크립트 2+테스트 1)은 3기 동시에서도 완주, 다산출 T0-4/T0-9는 사망,
T0-10은 세션 task_complete 후 파일 0개로 1.5시간 행. 사망 직후 소형 호출은 즉시 성공했으므로
계정 한도로 오진하지 말 것.
규칙: codex 1태스크의 산출은 코어 모듈 1개 + 그 테스트 (대략 신규 500줄, 파일 3~4개) 이내로
브리프를 설계한다. 그 이상은 sequential subtask 체인(T#-#a/b/c)으로 분해하고
subtask마다 자기 게이트(expectedCommand)를 갖는다.
반례 교훈: T0-4는 (a) 파서+리포트 골격 (b) hard fail 규칙 6종+픽스처 (c) yaml+constants sync,
T0-10은 (a) 스키마+로더+거부 규칙 (b) 팬아웃+재개 (c) 테스트로 나눴어야 했다.
Phase 1 이후 모든 브리프는 이 상한으로 작성한다.

리팩터형 태스크(slides-grab 이식 등)는 플레이북 §6 시퀀스를 따른다:
0 golden-freeze → 1 구조만(골든 green 유지) → 2 동작 수정 → 3 이중포맷 검증.
구조 변경과 동작 변경을 한 단계에 섞지 않는다.

### 2.2 파일 충돌 격리 규약

- 읽기 전용 태스크(분석·조사·리뷰): 격리 불필요, 같은 리포에 -s read-only로 병렬.
- 수정 태스크 전체: read-only를 제외한 모든 수정 워커는
  태스크 전용 git worktree + task branch(work/<phase>/<task-id>/wt)에서만 실행한다.
  패키지가 서로 달라도 예외 없다 — 서로 다른 packages/* 작업도
  루트 package.json, lockfile, workspace 설정, 공통 tsconfig, vendored contracts, CI 설정을
  동시에 건드릴 수 있고, 직접 cwd 작업 중 워커가 죽으면
  7절의 worktree 폐기 회수 절차가 성립하지 않기 때문이다.
  게이트 통과분만 fable이 머지하고, 머지 순서는 태스크 id 사전순으로 고정 (결정론).
- 루트 공유 파일(package.json, lockfile, workspace/tsconfig/CI 설정,
  계약 스키마, grader.yaml, 공통 어댑터층)의 수정은 병렬 전면 금지 —
  수정이 필요하면 integration 타입 순차 태스크로 승격하고 의존 태스크를 뒤로 민다.
  패키지 워커는 의존성 추가가 필요하면 루트를 고치지 않고
  out/attempt-N/deps-request.json에 요청만 기록한다.
  루트 의존성 갱신은 통합자(fable + integration 태스크)가 요청을 모아 한 번에 처리한다.
- 각 태스크의 sharedFiles 선언(2.3)이 겹치는 태스크는 DAG 러너가 동시 스폰을 거부한다.

### 2.3 실행 DAG 정본 — work/dag.json

5절 분배표는 사람이 읽는 뷰이고, 러너가 강제하는 정본은 work/dag.json이다 (T0-10 산출 스키마).
태스크별 필수 필드:

    {
      "id": "T2-2-adapter-vegalite",
      "taskType": "code",
      "worker": "codex",
      "needs": ["T2-1-poc-vegalite", "T0-8-judgment-infra"],
      "produces": ["packages/deck-charts/scripts/render-vegalite.mjs"],
      "consumes": ["contracts/chart-request.schema.json"],
      "sharedFiles": [],
      "dynamicChildren": null,
      "determinismClass": "deterministic",
      "mode": "attended"
    }

- needs: DAG 러너는 needs의 전 태스크가 integrated 상태(6절)가 아니면 스폰을 거부한다.
- produces/consumes: 계약 파일 흐름의 감사 근거. consumes가 미존재면 스폰 거부.
- sharedFiles: 선언 겹침 태스크의 동시 스폰 차단 (2.2).
- dynamicChildren: 동적 팬아웃 선언 — 부모의 산출(예: T2-1의 poc-result.json)을 읽어
  자식 tasks.jsonl과 dag 항목을 생성하는 expand 스크립트 경로를 지정한다.
  "PoC 통과 엔진만 어댑터 착수" 같은 조건 분기는 이 경로로만 구현한다.
- 대표 강제 의존: T2-2는 T2-1의 dynamicChildren, T2-14는 T2-12 전 규칙군 + T2-13,
  T2-17(P6 통합 검증)은 T2-7~T2-9 + T2-10,
  Phase 3의 90점 게이트 선언은 T2-14(1단계 캘리브레이션)를 needs로 가진다.
  모든 opus hard 게이트 태스크는 T0-8을 needs로 가진다.


## 3. 태스크 브리프 표준 포맷

브리프는 fable이 작성하고 반드시 파일로 저장한다 (재현성 — 같은 브리프 재실행 가능).
위치: work/<phase>/<task-id>/brief.md. 프롬프트는 이 파일 내용 그대로를 워커에 넘긴다.

필수 필드 (누락 시 스폰 금지):

    # TASK <task-id>
    ## 메타
    taskType: code|test|judgment|research|render|integration
    determinismClass: deterministic|canonicalized|nondeterministic
    mode: attended|unattended
    baseCommit: <워크트리 기준 커밋 해시>
    schemaVersion: <deck-contracts 버전 태그>
    ## 목표
    한 문단. 무엇을 만들고 무엇이 완료인지.
    ## 입력
    읽어야 할 파일의 절대 경로 목록 (스펙, 계약 스키마, 기존 코드).
    ## 산출
    allowedWritePaths: 쓸 파일 경로 + 포맷의 allowlist
    (예: packages/deck-charts/scripts/render-vegalite.mjs + tests/golden/vegalite/*.svg).
    allowlist 밖 파일 생성 금지.
    ## 합격기준
    PLAN.md 4절의 해당 파이프라인 정량 합격기준에서 이 태스크 몫을 문장 그대로 인용.
    expectedCommand: 검사 명령(테스트/검증 스크립트 실행줄) 명시.
    ## 금지사항
    공통: deck-contracts 스키마 수정 금지, 계약 필드명 변경 금지,
    폰트 축소 로직 도입 금지(1.2 불변식), allowedWritePaths 밖 쓰기 금지,
    자체 변환 상수 하드코딩 금지(deck-constants.json 로드).
    forbiddenSharedFiles: 루트 공유 파일 목록 (2.2 — 수정 금지, 필요 시 deps-request.json).
    태스크별 추가 금지를 여기에 명시.
    ## 참조
    관련 리서치 문서, 계약 문서, 재사용 자산의 경로.

재작업 브리프: 원본을 수정하지 않고 brief.retry-N.md로 새로 쓴다.
게이트 실패 근거(테스트 로그 경로, opus 판정 근거, measured 수치)를 앞에 덧붙이고
나머지는 원본을 인용한다 — 몇 번째 시도인지 파일만 보고 알 수 있어야 한다
(copy-reject.json의 attempt 영속 원칙과 동일 사상).
retry-N의 N은 out/attempt-N과 일치시킨다.


## 4. 표준 셀 (게이트 루프)

모든 태스크는 아래 셀을 돈다. skill-forge 원칙: 각 단계 게이트 통과 아니면 다음 없음.

    [1] fable: brief.md 작성 + dag.json 등록 (needs/sharedFiles 선언)
    [2] 워커 실행: attempt-N 분리 출력 (worktree 격리, -o 절대 경로 회수)
    [3] 기계 검증: 검증 스크립트 + sonnet 테스트 green + determinismClass별 재현성 검증
    [4] opus 판정: 판정 게이트가 걸린 태스크만. 5.4 프로토콜 = T0-8 하니스 실행
        (앵커드 루브릭 + 고정 프롬프트 + 독립 3회 다수결).
        verdict/final.json 산출 + verdict.schema.json 검증 통과
    [5] pass → state/attempt-N.passed + passed.json 기록 (상태: gated)
        → fable이 worktree 머지 (상태: merged)
        → 통합 브랜치에서 통합 게이트 재실행 (상태: integrated)
        → done을 atomic rename(done.tmp 작성 후 mv)으로 기록 → 다음 태스크
        fail → [6]
    [6] 재작업: brief.retry-N.md (실패 근거 포함)로 [2]부터 재진입 (out/attempt-N+1)

determinismClass별 [3]의 재현성 검증:
- deterministic: 같은 입력 2회 실행 산출물 해시 동일 — hard 게이트.
  (P7 compose HTML diff 0, P4 프레임 해시 등 PLAN.md가 결정론을 명시한 산출물)
- canonicalized: timestamp, cost, run id, retrievedAt 같은 volatile 필드를 제거한
  canonical JSON만 2회 비교 — 나머지 필드 동일이 hard 게이트.
- nondeterministic: 해시 게이트 없음. 스키마 검증 + 정량 지표(수율, 정밀도) 게이트만.
  (이미지 생성, opus 판정, claims 수집, 블라인드 비교 등)
해시를 전 태스크에 hard로 걸지 않는다 — 비결정 산출물의 실행을 막는 오적용이기 때문.

태스크 타입별 셀 변형 (2.1의 6분류):
- code: 표준 셀 그대로. red-first 지정분은 sonnet-test-freeze가 [2] 앞에 선행하고
  [3]의 테스트는 동결된 테스트의 회귀 실행(sonnet-regression)이다.
- test: [3]은 "실패 케이스가 red인지" 확인. [4] 없음.
- judgment: [2]가 opus/fable 판단 작업. [3]은 산출 문서/JSON의 스키마 검증만,
  해시 게이트 없음. [4]가 본체.
- research: [2]가 조사. [3]은 --output-schema JSON 검증 + evidence 경로 존재 확인.
  해시 게이트 없음.
- render: [2]가 렌더 큐(T1-7) 잡 제출. [3]은 artifact 존재 + 픽셀/해상도 검사 +
  deterministic 해시. LLM 호출 없음 — codex/claude 슬롯을 소비하지 않는다.
- integration: [2]가 머지·루트 파일 수정. [3]이 통합 브랜치 전체 게이트. 항상 순차.

mode 분기 (PLAN.md 5.3 실행 모드):
- attended(기본): 의미론 게이트 실패 또는 판정자 사전 검증 미달 시 사람 판정 승격.
  의미론 3항목(5.3)은 soft 강등 금지 — 사람 승격만.
  그 외 게이트의 판정자 미달은 5.4 규정대로 soft 강등 + 대리지표 재구성 또는 사람 승격.
- unattended(CI/무인): 결정론 게이트만 hard. 의미론 불합격 또는 판정자·사람 부재는
  파이프라인을 멈추지 않는다 — needsHumanReview 기록 + 종료 코드 review-required +
  draft 강등 산출(exports/draft/)로 끝난다. 사람 승격 대기 데드락을 만들지 않는다.
brief와 게이트 결과(passed.json)에 mode를 기록해 어느 분기로 통과했는지 감사 가능하게 한다.

규칙:
- [3]과 [4]는 순서 고정 — 기계 검증을 통과하지 못한 산출물을 opus에 올리지 않는다
  (판정 비용 절약 + 5.3의 "1차 필터 통과는 2차 진입 조건일 뿐"과 동형).
- 재시도 상한 2회. brief.retry-2.md까지 실패하면 워커 재스폰을 중단한다.
- 상한 도달 시 에스컬레이션 두 갈래:
  (a) fable 개입 — 태스크 분해가 잘못됐거나 브리프가 모호한 경우.
      태스크를 재분해하거나 브리프를 재작성하면 카운터는 0으로 리셋된다
      (새 태스크 id 부여 — 같은 id로 3회째 스폰 금지).
  (b) needsHumanReview — 판단 자체가 갈리는 경우(심미 판정 경합, 계약 모호).
      attended: work/<phase>/<task-id>/NEEDS-HUMAN.md에 쟁점을 기록하고 해당 태스크를 보류,
      의존하지 않는 다른 태스크를 계속 진행한다. 사람 결정 후 재개.
      unattended: 위 mode 분기의 review-required 종료 규약을 따른다.
- 게이트를 통과하지 못한 산출물은 절대 머지하지 않는다. 부분 산출물은 worktree에 남긴다 (7절 회수).
- done은 통합 게이트(integrated)까지 통과해야만 기록한다.
  개별 worktree 게이트 통과만으로는 passed.json까지만 쓴다 —
  머지 중 크래시 시 resume이 done을 보고 건너뛰는데 실제 변경이 통합되지 않는 사고를 차단한다.


## 5. Phase별 분배표

의존성 골격은 PLAN.md 6절: Phase 0 → 1 → {2, 3(골든 매니페스트로 조기 착수 가능)} → 4 → 5.
Phase 3의 90점 게이트는 Phase 2의 채점 스펙 확정·1단계 캘리브레이션에 의존.
러너 강제는 이 표가 아니라 work/dag.json(2.3)이다 — 표와 dag이 다르면 dag을 고친다.
표기: [순차]는 병렬 이득이 없어 순차로 고정하는 태스크 (플레이북 §3·§5).

### Phase 0. 기반 — 대부분 순차

스키마 확정이 본체라 과병렬 금지 구간이다. 오케스트레이션 인프라도 여기서 만든다.

| 태스크 | 워커 | 동시성 | 게이트 | 의존 |
|---|---|---|---|---|
| T0-1 deck-contracts 스키마 v1 초안 동결 [순차] | fable 설계 + codex 스크립트화, opus 계약 교차검증 | 1 | 스키마 CI green + opus 판정 (T0-8 전 soft — 표 하단 승격 규약) | 없음 |
| T0-2 인큐베이션 리포 packages/ + tools/orchestration/ 스캐폴딩 | codex | 1 | 구조 린트 | T0-1 |
| T0-3 vendored sync 스크립트 + diff CI | codex | 1 | sync 왕복 동작 + diff 검사 green | T0-1 |
| T0-4 grader 뼈대 (파서 + 기계검사 hard fail 6종 + grader.yaml 골격 + constants sync) [순차] | codex, sonnet 테스트 | 1 | 샘플 HTML 덱에 리포트 산출 | T0-1 |
| T0-5 골든셋 출처·포함기준 확정과 동결 문서 (judgment) | opus 조사 판정 + fable 확정 | 1 | 동결 문서 존재 | 없음 |
| T0-6 라이선스 잔여 확인 + evidence archive (research) | 원문 스냅샷 수집(fable WebFetch 또는 네트워크 허용 잡) → codex read-only 대조 4~5 병렬 + opus 판정 | 5 | 라이선스 표(--output-schema JSON) 완비 + license-evidence/에 원문 URL·캡처 날짜·스냅샷 저장 경로 기록. opus 판정은 T0-8 전 soft (표 하단 승격 규약) | 없음 |
| T0-7 hyperframes·slides-grab 커밋 핀 재클론 영속화 | codex(bash) | 1 | 클론 존재 + 해시 기록 | 없음 |
| T0-8 judgment-infra: opus 3표 다수결 판정 하니스 [순차] | fable 설계 + codex 하니스 구현 + opus 캘리브레이션 | 1 | 아래 스펙 | T0-5 |
| T0-9 codex-spawn attempt-분리 wrapper + 러너 vendoring | codex + sonnet 테스트 | 1 | 아래 스펙 | T0-2 |
| T0-10 DAG 태스크 러너 | codex + sonnet 테스트 | 1 | 아래 스펙 | T0-2, T0-9 |

Phase 0 opus 판정 승격 규약: T0-1/T0-6의 opus 판정은 T0-8 완료 전에는 soft 참고치다 —
게이트 확정은 기계 검증(스키마 CI, 라이선스 표·evidence 완비)만으로 하고,
opus 소견은 verdict/에 참고 기록으로만 남긴다. T0-8 integrated 직후 T0-8 하니스로
hard 재판정해 승격하며, 불합격이면 해당 산출물을 소비하는 후속 태스크를 보류한다.
선택 근거: T0-1은 Phase 0 대부분(T0-2/3/4, T0-9/10)의 선행 태스크라 T0-8 needs를 걸면
T0-5→T0-8이 크리티컬 패스 앞단에 끼어 Phase 0이 직렬 병목이 되므로 (b) soft 규약을 택했다.

신규 인프라 태스크 스펙 (0절 판단 기준의 산물):

T0-8 judgment-infra (신규).
- 입력: PLAN.md 5.3/5.4, T0-5 동결 골든셋(캘리브레이션 셋 파생원).
- 산출: scripts/prompts/의 고정 판정 프롬프트, 게이트별 앵커드 루브릭 파일,
  verdict.schema.json(rubricVersion/promptVersion/calibrationSetId/judgeQualification/
  표별 점수·근거/다수결/soft·hard/비용 필드), 캘리브레이션 셋(합격·불합격 각 10건 이상),
  판정자 사전 검증 결과 기록, 독립 컨텍스트 3표 스폰 + 다수결 집계 하니스 스크립트.
- 합격기준: 샘플 판정 3표가 verdict/{1,2,3}.json으로 저장되고 final.json이
  verdict.schema.json 검증을 통과하는 스모크 완주 +
  캘리브레이션 셋 다수결 일치율 90% 이상 기록(5.4 임계값) 또는 미달 판정자 명시.
- 모든 opus hard 게이트 태스크가 dag.json needs로 이 태스크를 소비한다.

T0-9 codex-spawn attempt-분리 wrapper + vendoring (확장).
- 입력: codex_spawn_runner.py·skill_forge_runner.py 원본 (0절 위치).
- 산출: tools/orchestration/에 vendored 러너 사본 + 버전·체크섬 기록 파일 +
  spawn_wrapper.py — attempt별 out/attempt-N/ 경로 생성, skip 기준을
  out 존재가 아니라 state/attempt-N.passed로 판정, 전 경로 절대화,
  preflight 쓰기 검증(실제 파일 생성), setsid로 process group 생성 + pgid 파일 기록.
- 합격기준: 실패 attempt 뒤 재실행 시 skip되지 않음(sonnet 테스트) +
  preflight 실패 시 스폰 0건 + kill이 기록된 pgid에만 전달되는 스코프 테스트.

T0-10 DAG 태스크 러너 (신규 — forge stages.json은 직렬 전용이라 확장 한계 초과.
게이트 루프·done 마커 사상만 forge에서 계승).
- 입력: dag.schema.json 설계(2.3 필드), T0-9 wrapper.
- 산출: tools/orchestration/dag_runner.py + dag.schema.json —
  needs 미충족·consumes 부재·sharedFiles 겹침 시 스폰 거부,
  dynamicChildren expand 스크립트 실행(부모 산출 → 자식 tasks.jsonl + dag 항목 생성),
  passed/done 마커 기반 재개.
- 합격기준: needs 미충족 스폰 거부 케이스 + 동적 팬아웃 케이스(모의 PoC 결과 →
  자식 생성) + 중단 후 재실행 시 integrated 태스크 skip 케이스 전부 sonnet 테스트 green.

완료 정의(PLAN.md Phase 0): 스키마 CI green(동기화 방식 포함) +
grader 샘플 hard fail 리포트 산출 + 골든셋 동결 문서 존재.
이 문서의 추가 완료 조건: T0-8~T0-10 합격 — 이것 없이 Phase 1 opus 게이트·병렬 스폰 금지.

### Phase 1. 파운데이션 (P1 + P2 + grader 규칙군 1차)

| 태스크 | 워커 | 동시성 | 게이트 | 의존 |
|---|---|---|---|---|
| T1-1 tokens 스키마 검증기·대비 검증기 vendored 이식 | codex | 1 | 골든 대비 계산 테스트 | Phase 0 |
| T1-2 프리셋 추출 x 8 (기존 design-* 5 + 국내 3) — Phase 1 최소 통과 기준 | codex, 프리셋당 1태스크 | 8 | 스키마 검증 + WCAG 대비 전수 + opus 스타일 타일 판정 4/5 (5.4) | T1-1, T0-8 |
| T1-3 Astryx 증류 프리셋 astryx-1..7 (개별 태스크, deferred backlog 허용 — Phase 1 완료 정의 불포함, PLAN P1 상세 범위) | codex, 프리셋당 1태스크 | 최대 7 | T1-2와 동일 게이트 + npm 버전·커밋 해시 메타 기록 | T1-1, T0-8 |
| T1-4 capacity 역산 스크립트 (deck-constants 로드) [순차] | codex | 1 | 실측 역산 출력 재현 해시 (deterministic) | Phase 0 |
| T1-5 레이아웃 템플릿 20종 = 4종 묶음 x 5 (archetype 계열별) | codex worktree 병렬 | 5 | Playwright 오버플로 0건 + 폰트 하한 DOM 검사 + opus 시각 판정 (5.4) | T1-4, T1-2 일부, T0-8, T1-7 (Playwright 매트릭스는 렌더 큐 경유) |
| T1-6 오버플로 검사기 + capacityFloors 산출기 | codex | 1 | 극단 콘텐츠 매트릭스 렌더 스냅샷 | T1-4, T1-7 (매트릭스 렌더는 렌더 큐 경유) |
| T1-7 비LLM 렌더 잡 큐 [인프라 신규] | codex + sonnet 테스트 | 1 | 아래 스펙 | T0-9 |
| T1-8 한도/예산 감시기 [인프라 신규] | codex + sonnet 테스트 | 1 | 아래 스펙 | T0-9, T0-10 |
| T1-9 grader 규칙군 1차 (타이포/컬러/정렬 3군) | codex, 규칙군당 1태스크 | 3 | 규칙별 양성/음성 케이스(sonnet) + 골든 리포트 스냅샷 | Phase 0 |

T1-7 비LLM 렌더 잡 큐 (신규).
- 입력: 렌더 잡 명세 jsonl {id, cmd, cwd, artifacts[], semaphoreClass(gpu|cpu), retries}.
- 산출: tools/orchestration/render_queue.py — 세마포어 상한(gpu 4~6, cpu 설정값),
  실패 자동 재시도 1회, artifact 존재 검증 + 해시 기록, LLM 호출 0.
- 합격기준: 더미 렌더 잡 매트릭스에서 동시 실행 수가 세마포어 상한을 넘지 않음(로그 검증) +
  재시도 케이스 + artifact 부재 시 fail 보고. 소비처: T2-15/T4-2b(manim),
  P2 Playwright 매트릭스(T1-5/T1-6) — 소비처는 T1-7을 needs로 선언한다.

T1-8 한도/예산 감시기 (신규).
- 입력: wrapper·러너 로그(429, rate limit 신호), work/**/logs/run.log.json (비용·호출 수).
- 산출: tools/orchestration/budget_watch.py — 한도 도달·임박 감지 시 신규 스폰 중지 신호,
  중단점 저장(checkpoint.json: 진행 중 태스크 목록·attempt 상태·수집된 verdict 표 수),
  재개 명령 문자열 출력(어느 태스크 디렉토리에서 무엇을 재실행할지).
- 합격기준: 모의 429 연발 시나리오에서 신규 스폰 0 + checkpoint.json 산출 +
  출력된 재개 명령으로 이어받기 스모크 완주.

피크 동시성 약 10~13 (T1-3 병행 시 상한 15 이내로 큐잉).
완료 정의(PLAN.md Phase 1): P1/P2 합격기준 전부 통과(프리셋 8종 이상) +
규칙군 골든 스냅샷 일치 + 토큰 → 레이아웃 → grader 관통 데모 1건.
이 문서의 추가 완료 조건: T1-7/T1-8 integrated —
Phase 2(T2-15 렌더 큐, T1-8 한도 감시)와 Phase 4(T4-2b)가
미완성 인프라를 소비하는 경로를 차단한다.

### Phase 2. 생성기 병렬 — 최대 병렬 지점 (P3 + P5 + P6 + P10 + grader 2차 + P4 PoC)

수정 태스크는 패키지가 달라도 전부 worktree 격리다 (2.2 — cwd 직행 폐지).
루트 공유 파일 수정은 integration 태스크로만.

codex 15슬롯의 실제 배치 (동시 상주 기준):

| 트랙 | 태스크 | codex 슬롯 | 게이트 |
|---|---|---|---|
| P3 deck-charts | T2-1 한글 골든 렌더 PoC x 4엔진 (Vega-Lite/ECharts/Mermaid/Graphviz) — 엔진별 첫 작업 [선행] | 4 | 한글 렌더 깨짐 0건, PNG를 opus 판정 (5.4). poc-result.json 산출 — 실패 엔진은 채택 제외 + 폴백 라우팅 갱신 |
| P3 | T2-2 엔진 어댑터 (T2-1의 dynamicChildren — PoC 통과 엔진만 expand 생성, 엔진당 1워커) | 최대 4 | 유형×엔진 supported 셀 골든 렌더 100% + 팔레트 파생색 대조 스크립트 |
| P3 | T2-3 유형 분류 라우터 + 테마 변환 공통층 [순차 — 공유 파일] | 1 | 라우팅 스펙 테스트(sonnet) |
| P5 deck-imagery | T2-4 C12 확장 프롬프트 컴파일러 / T2-5 구도 필터(분산도·OCR) / T2-6 오버레이 후처리 | 3 | 라벨셋 정밀도(sonnet) + OCR 회귀 + 오버레이 대비 4.5:1/3:1 재계산 테스트 + baked text 0건(OCR) 테스트 + image-manifest 스키마 검증 + opus 무드/브랜드 판정 (5.4) |
| P5 | T2-16 생성 실행 배치 (render/batch — codex-imagegen 동시성 15, codex 슬롯과 교대 운용) | 0 (교대) | 수율 기록(관리 기준선 60%, hard 아님 — PLAN P5) + 구도 필터 통과분 회수 |
| P6 deck-copy | T2-7 액션 타이틀 린터 / T2-8 압축 팩트체크 패스 + 6x6·발화시간 계산기 / T2-9 copy-reject 반려 처리기 | 3 | 린터 정밀도 코퍼스(sonnet) + opus 타이틀 테스트·팩트체크 (5.4). 조기 개발은 synthetic outline/claims로 진행, 실제 통합 코퍼스 검증은 T2-10 완료 후 T2-17이 기계 강제 (착수 순서가 아니라 검증 의존) |
| P10 deck-storyline | T2-10 claims 스키마 검증기 + 커버리지 검사기 / T2-11 titles-test 사전 린트 | 2 | 댕글링 0건 음성 케이스 + opus claims 팩트체크 (5.4) |
| P8 grader 2차 | T2-12 데이터시각화/신뢰성/접근성 규칙군 x 3 (규칙군당 1태스크, worktree 격리) | 3 | 규칙별 양성/음성 + 골든 리포트 |
| P6 통합 검증 | T2-17 P6 실제 코퍼스 통합 검증 (T2-7~9 산출물을 T2-10의 실제 claims/outline으로 재검증). needs: T2-7~T2-9, T2-10 | 1 | synthetic 검증과 동일 게이트(린터 정밀도 + opus 타이틀 테스트·팩트체크 5.4)를 실제 통합 코퍼스로 재실행 green |

합계 태스크 약 22개, 동시 상주 상한 15 — 초과분은 큐잉되고
wrapper의 PARALLEL=15 (또는 auto + MAX=15)가 자동 조절한다.

순차 구간 (병렬 금지 명시):
- T2-13 의미론 hard 게이트 (루브릭 3종 텍스트 고정 + 판정자 사전 검증 + 불합격 판정식) [순차] —
  opus 판정 체계 구축이 본체 (T0-8 하니스 소비). fable + opus,
  codex는 대리지표 1차 필터 스크립트만.
  산출: semantic gate 루브릭·판정식 파일 (T2-14가 소비).
- T2-14 채점 스펙 확정 (가중치·배점·집계식) + 1단계 캘리브레이션 [순차] —
  grader.yaml 단일 파일 수정 + 판단 연쇄.
  needs: T2-12 전 규칙군 integrated + T2-13 (의미론 게이트 산출물을 집계식에 연결).
  Phase 3의 90점 게이트 선행 조건이므로 이 태스크의 지연이 크리티컬 패스다.
- T2-15 P4 PoC 게이트 (수식 1컷 PNG → 3슬라이드 hyperframes → 5초 MP4 관통) [순차] —
  codex 1(글루 코드) + 렌더는 T1-7 큐 + fable 게이트 판단. 본 빌드는 Phase 4로 분리.

완료 정의(PLAN.md Phase 2): 각 파이프라인 합격기준 통과 + tokens.json 소비 크로스 검증 +
grader 종합점수 산출 가능(1단계 캘리브레이션까지).
이 문서의 추가 완료 조건: T2-17(P6 통합 검증) integrated —
synthetic 조기 개발분이 실제 통합 검증 없이 Phase 3/4로 흘러가지 않게 한다.

### Phase 3. 조립기 (P7) + 에디터 (P9) — 두 트랙 병행, 트랙 내부는 순차

P7은 판단 연쇄(plan 해소 루프)와 공유 계약 소비가 본체라 트랙 내부 과병렬 금지.
리팩터형이므로 플레이북 §6 시퀀스(골든 동결 → 구조 → 동작)를 stages.json으로 선언하고
vendored skill_forge_runner로 구동한다. 덩치 큰 순차 태스크는 sequential subtask로 쪼개고
subtask마다 골든 케이스 1개를 고정한다 (2.1).

| 태스크 | 워커 | 동시성 | 게이트 |
|---|---|---|---|
| T3-1 slides-grab 이식 (slide-mode.cjs 상수 제거 개조, image-contract) [순차] | codex | 1 | 골든 동결 green 유지 (구조 단계) |
| T3-2 plan 단계 [순차, sequential subtasks] — a 바인딩·수용량 검사 / b 해소 루프(copy-reject·image-reject 반려, kind별 터미널) / c 차트-출처 페어링 검증 / d measured-overflow 왕복 | codex + opus 설계 교차검증 | 1 | subtask별 골든 케이스 1개 고정: a 바인딩 골든, b 해소 3분기 + 반려 상한 케이스, c 페어링 음성 케이스, d 왕복 케이스 (sonnet) |
| T3-3 compose 단계 + slide-html 검증 통과 [순차] | codex | 1 | 결정론: 2회 실행 HTML diff 0 (deterministic 해시 게이트) |
| T3-4 뷰어 + Playwright 익스포터 (pdf/png/pptx, draft 격리) | codex 2 병렬 (뷰어/익스포터 파일 분리, worktree) | 2 | 익스포트 3포맷 스모크 + final/draft 게이트 케이스 |
| T3-5 시각 QA 루프 | opus 신선한 눈 서브에이전트 (T0-8 하니스) | 3 판정 | 체크리스트 검수 → fix → re-verify 1회 완주 |
| T3-6 deck-editor 이식 (P9, P7과 독립 병행 트랙) [sequential subtasks] — a 서버 + /api/apply 이식 / b bbox 편집 + undo 1단계 + 미리보기 / c 임의 HTML degrade + 재compose 차단 | codex 1 + sonnet API 테스트 | 1~2 | subtask별 골든 케이스: a API 통합 green, b 편집→재채점 왕복 + undo 케이스, c 임의 HTML 케이스 + --discard-edits 없는 덮어쓰기 거부 케이스 |

완료 정의(PLAN.md Phase 3): 골든 매니페스트+골든 deck-plan으로 E2E 덱 1벌,
잠정 합격선 90점 이상, 시각 QA 1회 완주, 해소 루프 3분기 케이스 통과, 에디터 왕복 1회.
골든 매니페스트 조기 착수 시 Phase 3 완료 선언은 Phase 2의 1단계 캘리브레이션 종료 후에만.

### Phase 4. 모션 본 빌드 (P4) + 오케스트레이터 (L3)

manim 렌더는 LLM 작업이 아니다 — codex는 씬 코드 생성까지만 맡고,
실제 렌더는 T1-7 비LLM 잡 큐로 돌려 codex quota를 태우지 않는다.
씬 코드 생성과 렌더가 같은 머신의 GPU/OOM 제약을 공유하므로
P4 배치 동시성 수치는 PLAN.md 그대로 4~6을 유지한다 (렌더 잡은 codex 슬롯 미소비).

| 태스크 | 워커 | 동시성 | 게이트 |
|---|---|---|---|
| T4-1 scenes.md → 씬 렌더 잡 분배 글루 + doctor(motion) | codex | 1 | doctor green + 씬 템플릿 3종 골든 렌더 |
| T4-2a manim 씬 코드 생성 (씬당 1태스크) | codex (wrapper 배치) | 4~6 | 씬 코드 lint + 드라이런(임포트·씬 클래스 검출) |
| T4-2b manim 씬 배치 렌더 (render 타입) | T1-7 렌더 큐, 씬당 1잡 | 세마포어 4~6 (15 금지 — GPU/OOM, PLAN.md P4) | 렌더 성공률 95%(재시도 1회 포함) + 배경 HEX 픽셀 검사 + 프레임 결정론 해시 (deterministic) |
| T4-3 hyperframes 합성 + 컷 판정 | codex 1 + opus 3b1b 판정 (5.4, T0-8) | 1 | 4/5 이상 |
| T4-4 deck-factory 얇은 라우터 + 진입 가드 [순차] | codex + fable 통합 | 1 | 아래 완료 정의 1차 → 2차 |

완료 정의(PLAN.md Phase 4, 2단계):
- 1차(선행): motion 자산이 전혀 없어도 브리프 1줄 → 최종 덱 E2E 완결
  (deck-motion 옵셔널 플러그인, doctor motion 프로파일 미설치 환경 포함).
- 2차: 브리프 1줄 → 최종 덱 + MP4 컷 포함 E2E.
  hyperframes 파손 시 manim 클립 ffmpeg concat 폴백 MP4로도 완료 인정 (PLAN.md 8절 완화책).

### Phase 5. 상업성 검증과 마감

| 태스크 | 워커 | 동시성 | 게이트 |
|---|---|---|---|
| T5-1 레퍼런스 덱 HTML 리빌드 x 3벌 (벌당 1태스크) | codex worktree 병렬 + opus 충실도 교차(폴백 경로 부분집합 대조) | 3 | 리빌드 충실도 교차 확인 |
| T5-2 2단계 캘리브레이션 + 합격선 근거 문서 [순차, judgment] | fable + opus | 1 | 조정 이력 YAML 기록 |
| T5-3 실제 주제 3건 덱 생산 | 전 파이프라인 E2E (덱당 순차, 3덱 병행) | 3 | hard fail 0 + 90점 |
| T5-4 블라인드 비교 + MBB 체크리스트 평가 (judgment) | opus 판정자(T0-8 사전 검증 통과자만) 쌍당 3회 다수결 | 판정 병렬 | 페어와이즈 50% 이상 + 체크리스트 통과율 90%. 호출 규모·중단 기준은 8절 판정 매트릭스 |
| T5-5 단독 상업 완성도 게이트 x 리포 (README/예제/실패 UX) | codex 병렬 + opus 콜드런 검수 | 리포당 1 | 5.1 (a)(b)(c) 전부 |


## 6. 디렉토리·상태 규약

    /home/seunghyeong/deck-factory/
      PLAN.md  WORKERS.md  research/
      incubator/                      # kimsh-1/deck-factory-incubator (packages/ + tools/orchestration/)
      work/
        dag.json                      # 실행 DAG 정본 (2.3)
        <phase>/                      # phase0 ... phase5
          <task-id>/                  # 예: T2-2-adapter-vegalite
            brief.md                  # 표준 브리프 (3절)
            brief.retry-N.md          # 재작업 브리프 (실패 근거 포함)
            tasks.jsonl               # wrapper 배치 태스크 (배치형만)
            wt/                       # git worktree (수정 태스크 전부, 2.2)
            out/attempt-N/            # 시도별 회수 파일 (덮어쓰기 금지)
            verdict/                  # opus 판정 1.json 2.json 3.json final.json
            logs/                     # 러너 stdout, 게이트 로그, run.log.json, pgid
            state/                    # attempt-N.passed / attempt-N.aborted / forge *.done
            passed.json               # 개별 게이트 통과 증거 (상태: gated)
            done                      # integrated 후에만 atomic rename으로 기록
            NEEDS-HUMAN.md            # 에스컬레이션 (b) 발생 시

태스크 상태 전이 (파일이 곧 상태):
- produced: out/attempt-N/ 산출 존재. 아직 아무 보증 없음.
- gated: 기계 검증 + (해당 시) opus 판정 통과 — state/attempt-N.passed + passed.json 기록.
  passed.json 내용은 게이트 증거 요약(테스트 rc, 해시 또는 canonical 비교 결과,
  verdict 경로, mode) — 빈 파일 금지.
- merged: fable이 worktree를 통합 브랜치에 머지.
- integrated: 통합 브랜치에서 통합 게이트(전체 테스트 + 스키마 diff) 재실행 통과.
  이때만 done을 기록한다 — done.tmp에 증거 요약을 쓰고 mv로 원자적 rename.
done 없이 passed.json만 있는 태스크는 "게이트는 통과했으나 미통합"으로 재개 대상이다.

git 추적 규칙 (work/ 하위):
- 추적: dag.json, brief*.md, tasks.jsonl, passed.json, done, verdict/*.json,
  state/*.passed, state/*.done, logs/run.log.json, NEEDS-HUMAN.md.
- ignore: wt/, out/, logs/의 나머지 전부 (대용량 산출·러너 stdout).

재개(resume) 방법:
1. forge 구동 태스크: 재실행 — done stage 자동 skip, 실패 지점부터.
2. wrapper 배치: 재실행 — skip 기준은 state/attempt-N.passed 존재.
   out/ 파일 존재는 skip 근거가 아니다 — 실패 attempt도 out을 남기기 때문 (T0-9 wrapper가 강제).
3. 전체 재개: fable이 dag.json과 work/를 스캔해 done(integrated) 없는 태스크 목록을 만들고,
   passed.json만 있는 태스크는 머지·통합 게이트부터,
   그것도 없는 태스크는 out/·wt/ 잔존물을 7절 회수 절차로 대조한 뒤 남은 것만 재스폰.
   메모리 상태에 의존하는 재개 금지 — 루프 위치는 파일(done, passed, retry-N, attempt)로만
   복원한다 (copy-reject attempt 영속 원칙과 동일).


## 7. 실패 처리

워커 죽음의 3형태와 회수 절차. 원칙: 상태 마커와 파일 산출 기반이면 항상 복구 가능하다 —
실제로 세션 한도로 워커가 중간에 죽은 사례를 상태 대조로 복구한 전례를 표준화한 것이다.

1. 워커 프로세스 죽음 (한도, 타임아웃, 크래시)
   - 판정: out/attempt-N/ 결과 파일 부재 또는 0바이트 (wrapper가 fail/timeout으로 보고).
   - 회수: 산출 파일이 없으면 부작용도 없다고 간주하지 않는다 —
     wt/(worktree) 잔존 변경을 git status로 대조:
     (a) 변경 없음 → 그대로 재스폰,
     (b) 부분 변경 있음 → 게이트를 먼저 돌려본다. 통과하면 passed.json 기록 후
         정상 머지·통합 경로로 진입(사실상 완료, 마커만 누락이던 경우),
         실패하면 worktree를 git worktree remove로 폐기하고 재스폰.
     부분 산출물을 다음 워커의 입력으로 승격하는 것은 금지 — 게이트 통과분만 존재한다.
2. 게이트 실패 (정상 종료, 산출 불합격)
   - 표준 셀 [6] 재작업 경로 (out/attempt-N+1). 재시도 상한 2회, 도달 시 에스컬레이션 (4절).
3. 부분 배치 실패 (N개 중 일부만 fail)
   - 런 안에서 무한 재시도 금지 (codex-spawn §5). 1패스 완료를 종료로 간주하고
     실패분은 다음 패스 resume에서만 재시도. 재시도 패스도 태스크당 2회 상한에 합산.

재스폰 기준:
- 같은 brief로 재스폰: 프로세스 죽음(1형)만. 게이트 실패(2형)는 반드시 brief.retry-N.md 갱신 후.
- 429/rate limit 검출 시: 예산 감시기(T1-8)가 신규 스폰 중지 + checkpoint 저장.
  fable은 PARALLEL을 절반으로 낮춰 재개.
- 잔여 프로세스 정리: 광범위 pkill -f "codex exec" 금지 —
  같은 머신의 무관한 codex 작업까지 죽인다.
  wrapper(T0-9)가 setsid로 만든 process group의 pgid를 logs/pgid에 기록하므로,
  정리는 kill -TERM -- -<pgid> → 유예 후 kill -KILL -- -<pgid>로 해당 그룹에만 보낸다.
  강제 kill 전에 진행 중이던 attempt는 state/attempt-N.aborted로 마킹해
  resume이 성공 산출과 혼동하지 않게 한다.


## 8. 비용·한도 가드

한도 감시는 예산 감시기(T1-8)가 상시 담당한다 —
한도 도달·임박 감지 → 신규 스폰 중지 → checkpoint.json 저장(진행 태스크·attempt·verdict 표 수) →
재개 명령 출력. 아래는 감시기가 구현하는 정책이다.

한도 도달 시 동작:
- codex(ChatGPT 계정 단위) 한도: 러너를 중단해도 상태는 이미 파일에 있다 —
  state/attempt-N.passed와 out/attempt-N/이 중단점이다.
  재개 명령: 감시기가 출력한 명령(해당 태스크 디렉토리에서 wrapper 재실행, 6절 재개 1·2번 경로).
  429 연발 시 PARALLEL 하향 후 재개, 세션 무효화 위험이 보이면 스폰 전면 중지 (codex-spawn 경고).
- claude(opus/sonnet) 한도: 판정 3표 중 일부만 수집된 상태로 중단되면
  verdict/에 남은 표 수를 세어 부족분만 추가 스폰한다 (표는 파일이므로 유실 없음).
  fable 세션 자체가 죽으면 새 세션이 dag.json + work/ 스캔(6절 재개 3번)으로 이어받는다 —
  이 문서와 brief 파일이 세션 간 인수인계 문서다.
- 한도 임박 신호가 오면 fable은 새 스폰을 멈추고 진행 중 워커의 자연 종료만 기다린다
  (강제 kill은 1형 회수 비용을 만든다).

Phase별 워커 호출 규모 어림 (재시도 1회분 여유 포함한 상한 어림):

| Phase | codex exec 호출 | opus 판정 호출 (3표 다수결 배수 포함) | sonnet 호출 |
|---|---|---|---|
| 0 | 15~22 (인프라 3태스크 포함) | 6~12 (계약 검증 + 라이선스 5건 x 판정) | 5~8 |
| 1 | 30~45 (프리셋 8+7 + 템플릿 5묶음 + 규칙군 3 + 인프라 2 + 재시도) | 45~75 (프리셋 8~15 + 템플릿 5 대상 x 3표) | 12~18 |
| 2 | 45~60 (태스크 21 + 재시도 + PoC) | 60~90 (PoC 4 + 판정 게이트 다수 x 3표) | 20~30 |
| 3 | 20~30 (순차 subtask 다수 + 케이스 수정) | 20~30 (시각 QA + 설계 교차) | 15~20 |
| 4 | 씬 코드 생성만 (씬 30개 가정 시 30~45, 동시 4~6 — 렌더는 큐라 codex 미소비) | 10~15 | 5~10 |
| 5 | 15~25 (리빌드 3 + 완성도 게이트) | 아래 판정 매트릭스 참조 | 5~10 |

Phase 5 opus 판정 매트릭스 (최대 구간 — 트랙별 분해):

| 트랙 | 표본 | 3표 배수 호출 |
|---|---|---|
| (a) 슬라이드 페어와이즈 (role·index 정합 쌍) | 최소 30쌍 | 90 |
| (b) 덱 단위 전체 평가 | 3건 페어와이즈 | 9 |
| (c) 핵심 슬라이드 subset (덱당 3장) | 9장 | 27 |
| MBB 체크리스트 (6항목 x 3덱) | 18셀 | 54 |
| 판정자 사전 검증 (우수/열위 쌍, 판정자별) | 10쌍 x 판정자 수 | 30~60 |
| 합계 | | 최소 약 210 ~ 최대 약 240 |

중단 기준: 한도 도달로 트랙 (a)의 최소 30쌍을 채우지 못하면 표본 축소로 때우지 않는다 —
checkpoint 저장 후 다음 한도 윈도에서 잔여 쌍만 재개한다 (표본 수는 착수 전 고정, PLAN.md 6절).
판정 호출 수·다표본 배수는 PLAN.md 7절 규정대로 런별 total_tokens/duration 로그에 포함해
가시화한다 (기록 위치: work/<phase>/<task-id>/logs/run.log.json).


## 9. PLAN.md 정합 자체 점검 기록

- 파이프라인 이름: P1 deck-tokens ~ P10 deck-storyline — 5절 분배표의 트랙명과 일치 확인.
- Phase 완료 정의: 0(스키마 CI + grader 샘플 리포트 + 골든셋 동결), 1(프리셋 8종 이상 +
  관통 데모 1건), 2(크로스 검증 + 종합점수 산출 가능), 3(E2E 1벌 + 잠정 90점 + QA 완주 +
  3분기 케이스 + 에디터 왕복), 4(1차 motion 부재 완결 / 2차 MP4 포함 — 별도 문단으로 명시),
  5(hard fail 0 x 3건 + 블라인드 통과선 + 5.1 게이트) —
  각 Phase 표의 완료 정의 문구가 PLAN.md 6절 인용임을 확인.
  Phase 0의 인프라 완료 조건(T0-8~T0-10)은 PLAN.md 완료 정의에 없는 이 문서의 추가 조건이며
  PLAN.md와 모순되지 않는다 (PLAN.md 4절 "실행 기반은 로컬 CLI 러너" 서두의 하위 실행 설계).
- 프리셋 수: Phase 1 최소 통과 기준 8종(기존 5 + 국내 3)은 PLAN.md Phase 1 완료 정의
  "8종 이상"과 일치. Astryx 7종 증류는 PLAN.md P1 상세 범위 — T1-3 개별 태스크로 분리하고
  deferred backlog를 허용해 커버리지를 명시했다.
- 동시성 수치: codex 15 (Phase 2 슬롯 배치 합계가 15 상한 준수),
  P4 배치 4~6 (T4-2a/b에 명시, 15 금지 병기 — PLAN.md P4의 GPU/OOM 제한 수치 유지.
  렌더를 비LLM 큐로 옮겨도 세마포어 상한은 같은 4~6이다),
  codex-imagegen 15 (T2-16 비고) — PLAN.md 4절과 일치.
  PLAN.md P4의 "씬별 렌더 잡 분배(codex-spawn)" 문구는 이 문서에서
  "분배 글루는 codex 산출물, 렌더 실행은 비LLM 큐"로 해석해 구현한다 —
  quota를 태우지 않는 실행 층 선택이며 PLAN.md 본문 수정은 불요.
- 재시도 상한: 워커 재작업 2회 = copy-reject/image-reject의 attempt 상한 2회와 동일 사상
  (카운터 파일 영속 원칙 포함). attempt 디렉토리 분리로 카운터가 경로에도 드러난다.
- 게이트 순서: 기계 검증 선행 → opus 판정 = 5.3 의미론 게이트의 1차 필터 → 2차 심사 구조와 동형.
- determinismClass: 해시 hard 게이트를 deterministic에 한정 —
  PLAN.md가 결정론을 명시한 지점(P7 compose diff 0, P4 프레임 해시)과 정확히 일치하고,
  PLAN.md가 비결정으로 규정한 산출(plan 단계, 이미지 생성, retrievedAt 포함 수집)에
  해시를 걸지 않는다.
- mode 분기: attended/unattended 게이트 동작이 PLAN.md 5.3 실행 모드
  (unattended = review-required 종료 + draft 강등, 의미론 soft 강등 금지의 attended 한정)과 일치.
- 워커 병렬은 로컬 CLI 러너, GitHub Actions는 게이트 검증 전용 — PLAN.md 4절 서두와 일치.
- 인프라 태스크(T0-8/9/10, T1-7/8)는 PLAN.md에 태스크로 존재하지 않으나
  PLAN.md 5.4(판정 프로토콜 실체), 6절(로드맵 게이트), 7절(비용 가시화)이 요구하는
  기능의 구현 태스크화다 — 0절 판단 기준의 적용 결과.
- 재크리틱 critical 5: T0-1/T0-6의 opus 판정을 T0-8 전 soft 참고치 + T0-8 후 hard 승격으로
  규약화(Phase 0 표 하단) — "T0-8 전 opus hard 게이트 금지"와 충돌 없이 Phase 0 병목 회피.
- 재크리틱 major 1: T1-5/T1-6 의존에 T1-7을 명시해 P2 Playwright 매트릭스의
  렌더 큐 소비 방향이 표와 dag.json에서 일치.
- 재크리틱 major 2: Phase 1 완료 정의에 T1-7/T1-8 integrated를 추가 완료 조건으로 명시 —
  Phase 2/4의 미완성 인프라 소비 경로 차단.
- 재크리틱 major 3: T2-17(P6 통합 검증)을 분배표·2.3 대표 의존에 신설(needs: T2-7~9 + T2-10)하고
  Phase 2 완료 정의에 연결 — synthetic 조기 개발의 실제 통합 검증을 DAG가 기계 강제.


## 10. 크리틱 반영·기각 기록 (workers-critique.md 대응)

critical 7건: 전량 반영.
1 attempt 분리 + passed 마커 skip (1.1, 6절, T0-9). 2 상태 4분리 + atomic done (4절 [5], 6절).
3 전 수정 워커 worktree 강제 + 루트 공유 파일 순차 승격 (2.2). 4 work/dag.json 정본 (2.3, T0-10).
5 T0-8 judgment-infra 신설 (Phase 0). 6 determinismClass 3분류 (3절, 4절).
7 절대 경로 + preflight 쓰기 검증 (1.1, T0-9).

major 12건: 반영 12, 기각 0.
타입 6분류 셀(2.1/4절), verdict.schema.json(T0-8), P5 게이트 보강 + 생성 배치 분리(T2-4~6/T2-16),
mode 분기(4절), red-first 3태스크 분리(1.2/4절), T2-13→T2-14 순차 의존(2.3/5절),
프리셋 8+Astryx 분리(T1-2/T1-3), 러너 vendoring(0절/T0-9), pgid 스코프 정리(7절),
T3-2/T3-6 subtask 분해(5절), manim 렌더 비LLM 큐 분리(T1-7/T4-2 — PLAN P4 문구와의
긴장은 9절 해석으로 해소), 라이선스 evidence archive(T0-6).

minor 5건: 전량 반영.
gitignore 분리(6절), brief 필드 추가(3절), Phase 4 완료 정의 문단(5절),
P6/P10 착수·검증 의존 분리(T2-7~9 비고), Phase 5 판정 매트릭스 표(8절).
