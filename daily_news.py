# -*- coding: utf-8 -*-
"""My Agent Times — daily collector / curator / emailer.
Runs on GitHub Actions (weekday 07:30 KST). Fetches 6 outlets, filters politics,
curates with the Anthropic API (with a no-API fallback), renders the newspaper,
and emails it via Gmail SMTP."""
import os, re, ssl, json, html, smtplib, urllib.request, urllib.parse
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formataddr
import feedparser
from render import render_html

try:
    from zoneinfo import ZoneInfo
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = None

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
      "Accept":"application/xml,*/*","Accept-Language":"ko-KR,ko;q=0.9,en;q=0.8"}

def _fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25, context=CTX).read()
def _gn(q, hl="ko", gl="KR", ceid="KR:ko"):
    return f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl={hl}&gl={gl}&ceid={ceid}"

DIRECT = {
 ("CNBC","글로벌"):"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
 ("CNBC","테크"):"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
 ("CNBC","경영"):"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147",
 ("한국경제","경제"):"https://www.hankyung.com/feed/economy",
 ("한국경제","증권"):"https://www.hankyung.com/feed/finance",
 ("한국경제","테크"):"https://www.hankyung.com/feed/it",
}
GN = {
 ("매일경제","경제"):_gn("site:mk.co.kr when:2d (경제 OR 금리 OR 환율 OR 물가 OR GDP)"),
 ("매일경제","증권"):_gn("site:mk.co.kr when:2d (증시 OR 코스피 OR 주가 OR 실적 OR 외국인)"),
 ("매일경제","산업"):_gn("site:mk.co.kr when:2d (반도체 OR 자동차 OR 조선 OR 배터리 OR 산업)"),
 ("매일경제","경영"):_gn("site:mk.co.kr when:2d (경영 OR 인수 OR 합병 OR CEO OR 투자유치)"),
 ("이데일리","경제"):_gn("site:edaily.co.kr when:2d (경제 OR 금리 OR 환율 OR 물가)"),
 ("이데일리","증권"):_gn("site:edaily.co.kr when:2d (증시 OR 코스피 OR 주가 OR 실적)"),
 ("조선비즈","경제"):_gn("site:biz.chosun.com when:2d (경제 OR 금리 OR 환율 OR 물가)"),
 ("조선비즈","테크"):_gn("site:biz.chosun.com when:2d (반도체 OR AI OR IT OR 테크 OR 전자)"),
 ("조선비즈","산업"):_gn("site:biz.chosun.com when:2d (자동차 OR 조선 OR 배터리 OR 철강 OR 산업)"),
 ("AP","글로벌"):_gn("site:apnews.com when:2d (markets OR economy OR inflation OR Fed OR stocks OR earnings)","en","US","US:en"),
}
POL = ["대통령","대선","총선","국회","여당","야당","민주당","국민의힘"," 의원","청문회","탄핵","정상회담","외교부","검찰","구속","선거","정치","북한","미사일","전쟁","장관 ","의혹","수사",
       "election","senate","congress","parliament"," war","military","missile","impeach","airspace","shooting","epstein","nba","world cup"]
GN_SRC = {"매일경제","이데일리","조선비즈","AP"}

def _clean(s): return re.sub(r"\s+"," ",re.sub("<[^>]+>","",s or "")).strip()
def _ispol(t): tl=t.lower(); return any(k.strip().lower() in tl for k in POL)

def collect():
    out=[]
    for (src,sec),url in {**DIRECT,**GN}.items():
        try: d=feedparser.parse(_fetch(url))
        except Exception: continue
        for e in d.entries[:30]:
            title=_clean(e.get("title",""))
            if src in GN_SRC: title=re.sub(r"\s+-\s+[^-]+$","",title)
            if not title or _ispol(title): continue
            summ="" if src in GN_SRC else _clean(e.get("summary","") or e.get("description",""))[:200]
            out.append({"src":src,"sec":sec,"title":title,"summary":summ,"link":e.get("link","")})
    seen=set(); ded=[]
    for r in out:
        k=re.sub(r"[^0-9a-z가-힣]","",r["title"].lower())[:40]
        if k in seen: continue
        seen.add(k); ded.append(r)
    return ded

SECTION_ORDER=[("경제","ECONOMY"),("증권","MARKETS"),("테크","TECH"),("산업","INDUSTRY"),("경영","MANAGEMENT")]

def curate_api(cands):
    import anthropic
    client=anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    model=os.environ.get("MODEL","claude-sonnet-4-6")
    lines=[f'{i}\t[{c["src"]}/{c["sec"]}]\t{c["title"]}' for i,c in enumerate(cands)]
    gl_idx=[i for i,c in enumerate(cands) if c["src"] in ("CNBC","AP")]
    prompt=f"""너는 재무·투자·경영 컨설턴트를 위한 한국어 경제신문 'My Agent Times'의 편집장이다.
아래 후보 기사(인덱스 번호 포함) 중에서만 골라 오늘 자 지면을 편성하라. 정치·연예·스포츠·전쟁/지정학 기사는 제외.

규칙:
- 같은 사안이 여러 매체에 보이면 그날의 핵심이다. 중복은 하나로.
- 금리·환율·실적·M&A·규제·자금조달 등 의사결정에 직결되는 뉴스를 우선.
- 글로벌 마켓 6건은 반드시 CNBC 또는 AP 후보(src=CNBC/AP)에서만 고른다.
- 5개 섹션(경제/증권/테크/산업/경영)은 각 6건. 국내 매체 중심이되 적절하면 해외 포함.
- summary는 한국어 1문장(자작, 원문 복제 금지). implication(헤드라인 3건만)은 투자/경영 관점 1문장.
- dek은 오늘 흐름을 요약한 한국어 1문장. snapshot은 헤드라인에서 추론한 5개 지표(name/val/note 짧게).

반드시 아래 JSON만 출력(설명 금지). i는 후보 인덱스 정수:
{{"dek":"...","snapshot":[{{"name":"코스피","val":"...","note":"..."}}],
"headlines":[{{"i":0,"summary":"...","implication":"..."}}],
"global":[{{"i":0,"summary":"..."}}],
"sections":[{{"ko":"경제","en":"ECONOMY","items":[{{"i":0,"summary":"..."}}]}}]}}

후보:
{chr(10).join(lines)}"""
    msg=client.messages.create(model=model,max_tokens=3500,messages=[{"role":"user","content":prompt}])
    txt="".join(b.text for b in msg.content if getattr(b,"type","")=="text")
    txt=re.sub(r"^```(json)?|```$","",txt.strip(),flags=re.M).strip()
    j=json.loads(txt)
    def mk(i, summary, implication=None):
        c=cands[int(i)]
        d={"title":c["title"],"link":c["link"],"source":c["src"],"summary":summary}
        if implication is not None: d["implication"]=implication
        return d
    data={"dek":j["dek"],"snapshot":j["snapshot"][:5],
          "headlines":[mk(h["i"],h["summary"],h.get("implication","")) for h in j["headlines"][:3]],
          "global":[mk(g["i"],g["summary"]) for g in j["global"][:6]],
          "sections":[{"ko":s["ko"],"en":s["en"],"items":[mk(x["i"],x["summary"]) for x in s["items"][:6]]} for s in j["sections"][:5]]}
    return data

def curate_fallback(cands):
    by=lambda src,sec:[c for c in cands if c["src"]==src and c["sec"]==sec]
    def pick(pools,n):
        out=[];seen=set()
        for p in pools:
            for c in p:
                k=c["title"][:20]
                if k in seen: continue
                seen.add(k);out.append(c)
                if len(out)>=n: return out
        return out
    def itm(c,impl=False):
        d={"title":c["title"],"link":c["link"],"source":c["src"],"summary":c["summary"] or c["title"]}
        if impl: d["implication"]="시장 영향과 정책·전략 방향을 함께 점검."
        return d
    glob=[itm(c) for c in pick([by("CNBC","글로벌"),by("AP","글로벌"),by("CNBC","테크")],6)]
    secs=[]
    smap={"경제":[by("한국경제","경제"),by("매일경제","경제"),by("조선비즈","경제"),by("이데일리","경제")],
          "증권":[by("한국경제","증권"),by("매일경제","증권"),by("이데일리","증권")],
          "테크":[by("조선비즈","테크"),by("한국경제","테크")],
          "산업":[by("매일경제","산업"),by("조선비즈","산업")],
          "경영":[by("매일경제","경영"),by("CNBC","경영"),by("한국경제","증권")]}
    for ko,en in SECTION_ORDER:
        secs.append({"ko":ko,"en":en,"items":[itm(c) for c in pick(smap[ko],6)]})
    heads=pick([by("CNBC","글로벌"),by("한국경제","경제"),by("조선비즈","테크")],3)
    return {"dek":"오늘의 주요 경제·시장 흐름을 요약합니다.",
            "snapshot":[{"name":"코스피","val":"—","note":"장중 동향"},{"name":"원/달러","val":"—","note":"환율"},
                        {"name":"美 증시","val":"—","note":"전일"},{"name":"美 금리","val":"—","note":"국채"},{"name":"WTI","val":"—","note":"유가"}],
            "headlines":[itm(c,impl=True) for c in heads],"global":glob,"sections":secs}

def get_datestr():
    now=datetime.now(KST) if KST else datetime.utcnow()
    wd=["월","화","수","목","금","토","일"][now.weekday()]
    return f"{now.year}년 {now.month}월 {now.day}일 {wd}요일"

def publish_pages(html_doc):
    """Save today's newspaper as index.html and push to GitHub Pages."""
    import subprocess
    token=os.environ.get("GITHUB_TOKEN","")
    repo=os.environ.get("GITHUB_REPOSITORY","")
    if not token or not repo:
        print("GITHUB_TOKEN/REPOSITORY not set, skipping Pages publish")
        return
    actor=os.environ.get("GITHUB_ACTOR","github-actions")
    remote=f"https://{actor}:{token}@github.com/{repo}.git"
    for c in [["git","config","user.email","actions@github.com"],
               ["git","config","user.name","GitHub Actions"],
               ["git","remote","set-url","origin",remote]]:
        subprocess.run(c, check=True)
    open("index.html","w").write(html_doc)
    subprocess.run(["git","add","index.html"], check=True)
    result=subprocess.run(["git","diff","--cached","--quiet"])
    if result.returncode != 0:
        subprocess.run(["git","commit","-m","신문 자동 발행"], check=True)
        subprocess.run(["git","push","origin","main"], check=True)
        print("Pages published: index.html pushed")
    else:
        print("No changes to publish")

def send(html_doc, datestr):
    user=os.environ["GMAIL_USER"]; pw=os.environ["GMAIL_APP_PASSWORD"]
    to=os.environ.get("RECIPIENT","drcap10@gmail.com")
    msg=MIMEText(html_doc,"html","utf-8")
    msg["Subject"]=f"My Agent Times | {datestr} 조간"
    msg["From"]=formataddr(("My Agent Times",user)); msg["To"]=to
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=ssl.create_default_context()) as s:
        s.login(user,pw); s.sendmail(user,[to],msg.as_string())
    print("sent to",to)

def main():
    cands=collect()
    print("collected",len(cands),"candidates")
    try:
        data=curate_api(cands) if os.environ.get("ANTHROPIC_API_KEY") else curate_fallback(cands)
    except Exception as e:
        print("curate_api failed -> fallback:",repr(e)[:120]); data=curate_fallback(cands)
    datestr=get_datestr()
    data["date"]=datestr
    doc=render_html(data, sample=False)
    if os.environ.get("DRY_RUN")=="1":
        open("preview.html","w").write(doc); print("DRY_RUN: wrote preview.html"); return
    send(doc, datestr)
    publish_pages(doc)

if __name__=="__main__":
    main()
