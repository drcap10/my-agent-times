# -*- coding: utf-8 -*-
import json, re
from render import render_html
rows=json.load(open("news.json"))
def find(phrase, src=None):
    for r in rows:
        if phrase in r["title"] and (src is None or r["src"]==src): return r
    return None
SRC={"한국경제":"한국경제","매일경제":"매일경제","조선비즈":"조선비즈","이데일리":"이데일리","CNBC":"CNBC","AP":"AP"}
def it(phrase, src, summary, implication=None):
    r=find(phrase,src) or {"title":phrase,"link":"#","src":src or ""}
    d={"title":r["title"],"link":r["link"],"source":SRC.get(r["src"],r["src"]),"summary":summary}
    if implication is not None: d["implication"]=implication
    return d

data={
 "date":"2026년 6월 11일 목요일",
 "dek":("美 5월 소비자물가가 4.2%로 3년 만에 최고를 찍었다. Fed 인상론이 고개를 들고 이란발 충격까지 겹치며 "
        "코스피는 한때 4%대 급락했다 낙폭을 줄였다 — 반도체 대형주의 방향이 오늘 지수의 분수령이다."),
 "snapshot":[
   {"name":"코스피","val":"≈ 7,500","note":"▼ 장중 약 4% → 낙폭 축소"},
   {"name":"원/달러","val":"≈ 1,500원","note":"▲ 원화 약세 지속"},
   {"name":"美 5월 CPI","val":"+4.2% YoY","note":"3년래 최고"},
   {"name":"美 증시","val":"AI주 매도","note":"▼ 5주 전 수준 되돌림"},
   {"name":"WTI 유가","val":"▲ 상승","note":"중동 리스크"},
 ],
 "headlines":[
   it("Consumer prices rose 4.2% annually in May, highest in three years",None,
      "5월 미국 소비자물가가 1년 전보다 4.2% 올라 3년 만에 가장 높았다. 시장은 Fed의 다음 카드를 ‘인하’에서 ‘인상’ 쪽으로 빠르게 다시 계산하고 있다.",
      "금리 인하 시나리오에 선 포지션은 재점검이 필요하다. 채권 듀레이션과 성장주 밸류에이션에 직접적인 압박."),
   it("코스피 장중 7800선 붕괴","조선비즈",
      "중동 리스크에 외국인이 반도체를 내던지며 코스피가 장중 7,800선을 내주고 삼성전자·SK하이닉스가 5%가량 빠졌다. 이후 개인 매수로 낙폭은 일부 줄었다.",
      "지수의 방향은 결국 반도체 대형주에 달려 있다. 변동성 확대 국면, 단기 헤지와 분할 대응을 검토."),
   it("과징금 6247억","한국경제",
      "개인정보 유출로 쿠팡에 역대 최대 6,247억원의 과징금이 부과됐다. 회사는 ‘유감’을 표하며 법적 절차로 사실관계를 다투겠다고 밝혔다.",
      "데이터 거버넌스가 곧 재무 리스크다. 규제 비용을 밸류에이션과 실사 체크리스트에 반영해야 한다."),
 ],
 "global":[
   it("Asian shares slip after another sell-off of AI stocks",None,"월가의 AI주 매도세가 아시아로 번지며 증시가 약세, 유가는 반등."),
   it("Traders now see next Fed interest rate move as a hike",None,"물가 급등에 트레이더들이 Fed의 다음 행보를 ‘인상’으로 베팅하기 시작."),
   it("Private payrolls grew by 122,000 in May",None,"5월 민간고용이 12.2만 명 늘며 예상을 웃돌아, 노동시장은 아직 견조."),
   it("China’s exports jump 19.4% in May",None,"5월 중국 수출이 19.4% 급증, 자동차·기술 수요가 견인."),
   it("Energy prices take center stage as the ECB",None,"ECB 금리 결정을 앞두고 에너지 물가가 핵심 변수로 부상."),
   it("US home sales surge to the fastest pace this year",None,"모기지 금리 상승에도 미국 주택 판매가 올해 최고 속도로 반등."),
 ],
 "sections":[
   {"ko":"경제","en":"ECONOMY","items":[
     it("14년만에 외국환은행 고강도 검사","매일경제","당국이 14년 만에 외국환은행을 고강도 검사한다. 환율 안정 ‘신호’를 넘어 실제 행동에 나섰다는 해석."),
     it("GLP-1 쇼크","한국경제","미국이 비만치료제 가격 장벽을 낮추기로 하면서 관련주 변동성이 커지고 미 증시까지 흔들렸다."),
     it("KT&G 쓸어담는","한국경제","캐피털그룹에 이어 블랙록까지 KT&G 지분을 늘린다. 글로벌 큰손들이 주목하는 배경에 관심."),
     it("집값 뛰는데 성장도 양극화","매일경제","한은이 집값은 오르는데 성장은 양극화되는 구조적 불균형을 짚었다."),
     it("외화지준","한국경제","원/달러 급등에 대응해 한은이 외화 지급준비금 부리를 6개월 연장한다."),
     it("라면 연구소","한국경제","농심이 신라면 40주년을 맞아 성수동에 ‘라면 연구소’를 열고 제품 혁신에 나섰다."),
   ]},
   {"ko":"증권","en":"MARKETS","items":[
     it("코스닥 급등에 매수 사이드카","한국경제","코스닥이 급등하며 매수 사이드카가 발동될 만큼 변동성이 컸다."),
     it("4배 저평가","매일경제","이익은 TSMC를 압도하는데 주가는 여전히 4배가량 저평가라는 분석이 나왔다."),
     it("오라클","한국경제","오라클이 호실적에도 대규모 추가 자금조달 계획에 시간외에서 급락했다."),
     it("환율 1500원 뉴노멀","한국경제","원/달러 1,500원이 ‘뉴노멀’로 굳어지는지 시장이 시험받고 있다."),
     it("집까지 팔아","매일경제","일부 큰손이 집을 팔아서까지 삼성전자·SK하이닉스에 베팅할 만큼 반도체 쏠림이 뚜렷하다."),
     it("끄떡없다","한국경제","중국 CXMT 상장 우려에도 투자 고수들은 삼성전자를 최선호주로 꼽았다."),
   ]},
   {"ko":"테크","en":"TECH","items":[
     it("샘 올트먼 오픈AI CEO 14일 방한","조선비즈","샘 올트먼 오픈AI CEO가 14일 방한해 삼성전자·카카오·네이버를 만난다."),
     it("CXMT 상장","조선비즈","중국 CXMT 상장으로 ‘D램 3강’ 구도가 흔들릴지 메모리 판도 변화 조짐."),
     it("퓨리오사AI","조선비즈","국내 AI 반도체 스타트업 퓨리오사AI에 글로벌 큰손 무바달라가 투자의향서를 냈다."),
     it("삼성전자, 챗GPT","조선비즈","삼성전자가 챗GPT·제미나이·클로드를 동시 도입하며 사내 AI 전환을 본격화."),
     it("젠슨 황","조선비즈","젠슨 황의 ‘선물’ 뒤에 숨은 비용 구조를 짚으며 빅테크 낙관론에 경고를 던졌다."),
     it("OpenAI mulls slashing prices",None,"오픈AI가 앤트로픽과의 경쟁 속에 이용료 인하를 검토 중이라고 WSJ가 전했다."),
   ]},
   {"ko":"산업","en":"INDUSTRY","items":[
     it("반도체 수출 205%","매일경제","반도체 수출이 205% 폭증하며 열흘 새 110억 달러어치가 나갔다. 수출이 역대급."),
     it("최태원","매일경제","최태원 회장이 일본의 반도체 생태계를 평가하며 ‘AI팩토리’ 가동을 언급."),
     it("반도체 지방투자론","매일경제","초호황을 배경으로 반도체 지방 투자론이 부상, 패키징 중심의 점진적 확장이 거론."),
     it("China car exports jump 73%",None,"고유가로 EV 수요가 늘며 5월 중국 자동차 수출이 73% 급증."),
     it("산업구조 전환","매일경제","산업구조 전환에 대응하려면 전략적 지원과 금융정책 고도화가 필요하다는 진단."),
     it("Boeing to start 737 Max",None,"보잉이 7월 6일 새 조립라인에서 737 맥스 생산을 시작한다고 밝혔다."),
   ]},
   {"ko":"경영","en":"MANAGEMENT","items":[
     it("NH證 CEO 레이스","한국경제","NH투자증권 CEO 선임 레이스가 법적 분쟁으로 번지며 임원 보직해임 등 내홍."),
     it("Morgan Stanley will soon open",None,"모건스탠리가 1조 달러 규모 자산관리 부문에 AI 에이전트를 도입한다."),
     it("JPMorgan Chase plans to deploy",None,"JP모건이 올해 더 강력한 AI 에이전트를 배치할 계획."),
     it("Eli Lilly's top dealmaker",None,"일라이릴리 딜 책임자가 새 영역으로 넓히는 추가 M&A가 놀랍지 않을 것이라 시사."),
     it("Honeywell Aerospace readies",None,"하니웰 항공우주가 분사 독립 출범을 앞두고 큰 폭의 성장을 자신했다."),
     it("Palantir's Karp",None,"팔란티어 칼프 CEO가 기업들이 프런티어 AI 연구소에 불만이라고 진단했다."),
   ]},
 ],
}
html=render_html(data, sample=True)
open("/mnt/user-data/outputs/my_agent_times_sample.html","w").write(html)
miss=sum(1 for s in data["sections"] for x in s["items"] if x["link"]=="#")
miss+=sum(1 for x in data["global"]+data["headlines"] if x["link"]=="#")
print("sample written. broken links:",miss,"| bytes:",len(html))
