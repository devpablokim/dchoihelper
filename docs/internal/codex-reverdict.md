이전 critical 재심사

1. critical 1: 미해소 — kind별 overflowPolicy, splitGranularity, copy-reject 순서는 들어왔지만 2.3/P7에서 title/source 상한 도달 시 "현 카피 유지"로 종료한다. 이는 1.2/P7의 "오버플로 해소 완료 deck-plan" 및 P7 compose 실측 오버플로 0 익스포트 게이트와 충돌하므로 계약 수준 해소가 아니다.
2. critical 2: 해소 — image-manifest에 focalBox/textSafeRegions/ocrFindings/recommendedCropCandidates가 추가됐고 deck-plan binding.transform 및 image-reject.json/2회 상한/토큰 배경 폴백까지 생겨 파일 핸드오프가 닫혔다.
3. critical 3: 해소 — chart-manifest에 caption/sourceLabel/sourceUrl/retrievedAt/dataHash/units/caveat가 추가되고 deck-plan의 차트-출처 페어링 스키마 검증 및 plan 실패 규칙이 들어왔다.
4. critical 4: 해소 — P9가 final artifact editor로 재정의되고 edit-manifest.json이 deck-plan/deck-manifest invalidation 및 재compose 차단을 계약화했다.
5. critical 5: 해소 — P3 매트릭스가 supported/required_fallback/not_applicable로 바뀌고 CI hard gate가 기본 엔진+지정 fallback으로 제한됐다.

신규 critical

없음

잔여 major급 우려

1. 5.3/P7: unattended draft export는 "draft로 표시"한다고만 되어 있고 deck-manifest/export 계약에 exportStatus, reviewRequired, releaseBlocked 같은 기계 판독 필드가 없다. draft가 전달용 산출물과 섞이지 않도록 계약 필드를 추가해야 한다.
2. P8/P10/P3: chart sourceLabel 문자열과 claims/source-pack 계층이 느슨하게만 연결된다. 수치 차트의 sourceRef를 source-pack 또는 claims id로 강제하고, sourceLabel은 표시용 파생값으로 낮춰야 신뢰성 게이트가 조작 가능한 문자열에 의존하지 않는다.
3. Phase 5/2.3: Gamma/Beautiful.ai 벤치마크는 privacyMode 경계와 별도 서술이라 실제 발표 주제가 sensitive/confidential일 때 외부 투입 차단이 프로토콜에 직접 걸려 있지 않다. Phase 5 조달 조건에 public 또는 sanitized synthetic 입력만 허용하는 게이트를 명시해야 한다.

verdict: revise
