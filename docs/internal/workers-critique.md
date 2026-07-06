# workers critique

critical

- WORKERS.md 4절 표준 셀과 6절 resume 규약이 서로를 깨뜨린다. 6절은 codex-spawn 배치 재실행 시 `out/<id>.md` 존재분을 자동 skip한다고 쓰지만, 4절은 게이트 실패 후 `brief.retry-N.md`로 재작업한다고 한다. 실패한 첫 실행도 `out` 파일을 남기므로 resume 시 실패 산출물이 성공처럼 skip될 수 있다. 수정안: skip 기준을 `out` 존재가 아니라 `done` 또는 `state/<attempt>.passed`로 바꾸고, `out/attempt-0/<id>.md`, `out/attempt-1/<id>.md`처럼 attempt별 출력 경로를 분리한다. codex-spawn runner가 out 존재 skip만 지원한다면 wrapper를 먼저 작성해야 한다.

- WORKERS.md 4절 [5]와 6절 done 규약은 통합 원자성이 없다. 현재 순서는 “pass -> done 마커 기록 -> worktree 머지”로 읽히며, 이 상태에서 머지 중 크래시가 나면 resume은 done을 보고 태스크를 건너뛰지만 실제 변경은 통합되지 않는다. 또한 개별 worktree 게이트 통과 뒤 통합 브랜치에서 다시 게이트를 돌리는 단계가 없다. 수정안: 상태를 `produced`, `gated`, `merged`, `integrated`로 분리하고, 태스크 최종 `done`은 머지 후 통합 게이트까지 통과한 뒤 atomic rename으로 기록한다. 개별 게이트 통과만으로는 `done`을 쓰지 말고 `passed.json`만 쓴다.

- WORKERS.md 2.2와 5절 Phase 2의 “패키지가 다르면 cwd 격리라 worktree 불필요”는 실제 파일 충돌을 막지 못한다. 서로 다른 `packages/*` 작업도 루트 `package.json`, lockfile, workspace 설정, 공통 tsconfig, incubator contracts 참조, CI 설정을 동시에 고칠 수 있다. 더 심각하게, direct cwd 작업 중 워커가 죽으면 7절의 worktree 폐기 회수 절차가 적용되지 않는다. 수정안: read-only를 제외한 모든 수정 워커는 task branch/worktree에서만 실행하고, 루트 공유 파일 및 lockfile 변경은 별도 순차 태스크로 승격한다. 패키지 작업자는 dependency 요청만 manifest에 기록하고 루트 의존성 갱신은 통합자가 한 번에 처리한다.

- WORKERS.md 5절 분배표는 사람이 읽는 표일 뿐 runner가 강제할 DAG가 없다. T2-2는 T2-1 PoC 통과 엔진만 대상으로 해야 하고, T2-14는 T2-12와 T2-13 이후여야 하며, Phase 3의 90점 게이트는 Phase 2 캘리브레이션 이후여야 한다. 그런데 codex-spawn `tasks.jsonl`에는 `needs`나 dynamic fanout 규약이 없다. 수정안: `work/stages.json` 또는 `work/dag.json`을 정본으로 만들고 각 task에 `needs`, `produces`, `consumes`, `sharedFiles`, `dynamicChildren`를 둔다. PoC 결과를 읽어 다음 tasks.jsonl을 생성하는 단계를 명시한다.

- WORKERS.md 1.2와 4절은 5.4 opus 판정 프로토콜을 요구하지만, Phase 1 첫 opus 게이트 전에 루브릭, 고정 프롬프트, 캘리브레이션 셋, 판정자 사전 검증 결과를 만드는 태스크가 없다. PLAN.md 5.4상 이 준비가 없으면 P1 스타일 타일, P2 템플릿, P3 한글 렌더 판정은 hard gate가 될 수 없다. 수정안: Phase 0에 `T0-8 judgment-infra`를 추가해 `scripts/prompts/*`, rubrics, verdict JSON schema, 캘리브레이션 셋, judge qualification 결과를 산출하고, 모든 opus 게이트가 이 산출물을 dependency로 소비하게 한다.

- WORKERS.md 4절 [3]의 “모든 태스크는 재현성 해시 필수”는 PLAN.md와 충돌하고 실행을 막는다. 이미지 생성, source ingest의 `retrievedAt`, claims 수집, opus 판정, Phase 5 블라인드 비교, 일부 라이선스 조사 산출은 본질적으로 비결정적이거나 시간이 박힌다. PLAN.md는 P7 compose, P4 프레임 등 특정 결정론 산출에 해시를 요구한다. 수정안: brief 필드에 `determinismClass: deterministic | canonicalized | nondeterministic`를 추가하고, 해시는 deterministic에만 hard gate로 둔다. canonicalized는 timestamp, cost, run id 같은 volatile 필드를 제거한 canonical JSON만 비교한다.

- WORKERS.md 1.1의 codex 실행 명령은 `-C work/<phase>/<task-id>/wt`와 상대 `-o work/<phase>/<task-id>/out/result.md`를 함께 쓴다. `-o`가 cwd 기준이면 결과가 worktree 내부의 중첩 경로에 쓰이고, sandbox가 cwd 밖 쓰기를 막으면 out 회수가 실패한다. 수정안: `cwd`, `brief`, `out`, `schema` 경로는 전부 절대 경로로 생성하고, runner preflight가 out 디렉토리 쓰기 가능 여부를 실제 파일 생성으로 확인한다. worktree 밖 out을 쓰지 못하는 CLI라면 결과 파일은 worktree 내부에 쓰고 fable이 게이트 전 복사한다.

major

- WORKERS.md 4절 표준 셀은 모든 태스크를 codex 구현 태스크처럼 다룬다. 하지만 T0-5 골든셋 동결, T5-2 캘리브레이션, T5-4 블라인드 비교는 판단/문서 태스크이며 codex 산출물이나 해시 게이트가 본체가 아니다. 수정안: task type을 `code`, `test`, `judgment`, `research`, `render`, `integration`으로 나누고 각 타입별 셀을 별도로 정의한다.

- WORKERS.md 1.2의 verdict 회수 규약은 파일 위치만 있고 스키마가 없다. PLAN.md 5.4가 요구하는 rubric version, prompt version, calibration set id, judge qualification, 다수결 근거, soft/hard 구분, 비용 로그가 없으면 다수결 집계와 사후 감사가 불가능하다. 수정안: `verdict.schema.json`을 Phase 0 산출물로 만들고 `verdict/final.json`은 이 스키마 검증을 통과해야만 게이트 입력으로 인정한다.

- WORKERS.md 5절 T2-4~T2-6의 P5 게이트가 PLAN.md 5.4 적용 대상인 무드/브랜드 opus 판정을 빠뜨렸다. PLAN.md P5 합격기준의 대비 재계산, 원치 않는 문자 0건, HTML 레이어 텍스트 보장도 OCR 회귀만으로는 덮이지 않는다. 수정안: P5 row에 `contrast overlay test`, `no baked text test`, `image-manifest schema`, `opus mood/brand verdict`를 명시하고 생성 실행 배치를 별도 task로 둔다.

- WORKERS.md 4절의 “opus 판정자 사전 검증 미달 시 soft 참고치로 강등”은 PLAN.md 5.3의 unattended 모드와 섞여 있다. 의미론 3항목은 사람 승격만이라고 쓰지만, PLAN.md는 unattended에서는 `needsHumanReview`와 draft 강등으로 진행한다고 한다. 수정안: brief와 게이트 결과에 `mode: attended | unattended`를 넣고, 의미론 게이트 실패 또는 판정자 부재 시 attended는 human escalation, unattended는 `review-required` 종료와 draft export로 분기한다.

- WORKERS.md 1.2는 sonnet이 “실패 케이스 먼저” 테스트를 만든다고 하지만 4절 표준 셀은 codex 구현 뒤 sonnet 테스트 green을 확인하는 순서다. 이러면 red-first 보장이 없고 codex와 sonnet이 같은 테스트 파일을 동시에 고칠 위험도 남는다. 수정안: 테스트 선행 태스크는 `sonnet-test-freeze -> codex-implement -> sonnet-regression`으로 분리하고, sonnet이 쓰는 테스트 경로를 brief의 산출 allowlist에 고정한다.

- WORKERS.md 5절 T2-13과 T2-14는 둘 다 grader 루브릭, 판정식, `grader.yaml`을 만질 가능성이 큰데 의존 관계가 불명확하다. T2-14는 T2-12 이후만 요구하고 T2-13 이후를 명시하지 않는다. 수정안: T2-13이 semantic gate schema/rubrics를 산출하고 T2-14가 이를 소비해 `grader.yaml` 집계식에 연결하도록 순차 의존을 추가한다.

- WORKERS.md 5절 T1-2의 프리셋 수가 PLAN.md와 어긋난다. PLAN.md Phase 1은 8종 이상(기존 5 + 국내 3)을 완료 정의로 쓰고, P1 상세는 Astryx 7개 테마를 증류한다고 한다. WORKERS는 “x 9, Astryx 1묶음”으로 축약해 실제 산출 커버리지가 불분명하다. 수정안: Phase 1 최소 통과 기준은 8종으로 두되, Astryx는 `astryx-1..7` 개별 preset 또는 명시적 deferred backlog로 분리한다.

- WORKERS.md 1절의 재사용 러너 경로가 홈 디렉토리의 mutable 파일에 묶여 있다. `~/behavior-skill-analysis/...`와 `~/.claude/skills/...`가 바뀌거나 새 세션에서 없으면 재현 실행이 깨진다. 수정안: Phase 0 preflight에서 runner version/checksum을 기록하고, 필요한 wrapper와 schema는 repo의 `tools/orchestration/`에 복사 또는 vendoring한다.

- WORKERS.md 7절의 광범위한 `pkill -9 -f "codex exec"` 정리는 같은 머신의 무관한 codex 작업까지 죽일 수 있다. 수정안: runner가 process group id와 pidfile을 기록하고, 정리는 해당 pgid에만 보낸다. 강제 kill 전에는 진행 중 out 파일을 `aborted` 상태로 마킹한다.

- WORKERS.md 5절 T3-2와 T3-6은 codex exec 단발 작업으로 너무 크다. P7 plan 단계는 바인딩, 수용량 추정, copy-reject, image-reject, chart-source pairing, measured-overflow 왕복을 모두 포함하고, P9 editor는 서버, bbox 편집, undo, 미리보기, 임의 HTML degrade까지 포함한다. 수정안: 공유 파일 때문에 병렬화는 제한하되 sequential subtasks로 쪼개고 각 subtask마다 골든 케이스를 하나씩 고정한다.

- WORKERS.md 5절 T4-2는 manim 씬 렌더를 codex-spawn 태스크로 취급한다. 렌더는 LLM 작업이 아니라 deterministic shell job이며 codex quota를 태운다. 수정안: codex는 씬 템플릿/코드 생성까지만 맡기고, 실제 manim 렌더는 non-LLM job queue로 돌린다. 렌더 worker에는 GPU/CPU semaphore와 artifact hash만 둔다.

- WORKERS.md T0-6 라이선스 조사는 codex read-only 병렬로 되어 있지만, 약관 원문 확인에는 네트워크 또는 저장된 원문 스냅샷이 필요하다. read-only 로컬 워커만으로는 최신 약관 검증이 성립하지 않는다. 수정안: 조사 입력에 원문 URL, 캡처 날짜, 저장 경로를 넣고, Phase 0 산출물로 license evidence archive를 만든다.

minor

- WORKERS.md 6절은 `work/`를 git 추적한다고 하면서 `wt/`, `logs/`, `out/`의 gitignore 규칙을 충분히 분리하지 않는다. 수정안: `work` 하위의 brief 파일, done 파일, verdict JSON, state done 마커만 추적하고 worktree, 대용량 산출, 로그는 ignore한다.

- WORKERS.md 3절 brief 포맷에는 base commit, schema version, allowed write paths, forbidden shared files, expected command가 없다. 수정안: 이 필드를 필수화해 resume과 리뷰 시 “무엇을 기준으로 작성됐는지”를 파일만 보고 알 수 있게 한다.

- WORKERS.md 9절 자체 점검은 Phase 완료 정의가 모두 일치한다고 쓰지만, Phase 4 표에는 PLAN.md의 “motion 없음 E2E 1차 완료”와 “MP4 포함 2차 완료”가 별도 완료 정의로 충분히 드러나지 않는다. 수정안: Phase 4에도 완료 정의 문단을 Phase 0~3처럼 명시한다.

- WORKERS.md 5절 Phase 2의 “P6보다 P10 선행 착수”는 착수 순서인지 완료 의존인지 애매하다. 수정안: P6은 synthetic outline/claims로 조기 개발 가능, 실제 integration corpus는 P10 완료 후라는 식으로 두 경로를 분리한다.

- WORKERS.md 8절의 opus 호출 수 추정은 Phase 5 블라인드 비교의 덱 단위 평가, 핵심 subset 평가, MBB 체크리스트 항목별 3회 판정을 모두 포함하는지 불명확하다. 수정안: Phase 5 판정 matrix를 별도 표로 풀어 최소/최대 호출 수와 중단 기준을 적는다.

verdict: revise
