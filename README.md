# My Agent Times — 매일 자동 발송 신문

평일 아침 07:30(KST)에 한국경제·조선비즈·매일경제·이데일리·CNBC·AP에서
경제·증권·테크·산업·경영 뉴스만 골라 신문 형식 HTML로 만들어 이메일로 보냅니다(정치 제외).

## 구성
- `daily_news.py` — 수집 → 정치 필터 → AI 큐레이션 → 렌더 → 메일 발송
- `render.py` — 신문 HTML 렌더러 (조선일보명조/나눔명조)
- `build_sample.py` — 견본 1부 생성 (로컬 미리보기용)
- `.github/workflows/daily-news.yml` — 매일 평일 07:30 KST 실행

## 1회 설정 (약 10분)
1. **GitHub 저장소 생성** 후 이 폴더의 파일을 모두 업로드합니다.
2. **Gmail 앱 비밀번호 발급**: Google 계정 → 보안 → 2단계 인증 ON → '앱 비밀번호' 생성(16자리).
   (보안상 일반 비밀번호가 아니라 반드시 '앱 비밀번호'를 사용하세요.)
3. **Anthropic API 키 발급**: console.anthropic.com → API Keys.
4. **저장소 Secrets 등록** (Settings → Secrets and variables → Actions → New repository secret):
   - `GMAIL_USER` = 보내는 Gmail 주소 (예: yourname@gmail.com)
   - `GMAIL_APP_PASSWORD` = 위 16자리 앱 비밀번호
   - `ANTHROPIC_API_KEY` = Anthropic 키
   - `RECIPIENT` = drcap10@gmail.com  (생략 시 기본값 동일)
   - `MODEL` = claude-sonnet-4-6  (선택, 생략 가능)
5. **Actions 탭에서 워크플로 활성화** → `Run workflow`로 즉시 1회 테스트.

> 비밀번호·API 키는 본인이 직접 Secrets에 입력하세요(보안). 코드에는 저장하지 않습니다.

## 참고
- GitHub Actions cron은 UTC 기준이라 `22:30 UTC(일~목) = 07:30 KST(월~금)`로 설정돼 있습니다.
  GitHub 부하에 따라 수 분 지연될 수 있습니다.
- API 키가 없거나 호출이 실패해도, 규칙 기반 폴백으로 신문은 발송됩니다(요약·함의 품질만 낮아짐).
- 로컬 미리보기:  `DRY_RUN=1 python daily_news.py`  → `preview.html`
- 소스/섹션/필터는 `daily_news.py` 상단의 `DIRECT`, `GN`, `POL`에서 수정합니다.
