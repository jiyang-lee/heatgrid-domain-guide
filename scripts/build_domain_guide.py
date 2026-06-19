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
    ("00_HeatGrid_Domain_Guide.md", "00", "이 문서 하나로 충분합니다", "다른 페이지로 안 가도 이 문서 하나만 읽으면 지역난방 기계실과 HeatGrid Agent를 이해할 수 있습니다."),
    ("01_PreDist_논문_정리.md", "01", "PreDist 논문", "PreDist의 문제의식, 라벨 구조, lead time 개념을 초심자 눈높이로 풀어냅니다."),
    ("02_PreDist_데이터셋_가이드.md", "02", "PreDist 데이터셋", "PreDist 파일 구조와 컬럼을 센서, 설비, 운영 이벤트 관점으로 읽는 법을 정리합니다."),
    ("03_국내_지역난방_구조와_운영_가이드.md", "03", "국내 구조와 운영", "한국의 집단에너지 구조, 민원, 긴급신고, 정기점검, 협력업체 흐름을 설명합니다."),
    ("04_해외_지역난방_구조와_운영_가이드.md", "04", "해외 구조와 운영", "ETS, substation, 예방정비, 체크리스트 문화가 HeatGrid에 주는 시사점을 정리합니다."),
    ("05_District_Heating_Substations_Design_요약.md", "05", "기계실 설계", "열교환기, 펌프, 밸브, 센서가 하나의 시스템으로 어떻게 연결되는지 설명합니다."),
    ("06_Gebwell_OandM_요약.md", "06", "현장 O&M", "운전과 점검이 어떤 순서로 이어지는지 작업지시 관점으로 해석합니다."),
    ("07_IEA_DHC_Connection_Handbook_요약.md", "07", "운영 기록과 PM", "연결 구조, 점검 이력, 로그북이 왜 재계획의 기반인지 보여줍니다."),
    ("08_District_Energy_PM_Checklist_요약.md", "08", "예방정비 체크리스트", "체크리스트를 HeatGrid 작업지시서 구조로 바꾸는 관점을 설명합니다."),
    ("09_ASHRAE_180_요약.md", "09", "유지관리 계획", "inspection, maintenance plan, condition indicator를 운영 문서 관점으로 풉니다."),
    ("10_Anomaly_Detection_Review_요약.md", "10", "이상탐지 해석", "이상탐지를 현장 맥락, 영향도, 원인 후보와 함께 해석해야 하는 이유를 다룹니다."),
    ("11_국내_정책_시장_사업자_가이드.md", "11", "국내 시장과 정책", "누가 구매자이고 누가 사용자이며 어떤 가치 제안이 통하는지 설명합니다."),
    ("12_정비사_업무와_출동_프로세스_가이드.md", "12", "정비사와 출동", "정비사가 실제로 어떤 정보와 순서로 움직이는지 작업지시 관점에서 설명합니다."),
    ("README.md", "readme", "폴더 안내", "Domain Guide 폴더 구조와 문서 규칙, 배포 구성을 빠르게 확인합니다."),
    ("sources_manifest.md", "sources", "소스 인벤토리", "원문 링크, 로컬 PDF 경로, 다운로드 상태를 한눈에 확인합니다."),
]

DOC_MAP = {name: slug for name, slug, _, _ in DOC_CONFIG}
DOC_META = {slug: {"source": name, "label": label, "summary": summary} for name, slug, label, summary in DOC_CONFIG}

REFERENCE_DOCS = [
    ("02_HeatGrid.md", "heatgrid-overview", "HeatGrid 주제 제안서"),
    ("17_HeatGrid_디벨롭.md", "heatgrid-ops-problem", "HeatGrid 운영 문제 정의"),
    ("18_HeatGrid_AIoT_Agent_아키텍처.md", "heatgrid-agent-architecture", "HeatGrid Agent 아키텍처"),
    ("20_HeatGrid_출시_타당성_보고서.md", "heatgrid-go-to-market", "HeatGrid 출시 타당성 보고서"),
    ("21_HeatGrid_참고문헌_및_PDF_번역정리.md", "heatgrid-reference-notes", "HeatGrid 참고문헌 및 번역 정리"),
]

REFERENCE_MAP = {name: slug for name, slug, _ in REFERENCE_DOCS}

# 사이드바 챕터 메뉴를 묶는 클러스터(학습 묶음) 정의
CHAPTER_CLUSTERS = [
    ("시작", ["00"]),
    ("데이터 이해", ["01", "02"]),
    ("국내·해외 구조", ["03", "04"]),
    ("설비·점검 심화", ["05", "06", "07", "08", "09", "10"]),
    ("시장·정비 서비스", ["11", "12"]),
]
CHAPTER_SLUGS = [slug for _, slugs in CHAPTER_CLUSTERS for slug in slugs]
CLUSTER_OF = {slug: name for name, slugs in CHAPTER_CLUSTERS for slug in slugs}

# 공통 <head> 조각: Pretendard 웹폰트(한국어 가독성) + 시스템 폰트 폴백은 CSS에서 처리
FONT_LINKS = (
    '<link rel="preconnect" href="https://cdn.jsdelivr.net">\n'
    '  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">'
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slug_output_path(slug: str) -> Path:
    return DOMAIN_ROOT / slug / "index.html"


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
            match = re.match(r'> \*\*(.+?)\*\*\s*', line)
            if match:
                key = match.group(1).strip()
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

    def repl_link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.unescape(match.group(2))
        href = rewrite_href(href, current_slug)
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl_link, text)
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
    target_path = (DOMAIN_ROOT / href).resolve()
    try:
        target_path.relative_to(DOMAIN_ROOT.resolve())
        return relative_href(current_out, target_path)
    except ValueError:
        return href.replace("\\", "/")


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
            html_parts.append(f"<blockquote>{content}</blockquote>")
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


def render_meta_box(meta: dict[str, str], slug: str) -> str:
    preferred = ["문서 역할", "대상 독자", "읽는 시간", "난이도", "선수지식", "원문 링크", "로컬 자산 경로", "로컬 PDF 경로"]
    items = [(key, meta[key]) for key in preferred if key in meta]
    if not items:
        return ""
    rows = "".join(
        f"<div class='meta-row'><div class='meta-key'>{html.escape(key)}</div><div class='meta-value'>{convert_inline(value, slug)}</div></div>"
        for key, value in items
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
        href = relative_href(slug_output_path(slug), slug_output_path(prev_slug))
        parts.append(f"<a class='nav-link prev' href='{href}'>이전: {html.escape(DOC_META[prev_slug]['label'])}</a>")
    if idx < len(order) - 1:
        next_slug = order[idx + 1]
        href = relative_href(slug_output_path(slug), slug_output_path(next_slug))
        parts.append(f"<a class='nav-link next' href='{href}'>다음: {html.escape(DOC_META[next_slug]['label'])}</a>")
    return "<nav class='doc-nav'>" + "".join(parts) + "</nav>" if parts else ""


def build_chapter_nav(current_slug: str) -> str:
    """사이드바에 00~12 전체 챕터를 클러스터로 묶어 보여주고 현재 위치를 강조한다."""
    current_out = slug_output_path(current_slug)
    if current_slug in CHAPTER_SLUGS:
        position = f"전체 {len(CHAPTER_SLUGS)}개 챕터 · 지금 {CHAPTER_SLUGS.index(current_slug) + 1}번째"
    else:
        position = f"전체 {len(CHAPTER_SLUGS)}개 챕터"
    blocks = [f"<p class='nav-progress'>{position}</p>"]
    for cluster_name, slugs in CHAPTER_CLUSTERS:
        items = []
        for slug in slugs:
            meta = DOC_META[slug]
            href = relative_href(current_out, slug_output_path(slug))
            active = " active" if slug == current_slug else ""
            items.append(
                f"<a class='nav-item{active}' href='{href}'>"
                f"<span class='nav-num'>{html.escape(slug)}</span>"
                f"<span class='nav-label'>{html.escape(meta['label'])}</span></a>"
            )
        blocks.append(
            f"<div class='nav-cluster'><p class='nav-cluster-title'>{html.escape(cluster_name)}</p>"
            + "".join(items)
            + "</div>"
        )
    return "<nav class='chapter-nav'>" + "".join(blocks) + "</nav>"


def add_toc(body_html: str) -> tuple[str, str]:
    """본문의 h2/h3에 id를 붙이고, 같은 순서로 페이지 내 목차(TOC)를 만든다."""
    counter = {"n": 0}
    entries: list[tuple[int, str, str]] = []

    def repl(match: re.Match[str]) -> str:
        level = int(match.group(1))
        inner = match.group(2)
        counter["n"] += 1
        anchor = f"sec-{counter['n']}"
        text = re.sub(r"<[^>]+>", "", inner).strip()
        entries.append((level, anchor, text))
        return f"<h{level} id=\"{anchor}\">{inner}</h{level}>"

    new_body = re.sub(r"<h([23])>(.*?)</h\1>", repl, body_html, flags=re.DOTALL)
    if not entries:
        return body_html, ""
    links = "".join(
        f"<a class='toc-h{level}' href='#{anchor}'>{html.escape(text)}</a>"
        for level, anchor, text in entries
    )
    toc = (
        "<aside class='page-toc'><div class='toc-inner'>"
        "<p class='toc-title'>이 페이지 목차</p>" + links + "</div></aside>"
    )
    return new_body, toc


def page_template(
    title: str,
    body: str,
    slug: str,
    summary: str,
    meta_box: str,
    breadcrumb: str,
    eyebrow: str = "",
    chips: str = "",
    toc: str = "",
) -> str:
    css_href = relative_href(slug_output_path(slug), CSS_FILE)
    home_href = relative_href(slug_output_path(slug), DOMAIN_ROOT / "index.html")
    eyebrow_html = f"<p class='chapter-eyebrow'>{eyebrow}</p>" if eyebrow else ""
    chips_html = f"<div class='meta-chips'>{chips}</div>" if chips else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  {FONT_LINKS}
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <div class="progress-bar"><span id="progress-fill"></span></div>
  <div class="page-shell">
    <aside class="page-side">
      <a class="side-home" href="{home_href}">🔥 HeatGrid<span>Domain Guide</span></a>
      {build_chapter_nav(slug)}
    </aside>
    <main class="page-main">
      <div class="breadcrumb">{breadcrumb}</div>
      <article class="doc-card">
        {eyebrow_html}
        {chips_html}
        {meta_box}
        {body}
        {render_prev_next(slug)}
      </article>
    </main>
    {toc}
  </div>
  <script>
    (function(){{
      var fill = document.getElementById('progress-fill');
      function onScroll(){{
        var h = document.documentElement;
        var max = h.scrollHeight - h.clientHeight;
        var pct = max > 0 ? (h.scrollTop || document.body.scrollTop) / max * 100 : 0;
        fill.style.width = pct + '%';
      }}
      document.addEventListener('scroll', onScroll, {{passive:true}});
      onScroll();
    }})();
  </script>
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
    content_html, toc = add_toc(content_html)
    meta_box = render_meta_box(meta, slug)

    home_href = relative_href(slug_output_path(slug), DOMAIN_ROOT / "index.html")
    cluster = CLUSTER_OF.get(slug)
    if slug in CHAPTER_SLUGS:
        eyebrow = f"CHAPTER {html.escape(slug)} · {html.escape(cluster)}"
        breadcrumb = (
            f"<a href='{home_href}'>홈</a> / <span>{html.escape(cluster)}</span> / "
            f"<span>{html.escape(label)}</span>"
        )
    else:
        eyebrow = ""
        breadcrumb = f"<a href='{home_href}'>홈</a> / <span>{html.escape(label)}</span>"

    chip_parts = []
    for key in ("읽는 시간", "난이도"):
        if key in meta:
            chip_parts.append(f"<span class='chip'>{html.escape(key)} · {convert_inline(meta[key], slug)}</span>")
    chips = "".join(chip_parts)

    out = slug_output_path(slug)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        page_template(title, content_html, slug, summary, meta_box, breadcrumb, eyebrow, chips, toc),
        encoding="utf-8",
    )


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
  {FONT_LINKS}
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <div class="page-shell page-shell-narrow">
    <aside class="page-side">
      <a class="side-home" href="{home_href}">🔥 HeatGrid<span>Domain Guide</span></a>
      <p class="side-summary">{html.escape(summary)}</p>
      <a class="back-home" href="{home_href}">← 메인으로 돌아가기</a>
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
    index_path = DOMAIN_ROOT / "index.html"

    # 클러스터 단위로 묶은 단일 챕터 로드맵 (중복 진입장치를 하나로 통합)
    roadmap_blocks = []
    for cluster_name, slugs in CHAPTER_CLUSTERS:
        cards = []
        for slug in slugs:
            meta = DOC_META[slug]
            href = relative_href(index_path, slug_output_path(slug))
            cards.append(
                f"""<a class="roadmap-card" href="{href}">
              <span class="roadmap-no">{html.escape(slug)}</span>
              <span class="roadmap-body"><strong>{html.escape(meta['label'])}</strong>
              <span>{html.escape(meta['summary'])}</span></span>
            </a>"""
            )
        roadmap_blocks.append(
            f"""<div class="roadmap-cluster">
          <p class="roadmap-cluster-title">{html.escape(cluster_name)}</p>
          <div class="roadmap-grid">{''.join(cards)}</div>
        </div>"""
        )

    pdf_items = []
    for pdf in sorted((DOMAIN_ROOT / "assets" / "pdf").glob("*.pdf")):
        href = relative_href(index_path, pdf)
        pdf_items.append(f"<li><a href='{href}'>{html.escape(pdf.name)}</a></li>")

    ref_items = []
    for _, slug, label in REFERENCE_DOCS:
        href = relative_href(index_path, DOMAIN_ROOT / "references" / slug / "index.html")
        ref_items.append(f"<li><a href='{href}'>{html.escape(label)}</a></li>")

    start_href = relative_href(index_path, slug_output_path("00"))
    sources_href = relative_href(index_path, slug_output_path("sources"))

    html_text = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HeatGrid Domain Guide</title>
  {FONT_LINKS}
  <link rel="stylesheet" href="{relative_href(index_path, CSS_FILE)}">
</head>
<body>
  <div class="landing-shell">
    <section class="hero hero-strong">
      <p class="eyebrow">🔥 HeatGrid Domain Guide</p>
      <h1>지역난방을 몰라도<br>HeatGrid를 이해할 수 있는 학습 사이트</h1>
      <p class="hero-lead">
        지역난방 기계실, 정비, 운영, 데이터를 처음 보는 사람을 위한 교재입니다.
        시간이 없다면 <strong>00번 한 편</strong>만 읽어도 전체 그림이 잡히고,
        더 알고 싶으면 아래 로드맵을 차례대로 따라가면 됩니다.
      </p>
      <div class="cta-row">
        <a class="btn primary" href="{start_href}">00번부터 시작하기 →</a>
        <a class="btn secondary" href="#roadmap">전체 챕터 보기</a>
      </div>
    </section>

    <section class="stepper">
      <div class="step">
        <span class="step-no">1</span>
        <div><strong>기초 잡기</strong><p>지역난방이 뭔지, 데이터가 뭘 알려주는지부터 (00~02)</p></div>
      </div>
      <div class="step-arrow">→</div>
      <div class="step">
        <span class="step-no">2</span>
        <div><strong>현장 이해</strong><p>국내·해외 구조와 설비, 점검·정비 흐름 (03~10)</p></div>
      </div>
      <div class="step-arrow">→</div>
      <div class="step">
        <span class="step-no">3</span>
        <div><strong>서비스 연결</strong><p>시장·정비 출동과 HeatGrid 설계로 (11~12)</p></div>
      </div>
    </section>

    <section class="section-block" id="roadmap">
      <div class="section-head">
        <h2>전체 챕터 로드맵</h2>
        <p>위에서 아래로 읽으면 자연스럽게 이어집니다. 번호를 눌러 바로 들어가세요.</p>
      </div>
      <div class="roadmap">{''.join(roadmap_blocks)}</div>
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
        <h3>소스 인벤토리</h3>
        <p>원문 링크와 로컬 자산 상태를 한곳에서 확인할 수 있다.</p>
        <a class="text-link" href="{sources_href}">sources 페이지 보기 →</a>
      </article>
    </section>
  </div>
</body>
</html>
"""
    index_path.write_text(html_text, encoding="utf-8")


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
