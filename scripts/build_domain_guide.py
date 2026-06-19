from __future__ import annotations

import html
import os
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ROOT = ROOT / "docs" / "domain-guide"
GUIDE_ROOT = ROOT / "docs" / "guide"
CSS_FILE = DOMAIN_ROOT / "assets" / "css" / "site.css"


DOC_CONFIG = [
    ("00_HeatGrid_Domain_Guide.md", "00", "전체 로드맵", "도메인 초심자가 어디서부터 무엇을 배우고 어떻게 Agent 설계까지 연결할지 안내합니다."),
    ("01_PreDist_논문_정리.md", "01", "PreDist 논문", "데이터셋 배경, 라벨 구조, 리드타임 개념을 가장 빠르게 이해합니다."),
    ("02_PreDist_데이터셋_가이드.md", "02", "PreDist 데이터셋", "실제 파일 구조와 멀티 기계실 데이터를 HeatGrid 관점으로 읽는 방법을 정리합니다."),
    ("03_국내_지역난방_구조와_운영_가이드.md", "03", "국내 구조와 운영", "한국의 집단에너지 구조, 민원/긴급신고, 정기점검, 협력업체 운영 흐름을 설명합니다."),
    ("04_해외_지역난방_구조와_운영_가이드.md", "04", "해외 구조와 운영", "ETS/substation, 예방정비, 체크리스트, O&M 문화 등 해외 운영 관행을 정리합니다."),
    ("05_District_Heating_Substations_Design_요약.md", "05", "기계실 설계", "열교환기, 밸브, 펌프, 센서 등 기계실 구성요소와 정비 분류를 이해합니다."),
    ("06_Gebwell_OandM_요약.md", "06", "현장 O&M", "실제 점검 항목과 예방정비 주기를 HeatGrid 작업지시 관점으로 해석합니다."),
    ("07_IEA_DHC_Connection_Handbook_요약.md", "07", "운영 기록과 PM", "기록, 정비 일정, 연결 구조가 왜 운영 계획의 기반인지 설명합니다."),
    ("08_District_Energy_PM_Checklist_요약.md", "08", "체크리스트", "정비사가 현장에서 확인하는 체크 포인트를 바로 읽을 수 있게 정리합니다."),
    ("09_ASHRAE_180_요약.md", "09", "유지관리 계획", "inspection, maintenance plan, condition indicator 같은 핵심 운영 개념을 잡습니다."),
    ("10_Anomaly_Detection_Review_요약.md", "10", "이상탐지 연구", "부분 고장, 성능 저하, 운영 리스크를 왜 anomaly 관점으로 봐야 하는지 이해합니다."),
    ("11_국내_정책_시장_사업자_가이드.md", "11", "국내 시장과 정책", "누가 구매자고 사용자며, 왜 지금 한국에서 이 서비스가 맞는지 설명합니다."),
    ("12_정비사_업무와_출동_프로세스_가이드.md", "12", "정비사와 출동", "현장 정비사가 실제로 어떤 정보를 갖고 움직이는지 이해합니다."),
    ("README.md", "readme", "폴더 안내", "Domain Guide 폴더 구조와 읽는 순서를 빠르게 확인합니다."),
    ("sources_manifest.md", "sources", "소스 인벤토리", "원문 링크, 로컬 PDF 경로, 다운로드 상태를 한 곳에서 확인합니다."),
]

DOC_MAP = {name: slug for name, slug, _, _ in DOC_CONFIG}
DOC_META = {slug: {"source": name, "label": label, "summary": summary} for name, slug, label, summary in DOC_CONFIG}

REFERENCE_DOCS = [
    ("02_HeatGrid.md", "heatgrid-overview", "HeatGrid 주제 제안서"),
    ("17_HeatGrid_디벨롭.md", "heatgrid-ops-problem", "HeatGrid 운영 문제 정의서"),
    ("18_HeatGrid_AIoT_Agent_아키텍처.md", "heatgrid-agent-architecture", "HeatGrid Agent 아키텍처"),
    ("20_HeatGrid_출시_타당성_보고서.md", "heatgrid-go-to-market", "HeatGrid 출시 타당성 보고서"),
    ("21_HeatGrid_참고문헌_및_PDF_번역정리.md", "heatgrid-reference-notes", "HeatGrid 참고문헌 및 번역 정리"),
]

REFERENCE_MAP = {name: slug for name, slug, _ in REFERENCE_DOCS}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slug_output_path(slug: str) -> Path:
    return DOMAIN_ROOT / slug / "index.html"


def to_posix(path: Path) -> str:
    return PurePosixPath(path.as_posix()).as_posix()


def relative_href(from_file: Path, to_file: Path) -> str:
    rel = os.path.relpath(to_file, from_file.parent)
    rel = rel.replace("\\", "/")
    if rel == ".":
        return "./"
    return rel


def extract_meta(lines: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("> **") and "**" in line[4:]:
            m = re.match(r'> \*\*(.+?)\*\*\s*', line)
            if m:
                key = m.group(1).strip()
                value_lines: list[str] = []
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.startswith("> **") and "**" in nxt[4:]:
                        i -= 1
                        break
                    if nxt.startswith(">"):
                        value_lines.append(nxt[1:].strip())
                    elif not nxt.strip():
                        pass
                    else:
                        break
                    i += 1
                value = " ".join(v for v in value_lines if v).strip()
                if value:
                    meta[key] = value
        i += 1
    return meta


def title_from_markdown(lines: list[str], fallback: str) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def strip_meta_from_markdown(lines: list[str]) -> list[str]:
    output: list[str] = []
    skip_meta = True
    for idx, line in enumerate(lines):
        if idx == 0 and line.startswith("# "):
            output.append(line)
            continue
        if skip_meta and (line.startswith(">") or not line.strip()):
            continue
        skip_meta = False
        output.append(line)
    return output


def convert_inline(text: str, current_slug: str) -> str:
    image_tokens: list[str] = []

    def repl_image(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        src = rewrite_href(match.group(2), current_slug)
        image_tokens.append(f'<img src="{html.escape(src, quote=True)}" alt="{alt}" class="doc-image">')
        return f"@@IMAGE_{len(image_tokens) - 1}@@"

    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl_image, text)
    text = html.escape(text, quote=False)
    text = text.replace("&lt;div", "<div").replace("&lt;/div&gt;", "</div>")
    text = re.sub(r'`([^`]+)`', r"<code>\1</code>", text)
    text = re.sub(r'\*\*([^*]+)\*\*', r"<strong>\1</strong>", text)

    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.unescape(match.group(2))
        href = rewrite_href(href, current_slug)
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, text)
    for idx, token in enumerate(image_tokens):
        text = text.replace(f"@@IMAGE_{idx}@@", token)
    return text


def rewrite_href(href: str, current_slug: str) -> str:
    href = href.strip()
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    source_name = PurePosixPath(href).name
    current_out = slug_output_path(current_slug)
    if source_name in DOC_MAP:
        target_out = slug_output_path(DOC_MAP[source_name])
        return relative_href(current_out, target_out)
    if source_name in REFERENCE_MAP:
        target_out = DOMAIN_ROOT / "references" / REFERENCE_MAP[source_name] / "index.html"
        return relative_href(current_out, target_out)
    if href.endswith(".pdf"):
        return href.replace("\\", "/")
    return href.replace("\\", "/")


def markdown_to_html(markdown: str, current_slug: str) -> str:
    lines = markdown.splitlines()
    html_parts: list[str] = []
    i = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
                code_lines = []
            else:
                class_attr = f' class="language-{code_lang}"' if code_lang else ""
                code = html.escape("\n".join(code_lines))
                html_parts.append(f"<pre><code{class_attr}>{code}</code></pre>")
                in_code = False
                code_lang = ""
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith("<") and line.endswith(">"):
            html_parts.append(line)
            i += 1
            continue
        if re.fullmatch(r"-{3,}", line.strip()):
            html_parts.append("<hr>")
            i += 1
            continue
        if line.startswith("# "):
            html_parts.append(f"<h1>{convert_inline(line[2:].strip(), current_slug)}</h1>")
            i += 1
            continue
        if line.startswith("## "):
            html_parts.append(f"<h2>{convert_inline(line[3:].strip(), current_slug)}</h2>")
            i += 1
            continue
        if line.startswith("### "):
            html_parts.append(f"<h3>{convert_inline(line[4:].strip(), current_slug)}</h3>")
            i += 1
            continue
        if line.startswith("#### "):
            html_parts.append(f"<h4>{convert_inline(line[5:].strip(), current_slug)}</h4>")
            i += 1
            continue
        if line.startswith(">"):
            block: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].strip())
                i += 1
            content = "<br>".join(convert_inline(b, current_slug) for b in block if b)
            html_parts.append(f'<blockquote>{content}</blockquote>')
            continue
        if "|" in line and i + 1 < len(lines) and re.match(r"^\|?[\s:-]+\|", lines[i + 1].strip()):
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            html_parts.append(render_table(table_lines, current_slug))
            continue
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]).strip())
                i += 1
            html_parts.append("<ol>" + "".join(f"<li>{convert_inline(item, current_slug)}</li>" for item in items) + "</ol>")
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip())
                i += 1
            html_parts.append("<ul>" + "".join(f"<li>{convert_inline(item, current_slug)}</li>" for item in items) + "</ul>")
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not starts_new_block(lines[i], i, lines):
            para.append(lines[i].strip())
            i += 1
        html_parts.append(f"<p>{convert_inline(' '.join(para), current_slug)}</p>")
    return "\n".join(html_parts)


def starts_new_block(line: str, idx: int, lines: list[str]) -> bool:
    if line.startswith(("# ", "## ", "### ", "#### ", ">", "- ", "```", "<")):
        return True
    if re.match(r"^\d+\.\s+", line):
        return True
    if re.fullmatch(r"-{3,}", line.strip()):
        return True
    if "|" in line and idx + 1 < len(lines) and re.match(r"^\|?[\s:-]+\|", lines[idx + 1].strip()):
        return True
    return False


def render_table(lines: list[str], current_slug: str) -> str:
    rows = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in lines]
    headers = rows[0]
    bodies = rows[2:]
    thead = "<thead><tr>" + "".join(f"<th>{convert_inline(cell, current_slug)}</th>" for cell in headers) + "</tr></thead>"
    tbody = "<tbody>"
    for row in bodies:
        tbody += "<tr>" + "".join(f"<td>{convert_inline(cell, current_slug)}</td>" for cell in row) + "</tr>"
    tbody += "</tbody>"
    return f'<div class="table-wrap"><table>{thead}{tbody}</table></div>'


def render_meta_box(meta: dict[str, str], slug: str) -> str:
    items = []
    preferred = ["문서 역할", "대상 독자", "읽는 시간", "난이도", "선수지식", "원문 링크", "로컬 PDF 경로"]
    for key in preferred:
        if key in meta:
            items.append((key, meta[key]))
    if not items:
        return ""
    rows = "".join(
        f"<div class='meta-row'><div class='meta-key'>{html.escape(k)}</div><div class='meta-value'>{convert_inline(v, slug)}</div></div>"
        for k, v in items
    )
    return f"<section class='meta-box'>{rows}</section>"


def render_prev_next(slug: str) -> str:
    order = [cfg[1] for cfg in DOC_CONFIG]
    if slug not in order:
        return ""
    idx = order.index(slug)
    parts = []
    if idx > 0:
        prev_slug = order[idx - 1]
        prev_label = DOC_META[prev_slug]["label"]
        href = relative_href(slug_output_path(slug), slug_output_path(prev_slug))
        parts.append(f"<a class='nav-link prev' href='{href}'>이전: {html.escape(prev_label)}</a>")
    if idx < len(order) - 1:
        next_slug = order[idx + 1]
        next_label = DOC_META[next_slug]["label"]
        href = relative_href(slug_output_path(slug), slug_output_path(next_slug))
        parts.append(f"<a class='nav-link next' href='{href}'>다음: {html.escape(next_label)}</a>")
    if not parts:
        return ""
    return "<nav class='doc-nav'>" + "".join(parts) + "</nav>"


def page_template(title: str, body: str, slug: str, summary: str, meta_box: str, breadcrumb: str) -> str:
    css_href = relative_href(slug_output_path(slug), CSS_FILE)
    home_href = relative_href(slug_output_path(slug), DOMAIN_ROOT / "index.html")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <div class="page-shell">
    <aside class="page-side">
      <a class="side-home" href="{home_href}">HeatGrid Domain Guide</a>
      <p class="side-summary">{html.escape(summary)}</p>
      <div class="side-links">
        <a href="{home_href}">메인 허브</a>
        <a href="{relative_href(slug_output_path(slug), slug_output_path('00'))}">00 메인 가이드</a>
        <a href="{relative_href(slug_output_path(slug), slug_output_path('03'))}">2-1 국내 구조와 운영</a>
        <a href="{relative_href(slug_output_path(slug), slug_output_path('04'))}">2-2 해외 구조와 운영</a>
      </div>
    </aside>
    <main class="page-main">
      <div class="breadcrumb">{breadcrumb}</div>
      <article class="doc-card">
        {meta_box}
        {body}
        {render_prev_next(slug)}
      </article>
    </main>
  </div>
</body>
</html>
"""


def build_doc(md_name: str, slug: str, label: str, summary: str) -> None:
    source = DOMAIN_ROOT / md_name
    lines = read_text(source).splitlines()
    meta = extract_meta(lines)
    title = title_from_markdown(lines, label)
    content_lines = strip_meta_from_markdown(lines)
    content_html = markdown_to_html("\n".join(content_lines), slug)
    meta_box = render_meta_box(meta, slug)
    breadcrumb = f"<a href='{relative_href(slug_output_path(slug), DOMAIN_ROOT / 'index.html')}'>홈</a> / <span>{html.escape(label)}</span>"
    out = slug_output_path(slug)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_template(title, content_html, slug, summary, meta_box, breadcrumb), encoding="utf-8")


def build_reference_doc(source_name: str, slug: str, label: str) -> None:
    source = GUIDE_ROOT / source_name
    lines = read_text(source).splitlines()
    title = title_from_markdown(lines, label)
    content_html = markdown_to_html("\n".join(lines), slug)
    out = DOMAIN_ROOT / "references" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    summary = f"{label} 참고 문서"
    css_href = relative_href(out, CSS_FILE)
    home_href = relative_href(out, DOMAIN_ROOT / "index.html")
    html_text = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <div class="page-shell">
    <aside class="page-side">
      <a class="side-home" href="{home_href}">HeatGrid Domain Guide</a>
      <p class="side-summary">{html.escape(summary)}</p>
    </aside>
    <main class="page-main">
      <div class="breadcrumb"><a href="{home_href}">홈</a> / <span>관련 기획 문서</span></div>
      <article class="doc-card">{content_html}</article>
    </main>
  </div>
</body>
</html>
"""
    out.write_text(html_text, encoding="utf-8")


def build_landing() -> None:
    cards = []
    for slug in ["00", "03", "04", "11", "12"]:
        href = relative_href(DOMAIN_ROOT / "index.html", slug_output_path(slug))
        cards.append(
            f"""
            <article class="summary-card">
              <div class="summary-no">{slug}</div>
              <h3>{html.escape(DOC_META[slug]["label"])}</h3>
              <p>{html.escape(DOC_META[slug]["summary"])}</p>
              <a class="text-link" href="{href}">바로 읽기</a>
            </article>
            """
        )

    catalog = []
    for _, slug, label, summary in DOC_CONFIG:
        href = relative_href(DOMAIN_ROOT / "index.html", slug_output_path(slug))
        catalog.append(f"<li><a href='{href}'>{html.escape(label)}</a><span>{html.escape(summary)}</span></li>")

    pdf_items = []
    for pdf in sorted((DOMAIN_ROOT / "assets" / "pdf").glob("*.pdf")):
        href = relative_href(DOMAIN_ROOT / "index.html", pdf)
        pdf_items.append(f"<li><a href='{href}'>{html.escape(pdf.name)}</a></li>")

    ref_items = []
    for _, slug, label in REFERENCE_DOCS:
        href = relative_href(DOMAIN_ROOT / "index.html", DOMAIN_ROOT / "references" / slug / "index.html")
        ref_items.append(f"<li><a href='{href}'>{html.escape(label)}</a></li>")

    html_text = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HeatGrid Domain Guide</title>
  <link rel="stylesheet" href="{relative_href(DOMAIN_ROOT / 'index.html', CSS_FILE)}">
</head>
<body>
  <div class="landing-shell">
    <section class="hero hero-strong">
      <p class="eyebrow">HeatGrid Domain Guide</p>
      <h1>지역난방을 몰라도<br>HeatGrid Agent 설계까지 갈 수 있는 학습 사이트</h1>
      <p class="hero-lead">
        이 사이트는 지역난방, 기계실, 정비, 운영, PreDist를 처음 보는 사람도
        <strong>문제 이해 → 데이터 해석 → 운영 판단 → Agent 설계</strong>까지 연결하도록 만든 도메인 가이드입니다.
      </p>
      <div class="cta-row">
        <a class="btn primary" href="{relative_href(DOMAIN_ROOT / 'index.html', slug_output_path('00'))}">처음 시작하기</a>
        <a class="btn secondary" href="{relative_href(DOMAIN_ROOT / 'index.html', slug_output_path('03'))}">국내 구조와 운영 먼저 보기</a>
        <a class="btn secondary" href="{relative_href(DOMAIN_ROOT / 'index.html', slug_output_path('04'))}">해외 구조와 운영 먼저 보기</a>
      </div>
    </section>

    <section class="answer-grid">
      <article class="answer-card">
        <h2>문제</h2>
        <p>지역난방 기계실은 구조도 낯설고, 센서와 부품, 민원과 출동, 예방정비와 재계획이 한 번에 얽혀 있어 처음 보면 무엇부터 공부해야 할지 감이 잘 오지 않습니다.</p>
      </article>
      <article class="answer-card">
        <h2>해결</h2>
        <p>이 사이트는 PreDist, 국내 운영 자료, 해외 O&amp;M 문서, 정비 체크리스트를 한 흐름으로 엮어 초심자도 단계적으로 이해할 수 있게 정리합니다.</p>
      </article>
      <article class="answer-card">
        <h2>결과</h2>
        <p>다 읽고 나면 주요 부품, 센서 변수, 대표 고장, 작업지시, 우선순위화, 재계획 구조를 설명하고 HeatGrid Agent 설계에 연결할 수 있습니다.</p>
      </article>
    </section>

    <section class="route-box">
      <div class="route-copy">
        <h2>학습순서</h2>
        <p>아래 순서로 보면 도메인이 없는 사람도 자연스럽게 올라올 수 있습니다.</p>
      </div>
      <ol class="route-list">
        <li><strong>00</strong> 전체 로드맵과 공부 순서 잡기</li>
        <li><strong>01~02</strong> PreDist와 데이터 구조 이해</li>
        <li><strong>03~04</strong> 국내/해외 지역난방 구조와 운영 비교</li>
        <li><strong>05~10</strong> 설계, O&amp;M, 체크리스트, 이상탐지 연구 읽기</li>
        <li><strong>11~12</strong> 시장/정책과 정비사 출동 프로세스 연결</li>
      </ol>
    </section>

    <section class="section-block">
      <div class="section-head">
        <h2>핵심 진입점</h2>
        <p>처음 보는 사람이 가장 먼저 눌러야 하는 문서들입니다.</p>
      </div>
      <div class="summary-grid">
        {''.join(cards)}
      </div>
    </section>

    <section class="section-block">
      <div class="section-head">
        <h2>학습 트랙</h2>
        <p>목표에 따라 바로 들어갈 수 있는 학습 루트입니다.</p>
      </div>
      <div class="track-grid">
        <article class="track-card">
          <h3>초심자 루트</h3>
          <p>00 → 01 → 02 → 03 → 04</p>
        </article>
        <article class="track-card">
          <h3>데이터 루트</h3>
          <p>01 → 02 → 10 → 05 → 06</p>
        </article>
        <article class="track-card">
          <h3>Agent 설계 루트</h3>
          <p>00 → 03 → 04 → 08 → 09 → 11 → 12</p>
        </article>
      </div>
    </section>

    <section class="section-block section-muted">
      <div class="section-head">
        <h2>전체 문서</h2>
      </div>
      <ul class="catalog-list">
        {''.join(catalog)}
      </ul>
    </section>

    <section class="lower-grid">
      <article class="panel">
        <h3>PDF 원문</h3>
        <ul class="simple-list">
          {''.join(pdf_items)}
        </ul>
      </article>
      <article class="panel">
        <h3>관련 기획 문서</h3>
        <ul class="simple-list">
          {''.join(ref_items)}
        </ul>
      </article>
      <article class="panel">
        <h3>자료 인벤토리</h3>
        <p>원문 링크와 로컬 저장 상태는 한 곳에서 확인할 수 있습니다.</p>
        <a class="text-link" href="{relative_href(DOMAIN_ROOT / 'index.html', slug_output_path('sources'))}">sources 페이지 보기</a>
      </article>
    </section>
  </div>
</body>
</html>
"""
    (DOMAIN_ROOT / "index.html").write_text(html_text, encoding="utf-8")


def build_docs_redirect() -> None:
    docs_index = ROOT / "docs" / "index.html"
    docs_index.write_text(
        """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="0; url=./domain-guide/index.html"><title>Redirect</title></head><body><p><a href="./domain-guide/index.html">HeatGrid Domain Guide로 이동</a></p></body></html>""",
        encoding="utf-8",
    )
    (ROOT / "docs" / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    for name, slug, label, summary in DOC_CONFIG:
        build_doc(name, slug, label, summary)
    for name, slug, label in REFERENCE_DOCS:
        build_reference_doc(name, slug, label)
    build_landing()
    build_docs_redirect()


if __name__ == "__main__":
    main()
