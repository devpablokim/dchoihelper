# TASK T1-2-kr-pick
## 메타
taskType: code / determinismClass: deterministic / mode: attended / baseCommit: 4feb240e651fda6db929b89bfc93acc01cfc0c2a / schemaVersion: v0.1.0-draft
## 목표
디자인 프리셋 "kr-pick" 를 deck-tokens 토큰으로 증류한다: (1) incubator/contracts/tokens.schema.json 을 만족하는 tokens.json, (2) 그 토큰만으로 렌더한 정적 스타일 타일 tile.html (16:9 1280x720 고정, 색상 팔레트 스와치·타이포 스케일·본문/제목 샘플·버튼/카드 1개 — 외부 리소스 0, 인라인 CSS만).
## 입력
/home/seunghyeong/deck-factory/research/korean-design-systems.md 에서 KRDS·토스 외 자산이 가장 풍부하고 상업적 이용 가능한 국내 시스템 1종을 네가 선택 (선택 근거를 tokens.json meta.rationale에 기록)
그리고 incubator/contracts/tokens.schema.json, incubator/packages/deck-tokens/scripts/{validate-tokens.mjs,contrast.mjs}
## 산출
allowedWritePaths: incubator/packages/deck-tokens/presets/kr-pick/tokens.json, incubator/packages/deck-tokens/presets/kr-pick/tile.html
## 합격기준
WORKERS.md T1-2 게이트 중 기계분: validate-tokens.mjs 스키마 검증 통과 + 스키마가 정의한 색상쌍 전수 WCAG 대비 통과 (미달 쌍은 명도만 조정하고 tokens.json meta.adjustments에 원색과 조정 사유 기록). opus 스타일 타일 판정은 후속 게이트로 fable이 실행한다.
expectedCommand: cd incubator && node packages/deck-tokens/scripts/validate-tokens.mjs packages/deck-tokens/presets/kr-pick/tokens.json
## 금지사항
contracts/ 수정 금지. 폰트 하한 미만 크기 토큰 금지 (deck-constants.json fontFloors 준수). 외부 웹폰트 URL 임베드 금지 (폰트는 이름만 선언). allowedWritePaths 밖 쓰기 금지. 다른 프리셋 디렉토리 접근 금지.
