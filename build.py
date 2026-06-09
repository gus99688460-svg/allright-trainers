#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""올라잇짐 트레이너 포트폴리오 빌더.
data/<slug>.json + assets/style.css → <slug>/index.html 생성.
"""
import json, os, html, glob

BASE = os.path.dirname(os.path.abspath(__file__))

def esc(s):
    return html.escape(str(s), quote=True)

def section(id_, icon, title, inner, sub=None):
    subh = f'<p class="sec-sub">{esc(sub)}</p>' if sub else ""
    return f'''<section id="{id_}">
  <h2 class="sec-h"><span class="ic">{icon}</span>{esc(title)}</h2>{subh}
  {inner}
</section>'''

def paras(items):
    return "\n  ".join(f'<p class="body">{esc(t)}</p>' for t in items)

def build(d):
    slug = d["slug"]
    # HERO spec
    spec = ""
    if d.get("main"):
        spec += f'<div><b>MAIN</b>{esc(d["main"])}</div>'
    if d.get("sub"):
        spec += f'<div><b>SUB</b>{esc(d["sub"])}</div>'
    catch = "<br>".join(esc(c) for c in d["catch"])

    hero = f'''<header id="hero">
  <p class="hero-tag">ALLRIGHTGYM TRAINER</p>
  <img class="photo" src="images/profile.jpg" alt="{esc(d["name_ko"])} 트레이너" />
  <p class="hero-catch">{catch}</p>
  <h1>{esc(d["name_ko"])}</h1>
  <p class="name-en">{esc(d["name_en"])}</p>
  <div class="hero-spec">{spec}</div>
</header>'''

    nav = '''<nav>
  <a href="#mind">마인드</a>
  <a href="#story">스토리</a>
  <a href="#curriculum">PT 진행</a>
  <a href="#career">경력·자격</a>
  <a href="#before-after">비포애프터</a>
  <a href="#contact">상담</a>
</nav>'''

    secs = []

    # MIND
    mind_inner = ""
    if d.get("mind_quote"):
        mind_inner += f'<p class="quote">{esc(d["mind_quote"])}</p>\n  '
    mind_inner += paras(d["mind"])
    secs.append(section("mind", "❤️‍🔥", "Mind", mind_inner))

    # STORY
    story_inner = '<div class="card">\n    <p class="quote">🧐 트레이너가 된 계기</p>\n    ' \
        + paras(d["story_motive"]) + '\n  </div>\n  '
    story_inner += '<div class="card">\n    <p class="quote">😆 트레이너로서 느끼는 보람</p>\n    ' \
        + paras(d["story_reward"]) + '\n  </div>'
    secs.append(section("story", "💬", "Story", story_inner))

    # HASHTAGS (이런 회원님)
    tags = '<div class="tags">' + "".join(f'<span>{esc(t)}</span>' for t in d["hashtags"]) + '</div>'
    secs.append(section("need", "🫵", f'이런 분께 {d["nick"]}이 필요합니다', tags))

    # CURRICULUM
    steps = '<div class="steps">' + "".join(
        f'<div class="step"><div class="no">{i+1}</div><div class="tx">{esc(s)}</div></div>'
        for i, s in enumerate(d["curriculum"])) + '</div>'
    secs.append(section("curriculum", "📆", "PT 커리큘럼", steps))

    # STYLE
    style_title = f'<p class="sec-sub" style="margin-top:-6px">{esc(d.get("style_title","진행 스타일"))}</p>' if d.get("style") else ""
    style_inner = '<div class="card">' + style_title + '<ul class="dotlist">' + \
        "".join(f'<li>{esc(s)}</li>' for s in d["style"]) + '</ul></div>'
    secs.append(section("style", "💁", "Style", style_inner))

    # QNA
    qna = '<div class="qna">' + "".join(
        f'<div class="qa"><div class="q">{esc(q)}</div><div class="a">{esc(a)}</div></div>'
        for q, a in d["qna"]) + '</div>'
    secs.append(section("qna", "❔", "자주 묻는 질문", qna))

    # CAREER (Experience + Cert + Competition)
    grp = ""
    if d.get("experience"):
        items = "".join(
            f'<li class="now">{esc(x)}</li>' if x.strip().startswith("현)")
            else f'<li>{esc(x)}</li>' for x in d["experience"])
        grp += f'<div class="grp"><h4>Experience</h4><ul class="tl">{items}</ul></div>'
    if d.get("cert"):
        grp += '<div class="grp"><h4>자격 · 교육</h4><ul>' + \
            "".join(f'<li>{esc(c)}</li>' for c in d["cert"]) + '</ul></div>'
    if d.get("competition"):
        comp_html = '<div class="grp"><h4>대회 이력</h4>'
        if isinstance(d["competition"], dict):
            for yr, lst in d["competition"].items():
                comp_html += f'<div class="yr">{esc(yr)}</div><ul>' + \
                    "".join(f'<li>{esc(c)}</li>' for c in lst) + '</ul>'
        else:
            comp_html += '<ul>' + "".join(f'<li>{esc(c)}</li>' for c in d["competition"]) + '</ul>'
        comp_html += '</div>'
        grp += comp_html
    secs.append(section("career", "🏆", "Career", f'<div class="card">{grp}</div>'))

    # BEFORE / AFTER
    ba = '<div class="ba">'
    for case in d["before_after"]:
        imgs = case["img"]
        n = "n4" if len(imgs) >= 3 else ("n2" if len(imgs) == 2 else "n1")
        imghtml = "".join(f'<img src="images/{esc(i)}" alt="비포애프터" loading="lazy" />' for i in imgs)
        cap = "\n".join(esc(c) for c in case["cap"])
        ba += f'<div class="ba-case"><div class="ba-imgs {n}">{imghtml}</div><div class="ba-cap">{cap}</div></div>'
    ba += '</div>'
    secs.append(section("before-after", "🔥", "비포 / 애프터", ba))

    # RECOMMEND
    reco = f'<p class="reco-lead">{esc(d["reco_title"])}</p><div class="card"><ul class="dotlist">' + \
        "".join(f'<li>{esc(r)}</li>' for r in d["reco"]) + '</ul></div>'
    secs.append(section("reco", "🫵", f'올라잇짐에서 {d["nick"]}을 추천합니다', reco))

    # PROMISE
    promise = f'<div class="promise">{esc(d["promise"])}</div>'
    secs.append(section("promise", "🫱‍🫲", f'{d["nick"]}의 약속', promise))

    # CONTACT
    insta = d["insta"]
    tel = d["phone"].replace(" ", "").replace("+82", "0").replace("-", "")
    contact = f'''<div class="cta-wrap">
    <a class="cta insta" href="https://instagram.com/{esc(insta)}" target="_blank" rel="noopener">📷 인스타그램 DM 상담</a>
    <a class="cta tel" href="tel:{esc(tel)}">📞 전화 상담 {esc(d["phone"])}</a>
  </div>
  <p class="contact-info"><b>@{esc(insta)}</b><br>{esc(d["email"])}</p>'''
    secs.append(section("contact", "📩", "상담 문의", contact))

    closing = "\n".join(esc(c) for c in d["closing"])
    closing_html = f'''<div class="closing">
  <p class="big">{closing}</p>
  <p class="fire">감사합니다 🔥</p>
</div>'''

    footer = f'''<footer>
  <p class="tn">TRAINER · {esc(d["name_en"]).upper()}</p>
  <p>© ALLRIGHTGYM. All rights reserved.</p>
</footer>'''

    sticky = f'''<div class="sticky">
  <a class="insta" href="https://instagram.com/{esc(insta)}" target="_blank" rel="noopener">📷 인스타 DM</a>
  <a class="tel" href="tel:{esc(tel)}">📞 전화 상담</a>
</div>'''

    page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(d["name_ko"])} 트레이너 · 올라잇짐</title>
<meta name="description" content="{esc(d["name_ko"])} 트레이너 ({esc(d.get("main",""))}) · 올라잇짐" />
<meta property="og:title" content="{esc(d["name_ko"])} 트레이너 · 올라잇짐" />
<meta property="og:description" content="{esc(' / '.join(d['catch']))}" />
<meta property="og:image" content="images/profile.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="stylesheet" href="../assets/style.css?v=1" />
</head>
<body>
{hero}
{nav}
{chr(10).join(secs)}
{closing_html}
{footer}
{sticky}
</body>
</html>'''
    out = os.path.join(BASE, slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return out


def build_hub(items, order):
    by = {d["slug"]: d for d in items}
    cards = ""
    for slug in order:
        d = by.get(slug)
        if not d:
            continue
        catch = esc(" ".join(d["catch"]))
        cards += f'''<a class="tcard" href="{slug}/">
    <img src="{slug}/images/profile.jpg" alt="{esc(d["name_ko"])}" loading="lazy" />
    <div class="tcard-b">
      <h3>{esc(d["name_ko"])} <span>{esc(d["nick"])}</span></h3>
      <p class="tcatch">{catch}</p>
      <p class="tmain">{esc(d.get("main",""))}</p>
    </div>
    <span class="tgo">자세히 보기 →</span>
  </a>'''
    page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>올라잇짐 트레이너</title>
<meta name="description" content="올라잇짐 트레이너 소개 — 검증된 전문 트레이너와 함께하세요." />
<meta property="og:title" content="올라잇짐 트레이너" />
<link rel="stylesheet" href="assets/style.css?v=1" />
<style>
  .hub-hero{{text-align:center;padding:70px 24px 40px;position:relative;
    background:radial-gradient(circle at 50% 0%,rgba(212,175,55,.16),transparent 60%),linear-gradient(180deg,#161616,#0a0a0a);
    border-bottom:1px solid var(--line)}}
  .hub-hero::before{{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}}
  .hub-hero .tag{{color:var(--gold);letter-spacing:3px;font-weight:700;font-size:13px;text-transform:uppercase}}
  .hub-hero h1{{font-size:30px;font-weight:800;margin:14px 0 8px;letter-spacing:-.5px}}
  .hub-hero p{{color:var(--muted);font-size:15px}}
  .tgrid{{max-width:680px;margin:0 auto;padding:34px 18px 10px;display:flex;flex-direction:column;gap:16px}}
  .tcard{{display:flex;align-items:center;gap:16px;background:var(--card);border:1px solid var(--line);
    border-radius:18px;padding:16px;transition:border-color .2s}}
  .tcard:active{{border-color:var(--gold)}}
  .tcard img{{width:84px;height:84px;border-radius:14px;object-fit:cover;border:2px solid var(--gold);flex:0 0 auto}}
  .tcard-b{{flex:1;min-width:0}}
  .tcard-b h3{{font-size:18px;font-weight:800}}
  .tcard-b h3 span{{color:var(--gold);font-size:13px;font-weight:600;margin-left:4px}}
  .tcatch{{color:#ddd;font-size:13.5px;margin:3px 0;line-height:1.4;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
  .tmain{{color:var(--gold);font-size:12.5px;font-weight:600}}
  .tgo{{flex:0 0 auto;color:var(--muted2);font-size:12px;font-weight:700;align-self:flex-end}}
</style>
</head>
<body style="padding-bottom:40px">
<header class="hub-hero">
  <p class="tag">ALLRIGHTGYM</p>
  <h1>올라잇짐 트레이너</h1>
  <p>나에게 맞는 트레이너를 만나보세요</p>
</header>
<div class="tgrid">
  {cards}
</div>
<footer>
  <p class="tn">ALLRIGHTGYM</p>
  <p>© ALLRIGHTGYM. All rights reserved.</p>
</footer>
</body>
</html>'''
    out = os.path.join(BASE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return out


if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(BASE, "data", "*.json")))
    items = []
    for fp in files:
        d = json.load(open(fp, encoding="utf-8"))
        items.append(d)
        out = build(d)
        print("built:", out)
    # 허브 (표시 순서: 최상빈·조민서·김선준·손서빈·한우진)
    hub = build_hub(items, ["choi", "cho", "kim", "son", "han"])
    print("built:", hub)
