# TASK T2-15-motion-poc (P4 PoC 게이트 — 리스크 조기 노출이 목적, 실패도 유효 결과)
## 메타
taskType: code / determinismClass: nondeterministic / mode: attended / baseCommit: d67fa8b745a5da21e4b00df63a2ad7ae3e2b9283
## 목표
모션 파이프라인 최소 관통: (1) manim CE를 유저 공간에 설치 시도 (pip install --user manim.
pycairo/ManimPango 빌드가 시스템 헤더 부족으로 실패하면 pip 바이너리 휠 우선, 그래도 안 되면
설치 불가 사실과 필요한 시스템 패키지 목록을 기록하고 중단 — 이것도 PoC 완료다),
(2) 설치되면 LaTeX 없이 Text() 기반 수식 근사 씬 1컷을 PNG 렌더 (--format png),
(3) PNG 3장(정지컷 변형)을 ffmpeg concat으로 5초 MP4 생성 (hyperframes는 이번 PoC 범위 밖 —
vendor/hyperframes 존재만 확인해 기록).
## 산출
allowedWritePaths: incubator/packages/deck-motion/poc/ (설치 로그, 씬 코드, out/, poc-result.json {installed, rendered, mp4, blockers[]})
## 합격기준
poc-result.json이 정직한 상태 기록과 함께 존재. mp4 성공 시 5초±1 길이 검증.
expectedCommand: node -e "const r=require('/home/seunghyeong/deck-factory/incubator/packages/deck-motion/poc/poc-result.json');console.log(JSON.stringify(r).slice(0,200));process.exit(0)"
## 금지사항
시스템 전역 설치(sudo) 금지. 1200초 내 설치 안 풀리면 blockers 기록하고 포기할 것 (무한 씨름 금지).
