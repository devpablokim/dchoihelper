critical 1: 해소 - attempt별 out/attempt-N 경로와 state/attempt-N.passed skip 기준이 1.1, 6절, T0-9에 규약화됐다.
critical 2: 해소 - produced/gated/merged/integrated 상태 전이와 integrated 후 atomic done 기록이 4절, 6절에 명시됐다.
critical 3: 해소 - 모든 수정 워커 worktree 강제, 루트 공유 파일 integration 순차 승격, deps-request 경로가 2.2에 명시됐다.
critical 4: 해소 - work/dag.json을 러너 정본으로 두고 needs, sharedFiles, dynamicChildren 및 대표 의존을 2.3, T0-10에 둔 것은 충분하다.
critical 5: 미해소 - T0-8은 신설됐지만 Phase 0 표의 T0-1/T0-6에 T0-8 needs 없는 opus 판정이 남아 있어 "T0-8 완료 전 opus hard 게이트 금지"와 충돌한다.
critical 6: 해소 - determinismClass 3분류와 해시 적용 범위가 3절, 4절에 명시돼 PLAN.md의 결정론/비결정 산출 구분과 맞는다.
critical 7: 해소 - 경로 절대화, preflight 쓰기 검증, cwd 밖 쓰기 불가 시 worktree 내부 out 복사 경로가 1.1, T0-9에 명시됐다.

신규 critical: 없음

잔여 major급 우려 1: T1-7은 P2 Playwright 매트릭스 소비처라고 쓰지만 T1-5/T1-6 의존에 T1-7이 없어 Phase 1 내부 DAG가 표와 다르게 열릴 수 있다.
잔여 major급 우려 2: T1-7/T1-8이 Phase 1 정식 인프라 태스크인데 Phase 1 완료 정의에 추가 완료 조건으로 포함되지 않아 Phase 2/4 소비 전 integrated 강제가 약하다.
잔여 major급 우려 3: P6은 synthetic으로 조기 개발하고 실제 통합 검증은 T2-10 후라고 설명하지만 별도 검증 태스크나 needs가 없어 DAG가 후행 검증을 기계적으로 강제하기 어렵다.

verdict: revise
