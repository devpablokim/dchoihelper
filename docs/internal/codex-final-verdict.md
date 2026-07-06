critical 1(title/source 오버플로 종료 모순): 해소 - releaseBlocked를 해소 실패 상태로 계약화하고 final 차단 및 draft 격리를 P7/deck-manifest 게이트로 연결함.
major 1(deck-manifest draft/export 상태 계약): 해소 - exportStatus/reviewRequired/releaseBlocked 필수 필드와 exports/draft/-draft 격리 규약이 추가됨.
major 2(chart sourceRef 신뢰성 연결): 해소 - 수치 차트 sourceRef를 claims/source-pack 실존 id로 강제하고 sourceLabel은 파생 표시값으로 낮췄으며 grader hard fail이 걸림.
major 3(Phase 5 privacyMode 벤치마크 경계): 해소 - 외부 벤치마크는 public 또는 sanitized synthetic만 허용하고 sensitive/confidential은 차단하는 조달 게이트가 추가됨.
신규 문제: 없음
verdict: pass
