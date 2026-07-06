# TASK T3-5-visual-qa (opus 신선한 눈 시각 QA 루프 — fable 주관, codex는 fix만)
## 개요 (fable 실행 계획 — 이 파일은 기록용)
1. T3-4b 익스포터로 golden-compose 덱을 PNG 익스포트
2. opus 3표 판정 (T0-8 하니스, PNG Read 방식 — 체크리스트: 위계/정렬/여백/가독/드리프트)
3. 지적사항을 codex fix 태스크로 변환 (fix 브리프에 지적 인용) → 재익스포트 → re-verify 1회 완주
4. 게이트: re-verify에서 pass (WORKERS T3-5 — 체크리스트 검수 → fix → re-verify 1회 완주)
baseCommit: (T3-4 통합 후 기록)
