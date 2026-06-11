# -*- coding: utf-8 -*-
"""Shared newspaper renderer for My Agent Times (used by sample + daily job)."""
import html

PAPER="#f7f4ec"; INK="#191613"; RED="#9b2226"; RULE="#d6cdb8"; MUT="#6f665a"; BAND="#9b2226"
DISP="'ChosunIlboMyungjo','Nanum Myeongjo',Georgia,'바탕',serif"
BODY="'Nanum Myeongjo','ChosunIlboMyungjo',Georgia,serif"
LBL="'Helvetica Neue',Arial,'Apple SD Gothic Neo','맑은 고딕',sans-serif"

def esc(s): return html.escape(str(s), quote=True)

def _art(it, big=False):
    ts="19px" if big else "15px"
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
      <tr><td style="padding:0 0 3px;"><a href="{esc(it['link'])}" style="color:{INK};text-decoration:none;font-family:{DISP};font-size:{ts};line-height:1.28;font-weight:700;">{esc(it['title'])}</a></td></tr>
      <tr><td style="padding:0 0 4px;font-family:{BODY};font-size:12.5px;line-height:1.55;color:#34302a;">{esc(it['summary'])}</td></tr>
      <tr><td style="font-family:{LBL};font-size:10px;letter-spacing:.08em;color:{RED};text-transform:uppercase;font-weight:700;">{esc(it['source'])}</td></tr>
    </table>"""

def _twocol(items):
    c=[_art(x) for x in items]
    if len(c)%2: c.append("&nbsp;")
    n=len(c); rows=""
    for r in range(0,n,2):
        bb="" if r+2>=n else f"border-bottom:1px solid {RULE};"
        rows+=(f'<tr><td width="50%" valign="top" style="padding:9px 14px 11px 0;border-right:1px solid {RULE};{bb}">{c[r]}</td>'
               f'<td width="50%" valign="top" style="padding:9px 0 11px 14px;{bb}">{c[r+1]}</td></tr>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">{rows}</table>'

def _sechead(ko,en):
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;margin:20px 0 6px;">
      <tr><td style="border-top:2px solid {INK};padding-top:5px;">
        <span style="font-family:{DISP};font-size:18px;font-weight:700;color:{INK};">{ko}</span>
        <span style="font-family:{LBL};font-size:10px;letter-spacing:.18em;color:{MUT};padding-left:8px;">{en}</span>
      </td></tr></table>"""

def _headlines(hs):
    lead=hs[0]
    def impl(t): return f'<div style="font-family:{LBL};font-size:11px;line-height:1.5;color:{INK};background:#efe9da;border-left:3px solid {RED};padding:6px 9px;margin:6px 0 0;"><b style="color:{RED};">함의</b>&nbsp;&nbsp;{esc(t)}</div>'
    lead_html=f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;padding-bottom:12px;">
      <tr><td style="padding:0 0 5px;"><a href="{esc(lead['link'])}" style="color:{INK};text-decoration:none;font-family:{DISP};font-size:27px;line-height:1.18;font-weight:800;">{esc(lead['title'])}</a></td></tr>
      <tr><td style="font-family:{BODY};font-size:13.5px;line-height:1.6;color:#2c2822;">{esc(lead['summary'])}
        <span style="font-family:{LBL};font-size:10px;letter-spacing:.08em;color:{RED};text-transform:uppercase;font-weight:700;padding-left:6px;">{esc(lead['source'])}</span></td></tr>
      <tr><td>{impl(lead['implication'])}</td></tr></table>
      <div style="border-bottom:1px solid {RULE};margin:0 0 12px;"></div>"""
    def sub(h):
        return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
          <tr><td style="padding:0 0 4px;"><a href="{esc(h['link'])}" style="color:{INK};text-decoration:none;font-family:{DISP};font-size:18px;line-height:1.25;font-weight:700;">{esc(h['title'])}</a></td></tr>
          <tr><td style="font-family:{BODY};font-size:12.5px;line-height:1.55;color:#2c2822;">{esc(h['summary'])}
            <span style="font-family:{LBL};font-size:9.5px;letter-spacing:.08em;color:{RED};text-transform:uppercase;font-weight:700;padding-left:5px;">{esc(h['source'])}</span></td></tr>
          <tr><td>{impl(h['implication'])}</td></tr></table>"""
    two=f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
      <tr><td width="50%" valign="top" style="padding:0 16px 0 0;border-right:1px solid {RULE};">{sub(hs[1])}</td>
          <td width="50%" valign="top" style="padding:0 0 0 16px;">{sub(hs[2])}</td></tr></table>"""
    return lead_html+two

def _globalband(items):
    cells=[]
    for it in items:
        cells.append(f"""<td width="33.33%" valign="top" style="padding:9px 13px;border-right:1px solid #b9402f;border-bottom:1px solid #b9402f;">
          <a href="{esc(it['link'])}" style="color:#fff;text-decoration:none;font-family:{DISP};font-size:13px;line-height:1.3;font-weight:700;">{esc(it['title'])}</a>
          <div style="font-family:{BODY};font-size:11px;line-height:1.5;color:#f3d9d4;padding-top:3px;">{esc(it['summary'])}</div>
          <div style="font-family:{LBL};font-size:9px;letter-spacing:.1em;color:#f7c9c2;text-transform:uppercase;font-weight:700;padding-top:3px;">{esc(it['source'])}</div></td>""")
    rows=""
    for i in range(0,len(cells),3):
        rows+="<tr>"+"".join(cells[i:i+3])+"</tr>"
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;background:{BAND};margin:22px 0 0;">
      <tr><td colspan="3" style="padding:8px 13px;border-bottom:1px solid #b9402f;">
        <span style="font-family:{DISP};font-size:16px;font-weight:700;color:#fff;">글로벌 마켓</span>
        <span style="font-family:{LBL};font-size:9.5px;letter-spacing:.18em;color:#f3c9c2;padding-left:8px;">GLOBAL MARKETS · CNBC / AP</span></td></tr>
      {rows}</table>"""

def _snap(snap):
    tds=""
    for s in snap:
        tds+=f"""<td valign="top" style="padding:6px 10px;border-right:1px solid {RULE};">
          <div style="font-family:{LBL};font-size:9.5px;letter-spacing:.1em;color:{MUT};text-transform:uppercase;">{esc(s['name'])}</div>
          <div style="font-family:{DISP};font-size:16px;font-weight:700;color:{INK};padding:1px 0;">{esc(s['val'])}</div>
          <div style="font-family:{LBL};font-size:9.5px;color:{RED};">{esc(s['note'])}</div></td>"""
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-top:1px solid {INK};border-bottom:1px solid {INK};background:#fbf9f2;margin:6px 0 0;">
      <tr>{tds}</tr></table>"""

def render_html(data, edition="제1호", sample=True):
    sec=""
    for s in data["sections"]:
        sec+=_sechead(s["ko"],s["en"])+_twocol(s["items"])
    sample_note = " · 본 메일은 견본판입니다." if sample else ""
    edition_txt = f"{edition} · 견본판" if sample else edition
    fonthead=f"""<style>
      @font-face{{font-family:'ChosunIlboMyungjo';src:url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_one@1.0/Chosunilbo_myungjo.woff') format('woff');font-weight:400 800;font-display:swap;}}
      @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap');
    </style>"""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap" rel="stylesheet">
<title>My Agent Times</title>{fonthead}</head>
<body style="margin:0;padding:0;background:#e7e2d6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#e7e2d6;"><tr><td align="center" style="padding:18px 10px;">
<table role="presentation" width="700" cellpadding="0" cellspacing="0" style="width:700px;max-width:100%;background:{PAPER};border:1px solid #cabfa8;">
  <tr><td style="padding:24px 28px 0;">

    <div style="text-align:center;border-bottom:1px solid {INK};padding:2px 0 8px;">
      <div style="font-family:{DISP};font-size:48px;line-height:1;font-weight:800;letter-spacing:.01em;color:{INK};">My Agent Times</div>
      <div style="font-family:{LBL};font-size:10px;letter-spacing:.34em;color:{RED};text-transform:uppercase;padding-top:9px;">ECONOMY · MARKETS · TECH · INDUSTRY · MANAGEMENT</div>
    </div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-bottom:2px solid {INK};">
      <tr><td style="font-family:{DISP};font-size:12px;color:{INK};padding:5px 0;">{esc(data['date'])}</td>
          <td align="right" style="font-family:{LBL};font-size:10px;letter-spacing:.12em;color:{MUT};text-transform:uppercase;padding:5px 0;">{esc(edition_txt)}</td></tr></table>

    <div style="text-align:center;padding:13px 14px 11px;">
      <div style="font-family:{LBL};font-size:9.5px;letter-spacing:.2em;color:{RED};text-transform:uppercase;font-weight:700;">오늘의 한 줄</div>
      <div style="font-family:{DISP};font-size:15.5px;line-height:1.62;color:{INK};padding-top:5px;">{esc(data['dek'])}</div>
    </div>

    {_snap(data['snapshot'])}

    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px;">
      <tr><td>
        <div style="font-family:{LBL};font-size:10px;letter-spacing:.2em;color:{RED};text-transform:uppercase;font-weight:700;border-bottom:1px solid {RULE};padding-bottom:4px;margin-bottom:9px;">오늘의 헤드라인</div>
        {_headlines(data['headlines'])}
      </td></tr></table>

    {sec}

    {_globalband(data['global'])}

    <div style="border-top:2px solid {INK};margin-top:22px;padding:10px 0 24px;">
      <div style="font-family:{BODY};font-size:11px;line-height:1.65;color:{MUT};">
        <b style="color:{INK};font-family:{DISP};">My Agent Times</b>는 한국경제·조선비즈·매일경제·이데일리·CNBC·AP의 공개 기사에서 경제·증권·테크·산업·경영 뉴스만 선별합니다(정치 제외). 제목을 클릭하면 원문으로 이동합니다. 요약·함의는 편집 코멘트이며 투자 자문이 아닙니다.</div>
      <div style="font-family:{LBL};font-size:9.5px;color:{MUT};padding-top:6px;">매일 평일 07:30(KST) 발송 · 수신: drcap10@gmail.com{sample_note}</div>
    </div>

  </td></tr></table>
</td></tr></table></body></html>"""
