from __future__ import annotations

import math
import textwrap
import zipfile
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from typing import Iterable, Sequence
from xml.sax.saxutils import escape as xml_escape

PDF_PAGE_WIDTH = 595.28
PDF_PAGE_HEIGHT = 841.89

PPT_SLIDE_WIDTH = 13.333
PPT_SLIDE_HEIGHT = 7.5


@dataclass(frozen=True)
class PdfPage:
    commands: list[str]


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value)
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
        "\u00b7": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.replace("\r", " ").replace("\n", " ").strip()


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_text_block(x: float, y: float, lines: Sequence[str], font_size: float = 11, leading: float | None = None, font: str = "/F1", color: tuple[float, float, float] = (0.13, 0.15, 0.17)) -> str:
    leading = leading or (font_size * 1.35)
    parts = [f"BT {font} {font_size:.2f} Tf {color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.2f} {y:.2f} Td"]
    for idx, line in enumerate(lines):
        safe = _pdf_escape(_clean_text(line))
        if idx == 0:
            parts.append(f"({safe}) Tj")
        else:
            parts.append(f"0 -{leading:.2f} Td ({safe}) Tj")
    parts.append("ET")
    return " ".join(parts)


def _wrap(text: str, width: int) -> list[str]:
    cleaned = _clean_text(text)
    if not cleaned:
        return [""]
    return textwrap.wrap(cleaned, width=width, break_long_words=False, break_on_hyphens=False) or [cleaned]


def _rect(x: float, y: float, w: float, h: float, fill: tuple[float, float, float] | None = None, stroke: tuple[float, float, float] | None = None, line_width: float = 1.0) -> str:
    ops: list[str] = ["q"]
    if fill:
        ops.append(f"{fill[0]:.3f} {fill[1]:.3f} {fill[2]:.3f} rg")
    if stroke:
        ops.append(f"{stroke[0]:.3f} {stroke[1]:.3f} {stroke[2]:.3f} RG")
    ops.append(f"{line_width:.2f} w")
    ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
    ops.append("B" if fill and stroke else "f" if fill else "S")
    ops.append("Q")
    return " ".join(ops)


def _line(x1: float, y1: float, x2: float, y2: float, color: tuple[float, float, float] = (0.2, 0.2, 0.2), width: float = 1.0) -> str:
    return f"q {color[0]:.3f} {color[1]:.3f} {color[2]:.3f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q"


def _pdf_stream(commands: Iterable[str]) -> bytes:
    return "\n".join(commands).encode("ascii", errors="ignore")


def build_overview_pdf(payload: dict) -> bytes:
    risk = payload.get("risk", {})
    market = payload.get("market_data", {})
    signals = payload.get("signals", [])
    scenario = payload.get("primary_scenario") or {}
    recommendations = payload.get("recommendations") or {}
    generated_at = _clean_text(payload.get("timestamp") or datetime.utcnow().isoformat())

    corridors = sorted(risk.get("corridors", []), key=lambda item: item.get("composite_risk", 0), reverse=True)
    top_corridors = corridors[:4]
    signal_items = signals[:4]
    rec_items = recommendations.get("recommendations", [])[:4]

    pages: list[PdfPage] = []

    page1: list[str] = []
    page1.append(_rect(0, PDF_PAGE_HEIGHT - 92, PDF_PAGE_WIDTH, 92, fill=(0.08, 0.14, 0.18)))
    page1.append(_pdf_text_block(36, PDF_PAGE_HEIGHT - 48, ["ENERGEM", "EXECUTIVE OVERVIEW"], font_size=22, leading=24, font="/F2", color=(1, 1, 1)))
    page1.append(_pdf_text_block(390, PDF_PAGE_HEIGHT - 40, [f"Generated {generated_at}"], font_size=9, font="/F1", color=(0.85, 0.9, 0.92)))
    page1.append(_pdf_text_block(36, PDF_PAGE_HEIGHT - 118, [f"Primary threat: {_clean_text(risk.get('primary_threat', 'N/A'))}", f"Risk level: {_clean_text(risk.get('risk_level', 'N/A'))}", f"Overall score: {risk.get('overall_risk_score', 0):.1f}"], font_size=12, leading=16, font="/F2", color=(0.12, 0.17, 0.2)))

    card_y = PDF_PAGE_HEIGHT - 210
    card_specs = [
        (36, 165, "RISK SCORE", f"{risk.get('overall_risk_score', 0):.1f}", "Composite disruption outlook across monitored corridors."),
        (215, 165, "TOP THREAT", _clean_text(risk.get("primary_threat", "N/A")), "Most likely trigger for immediate intervention."),
        (394, 165, "MARKET VIEW", _clean_text(market.get("brent_crude", {}).get("current_price", "N/A")), "Latest benchmark context used in scenario modeling."),
    ]
    for x, w, title, value, caption in card_specs:
        page1.append(_rect(x, card_y, w, 108, fill=(0.97, 0.98, 0.99), stroke=(0.82, 0.86, 0.88), line_width=1))
        page1.append(_pdf_text_block(x + 14, card_y + 84, [title], font_size=10, font="/F2", color=(0.09, 0.31, 0.37)))
        page1.append(_pdf_text_block(x + 14, card_y + 54, [_clean_text(value)], font_size=18, font="/F2", color=(0.13, 0.15, 0.17)))
        page1.append(_pdf_text_block(x + 14, card_y + 24, _wrap(caption, 28), font_size=9, leading=12, font="/F1", color=(0.34, 0.38, 0.4)))

    page1.append(_pdf_text_block(36, 470, ["EXECUTIVE SUMMARY"], font_size=13, font="/F2", color=(0.09, 0.31, 0.37)))
    summary_lines = [
        f"Current monitoring indicates {_clean_text(risk.get('primary_threat', 'an elevated disruption profile'))}.",
        f"Risk posture is classified as {_clean_text(risk.get('risk_level', 'unknown')).upper()} with an overall score of {risk.get('overall_risk_score', 0):.1f}.",
    ]
    if scenario:
        summary_lines.append(f"Latest modeled scenario: {_clean_text(scenario.get('scenario_name', 'N/A'))} with confidence {_clean_text(scenario.get('confidence', 'N/A'))}.")
    if recommendations:
        summary_lines.append(f"Procurement strategy includes {len(rec_items)} highlighted actions from the approved recommendation set.")
    page1.append(_pdf_text_block(36, 446, _wrap(" ".join(summary_lines), 92), font_size=10.5, leading=14, font="/F1"))

    page1.append(_pdf_text_block(36, 390, ["RECENT SIGNALS"], font_size=13, font="/F2", color=(0.09, 0.31, 0.37)))
    cursor_y = 374
    for idx, signal in enumerate(signal_items, start=1):
        headline = _clean_text(signal.get("headline") or signal.get("event") or "Signal")
        corridor = _clean_text(signal.get("corridor", ""))
        impact = signal.get("impact", {})
        page1.append(_pdf_text_block(44, cursor_y, [f"{idx}. {headline}"], font_size=10.5, font="/F2"))
        cursor_y -= 12
        page1.append(_pdf_text_block(58, cursor_y, _wrap(f"Corridor: {corridor} | Risk delta: {_clean_text(impact.get('risk_delta', 'N/A'))} | Supply impact: {_clean_text(impact.get('supply_impact', 'N/A'))}", 86), font_size=9.2, leading=11, font="/F1", color=(0.33, 0.36, 0.39)))
        cursor_y -= 23

    page1.append(_pdf_text_block(36, 160, ["TOP CORRIDORS"], font_size=13, font="/F2", color=(0.09, 0.31, 0.37)))
    table_y = 136
    for corridor in top_corridors:
        page1.append(_rect(36, table_y - 4, 523, 22, fill=(0.98, 0.99, 0.99), stroke=(0.89, 0.91, 0.93), line_width=0.8))
        row = f"{_clean_text(corridor.get('corridor', corridor.get('name', 'N/A'))).upper():<18}  SCORE {corridor.get('composite_risk', 0):>6.1f}  PROB {corridor.get('probability_percent', 0):>5.1f}%  CONF {_clean_text(corridor.get('confidence', 'N/A')).upper()}"
        page1.append(_pdf_text_block(48, table_y + 2, [row], font_size=9.5, font="/F1"))
        table_y -= 26

    page1.append(_pdf_text_block(36, 48, ["ENERGEM - CONFIDENTIAL INTERNAL EXECUTIVE BRIEF"], font_size=8.5, font="/F1", color=(0.42, 0.45, 0.47)))
    pages.append(PdfPage(page1))

    page2: list[str] = []
    page2.append(_rect(0, PDF_PAGE_HEIGHT - 72, PDF_PAGE_WIDTH, 72, fill=(0.11, 0.16, 0.2)))
    page2.append(_pdf_text_block(36, PDF_PAGE_HEIGHT - 38, ["ENERGEM EXECUTIVE OVERVIEW - DETAIL"], font_size=18, font="/F2", color=(1, 1, 1)))
    page2.append(_pdf_text_block(36, PDF_PAGE_HEIGHT - 96, ["RECOMMENDED ACTIONS"], font_size=13, font="/F2", color=(0.09, 0.31, 0.37)))
    if rec_items:
        y = PDF_PAGE_HEIGHT - 120
        for rec in rec_items:
            page2.append(_rect(36, y - 8, 523, 52, fill=(0.98, 0.99, 0.99), stroke=(0.86, 0.89, 0.91), line_width=0.8))
            title = f"PRIORITY {_clean_text(rec.get('priority', '?')).upper()} - {_clean_text(rec.get('supplier', 'Unknown')).upper()}"
            page2.append(_pdf_text_block(48, y + 22, [title], font_size=10.5, font="/F2"))
            body = (
                f"Volume {_clean_text(rec.get('volume_bbl_per_day', 0))} BBL/DAY | "
                f"ETA {_clean_text(rec.get('eta_days', 0))} DAYS | "
                f"Premium ${float(rec.get('cost_premium_per_barrel', 0)):,.2f}/bbl | "
                f"Risk {_clean_text(rec.get('geopolitical_risk', 'N/A')).upper()} | "
                f"Confidence {_clean_text(rec.get('confidence', 'N/A'))}%"
            )
            page2.append(_pdf_text_block(48, y + 8, _wrap(body, 88), font_size=9.2, leading=11, font="/F1", color=(0.32, 0.35, 0.38)))
            reason = _clean_text(rec.get("reasoning", ""))
            page2.append(_pdf_text_block(48, y - 5, _wrap(f"Rationale: {reason}", 88), font_size=8.8, leading=10.5, font="/F1", color=(0.44, 0.47, 0.49)))
            y -= 68
    else:
        page2.append(_pdf_text_block(48, PDF_PAGE_HEIGHT - 122, ["No recommendation records were available at the time of export."], font_size=10, font="/F1"))

    page2.append(_pdf_text_block(36, 274, ["MARKET CONTEXT"], font_size=13, font="/F2", color=(0.09, 0.31, 0.37)))
    market_lines = [
        f"Brent crude: {_clean_text(market.get('brent_crude', {}).get('current_price', 'N/A'))}",
        f"WTI crude: {_clean_text(market.get('wti_crude', {}).get('current_price', 'N/A'))}",
        f"Natural gas: {_clean_text(market.get('natural_gas', {}).get('current_price', 'N/A'))}",
    ]
    page2.append(_rect(36, 158, 523, 98, fill=(0.97, 0.98, 0.99), stroke=(0.86, 0.89, 0.91), line_width=0.8))
    page2.append(_pdf_text_block(48, 226, market_lines, font_size=10, leading=16, font="/F1"))
    page2.append(_pdf_text_block(36, 100, ["This document was generated automatically from the live dashboard payload."], font_size=9, font="/F1", color=(0.43, 0.46, 0.49)))
    page2.append(_pdf_text_block(36, 72, [f"Timestamp: {generated_at}"], font_size=8.5, font="/F1", color=(0.48, 0.51, 0.54)))
    pages.append(PdfPage(page2))

    page_streams = [_pdf_stream(page.commands) for page in pages]
    object_defs: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{' '.join(f'{4 + idx * 2} 0 R' for idx in range(len(page_streams)))}] /Count {len(page_streams)} >>".encode("ascii"),
    ]
    for index, stream in enumerate(page_streams):
        content_obj = 3 + index * 2
        object_defs.append(f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"\nendstream")
        object_defs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PDF_PAGE_WIDTH:.2f} {PDF_PAGE_HEIGHT:.2f}] /Resources << /Font << /F1 {3 + len(page_streams) * 2} 0 R /F2 {4 + len(page_streams) * 2} 0 R >> >> /Contents {content_obj} 0 R >>".encode("ascii"))
    object_defs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    object_defs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    output = BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for obj_index, obj in enumerate(object_defs, start=1):
        offsets.append(output.tell())
        output.write(f"{obj_index} 0 obj\n".encode("ascii"))
        output.write(obj)
        output.write(b"\nendobj\n")

    xref_offset = output.tell()
    output.write(f"xref\n0 {len(object_defs) + 1}\n".encode("ascii"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.write(b"trailer\n")
    output.write(f"<< /Size {len(object_defs) + 1} /Root 1 0 R >>\n".encode("ascii"))
    output.write(b"startxref\n")
    output.write(f"{xref_offset}\n".encode("ascii"))
    output.write(b"%%EOF")
    return output.getvalue()


def _pptx_text_box(shape_id: int, x: float, y: float, w: float, h: float, title: str, body_lines: Sequence[str], fill: str = "1FFFFFF", accent: str = "2F5D62") -> str:
    paras = [f"""
        <a:p>
          <a:pPr/>
          <a:r>
            <a:rPr lang=\"en-US\" sz=\"2200\" b=\"1\" dirty=\"0\" smtClean=\"0\">
              <a:solidFill><a:srgbClr val=\"{accent}\"/></a:solidFill>
            </a:rPr>
            <a:t>{xml_escape(_clean_text(title))}</a:t>
          </a:r>
        </a:p>
    """]
    for line in body_lines:
        paras.append(f"""
        <a:p>
          <a:pPr lvl=\"0\" marL=\"0\" indent=\"0\"/>
          <a:r>
            <a:rPr lang=\"en-US\" sz=\"1500\" dirty=\"0\" smtClean=\"0\"/>
            <a:t>{xml_escape(_clean_text(line))}</a:t>
          </a:r>
        </a:p>
        """)
    return f"""
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id=\"{shape_id}\" name=\"TextBox {shape_id}\"/>
        <p:cNvSpPr txBox=\"1\"/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm>
          <a:off x=\"{int(x * 914400)}\" y=\"{int(y * 914400)}\"/>
          <a:ext cx=\"{int(w * 914400)}\" cy=\"{int(h * 914400)}\"/>
        </a:xfrm>
        <a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom>
        <a:solidFill><a:srgbClr val=\"{fill}\"/></a:solidFill>
        <a:ln><a:solidFill><a:srgbClr val=\"D9DEE3\"/></a:solidFill></a:ln>
      </p:spPr>
      <p:txBody>
        <a:bodyPr wrap=\"square\" rtlCol=\"0\" anchor=\"t\"/>
        <a:lstStyle/>
        {''.join(paras)}
      </p:txBody>
    </p:sp>
    """


def _pptx_title_block(shape_id: int, title: str, subtitle: str, meta: str) -> str:
    return f"""
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id=\"{shape_id}\" name=\"Title {shape_id}\"/>
        <p:cNvSpPr txBox=\"1\"/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm>
          <a:off x=\"548640\" y=\"457200\"/>
          <a:ext cx=\"11430000\" cy=\"2286000\"/>
        </a:xfrm>
        <a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom>
      </p:spPr>
      <p:txBody>
        <a:bodyPr wrap=\"square\"/>
        <a:lstStyle/>
        <a:p>
          <a:r>
            <a:rPr lang=\"en-US\" sz=\"2800\" b=\"1\" dirty=\"0\" smtClean=\"0\">
              <a:solidFill><a:srgbClr val=\"163A45\"/></a:solidFill>
            </a:rPr>
            <a:t>{xml_escape(_clean_text(title))}</a:t>
          </a:r>
        </a:p>
        <a:p>
          <a:r>
            <a:rPr lang=\"en-US\" sz=\"1500\" dirty=\"0\" smtClean=\"0\">
              <a:solidFill><a:srgbClr val=\"41515B\"/></a:solidFill>
            </a:rPr>
            <a:t>{xml_escape(_clean_text(subtitle))}</a:t>
          </a:r>
        </a:p>
        <a:p>
          <a:r>
            <a:rPr lang=\"en-US\" sz=\"1200\" dirty=\"0\" smtClean=\"0\">
              <a:solidFill><a:srgbClr val=\"68737B\"/></a:solidFill>
            </a:rPr>
            <a:t>{xml_escape(_clean_text(meta))}</a:t>
          </a:r>
        </a:p>
      </p:txBody>
    </p:sp>
    """


def _pptx_slide(slide_title: str, subtitle: str, blocks: Sequence[str], footer: str) -> str:
    shapes = [_pptx_title_block(2, slide_title, subtitle, footer)]
    positions = [
        (0.55, 1.95, 3.95, 1.35),
        (4.7, 1.95, 3.95, 1.35),
        (8.85, 1.95, 3.9, 1.35),
        (0.55, 3.65, 4.0, 1.55),
        (4.7, 3.65, 4.0, 1.55),
        (8.85, 3.65, 3.9, 1.55),
    ]
    for idx, block in enumerate(blocks[:6]):
        x, y, w, h = positions[idx]
        title = block.split("\n", 1)[0]
        body = block.split("\n", 1)[1:] or [""]
        body_lines = []
        for part in body:
            body_lines.extend([line for line in part.split("\n") if line.strip()])
        shapes.append(_pptx_text_box(3 + idx, x, y, w, h, title, body_lines, fill="F8FAFB"))
    return f"""
    <p:sld xmlns:p=\"http://schemas.openxmlformats.org/presentationml/2006/main\" xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">
      <p:cSld>
        <p:spTree>
          <p:nvGrpSpPr>
            <p:cNvPr id=\"1\" name=\"\"/>
            <p:cNvGrpSpPr/>
            <p:nvPr/>
          </p:nvGrpSpPr>
          <p:grpSpPr>
            <a:xfrm>
              <a:off x=\"0\" y=\"0\"/>
              <a:ext cx=\"0\" cy=\"0\"/>
              <a:chOff x=\"0\" y=\"0\"/>
              <a:chExt cx=\"0\" cy=\"0\"/>
            </a:xfrm>
          </p:grpSpPr>
          {''.join(shapes)}
        </p:spTree>
      </p:cSld>
      <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
    </p:sld>
    """


def build_procurement_pptx(payload: dict) -> bytes:
    recommendations = payload.get("recommendations", [])
    generated_at = _clean_text(datetime.utcnow().isoformat(timespec="seconds") + "Z")
    total_volume = sum(int(item.get("volume_bbl_per_day", 0)) for item in recommendations)
    total_premium = sum(int(item.get("volume_bbl_per_day", 0)) * float(item.get("cost_premium_per_barrel", 0)) for item in recommendations)
    can_execute = payload.get("execution_readiness", {}).get("can_execute_all", False)
    blockers = payload.get("execution_readiness", {}).get("blockers", [])

    title_slide = _pptx_slide(
        "ENERGEM PROCUREMENT BRIEF",
        f"Scenario {payload.get('scenario_id', 'N/A')} | Authority {_clean_text(payload.get('authority_level', 'N/A')).upper()}",
        [
            f"Total volume\n{total_volume:,} BBL/DAY",
            f"Estimated premium\n${total_premium:,.0f}",
            f"Execution readiness\n{'CLEAR' if can_execute else 'BLOCKED'}",
            f"Blockers\n{', '.join(blockers) if blockers else 'None'}",
        ],
        f"Generated {generated_at}",
    )

    summary_blocks = [
        "Executive Summary\nProfessional procurement presentation generated from live recommendations.",
        f"Readiness\n{'All selected recommendations are ready for execution.' if can_execute else 'Execution is constrained by active blockers.'}",
        f"Approved volume\n{payload.get('execution_readiness', {}).get('total_approved_volume', 0):,} BBL/DAY",
        "Operating guidance\nPrioritize highest confidence supply options while preserving continuity buffers.",
    ]
    overview_slide = _pptx_slide(
        "READINESS OVERVIEW",
        "Summary of current procurement posture",
        summary_blocks,
        f"Scenario {payload.get('scenario_id', 'N/A')}",
    )

    detail_blocks: list[str] = []
    for rec in recommendations[:6]:
        detail_blocks.append(
            "\n".join(
                [
                    f"Priority {rec.get('priority', '?')} - {rec.get('supplier', 'Unknown')}",
                    f"Volume: {int(rec.get('volume_bbl_per_day', 0)):,} BBL/DAY",
                    f"ETA: {rec.get('eta_days', 0)} DAYS | Risk: {str(rec.get('geopolitical_risk', '')).upper()}",
                    f"Confidence: {rec.get('confidence', 0)}% | Status: {str(rec.get('status', '')).upper()}",
                    f"Reasoning: {rec.get('reasoning', '')}",
                ]
            )
        )
    details_slide = _pptx_slide(
        "SUPPLIER MATRIX",
        "Recommendation-by-recommendation detail",
        detail_blocks or ["No recommendations available\nThe system returned no procurement actions for this scenario."],
        "ENERGEM PROCUREMENT",
    )

    slides = [title_slide, overview_slide, details_slide]

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
      <Default Extension="xml" ContentType="application/xml"/>
      <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
      <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
      <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
      <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
      <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
      <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
      <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
      <Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
      <Override PartName="/ppt/slides/slide3.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
    </Types>
    """

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
      <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
      <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
    </Relationships>
    """

    presentation_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <p:sldMasterIdLst>
        <p:sldMasterId id="2147483648" r:id="rId1"/>
      </p:sldMasterIdLst>
      <p:sldIdLst>
        <p:sldId id="256" r:id="rId2"/>
        <p:sldId id="257" r:id="rId3"/>
        <p:sldId id="258" r:id="rId4"/>
      </p:sldIdLst>
      <p:slideSize cx="12192000" cy="6858000"/>
      <p:notesSize cx="6858000" cy="9144000"/>
      <p:defaultTextStyle/>
    </p:presentation>
    """

    presentation_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
      <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
      <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>
      <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide3.xml"/>
      <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
    </Relationships>
    """

    slide_master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sldMaster xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <p:cSld>
        <p:spTree>
          <p:nvGrpSpPr>
            <p:cNvPr id="1" name=""/>
            <p:cNvGrpSpPr/>
            <p:nvPr/>
          </p:nvGrpSpPr>
          <p:grpSpPr>
            <a:xfrm>
              <a:off x="0" y="0"/>
              <a:ext cx="0" cy="0"/>
              <a:chOff x="0" y="0"/>
              <a:chExt cx="0" cy="0"/>
            </a:xfrm>
          </p:grpSpPr>
        </p:spTree>
      </p:cSld>
      <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
      <p:sldLayoutIdLst>
        <p:sldLayoutId id="1" r:id="rId1"/>
      </p:sldLayoutIdLst>
      <p:txStyles/>
    </p:sldMaster>
    """

    slide_master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
      <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
    </Relationships>
    """

    slide_layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sldLayout xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" type="blank" preserve="1">
      <p:cSld>
        <p:spTree>
          <p:nvGrpSpPr>
            <p:cNvPr id="1" name=""/>
            <p:cNvGrpSpPr/>
            <p:nvPr/>
          </p:nvGrpSpPr>
          <p:grpSpPr>
            <a:xfrm>
              <a:off x="0" y="0"/>
              <a:ext cx="0" cy="0"/>
              <a:chOff x="0" y="0"/>
              <a:chExt cx="0" cy="0"/>
            </a:xfrm>
          </p:grpSpPr>
        </p:spTree>
      </p:cSld>
      <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
    </p:sldLayout>
    """

    slide_layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
    </Relationships>
    """

    theme = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Energem">
      <a:themeElements>
        <a:clrScheme name="Energem">
          <a:dk1><a:sysClr val="windowText" lastClr="1A2024"/></a:dk1>
          <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
          <a:dk2><a:srgbClr val="1F2933"/></a:dk2>
          <a:lt2><a:srgbClr val="F8FAFB"/></a:lt2>
          <a:accent1><a:srgbClr val="2F5D62"/></a:accent1>
          <a:accent2><a:srgbClr val="D08C3A"/></a:accent2>
          <a:accent3><a:srgbClr val="8BA23F"/></a:accent3>
          <a:accent4><a:srgbClr val="A66459"/></a:accent4>
          <a:accent5><a:srgbClr val="5B7C99"/></a:accent5>
          <a:accent6><a:srgbClr val="4B5563"/></a:accent6>
          <a:hlink><a:srgbClr val="2563EB"/></a:hlink>
          <a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>
        </a:clrScheme>
        <a:fontScheme name="Energem">
          <a:majorFont>
            <a:latin typeface="Aptos Display"/>
            <a:ea typeface=""/>
            <a:cs typeface=""/>
          </a:majorFont>
          <a:minorFont>
            <a:latin typeface="Aptos"/>
            <a:ea typeface=""/>
            <a:cs typeface=""/>
          </a:minorFont>
        </a:fontScheme>
        <a:fmtScheme name="Energem">
          <a:fillStyleLst>
            <a:solidFill><a:schemeClr val="accent1"/></a:solidFill>
            <a:solidFill><a:schemeClr val="accent2"/></a:solidFill>
            <a:solidFill><a:schemeClr val="accent3"/></a:solidFill>
          </a:fillStyleLst>
          <a:lnStyleLst>
            <a:ln w="9525"><a:solidFill><a:schemeClr val="accent1"/></a:solidFill></a:ln>
          </a:lnStyleLst>
          <a:effectStyleLst>
            <a:effectStyle/>
          </a:effectStyleLst>
          <a:bgFillStyleLst>
            <a:solidFill><a:schemeClr val="lt1"/></a:solidFill>
          </a:bgFillStyleLst>
        </a:fmtScheme>
      </a:themeElements>
      <a:objectDefaults/>
      <a:extraClrSchemeLst/>
    </a:theme>
    """

    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <dc:title>Energem Procurement Brief</dc:title>
      <dc:creator>Energem</dc:creator>
      <cp:lastModifiedBy>Energem</cp:lastModifiedBy>
      <dcterms:created xsi:type="dcterms:W3CDTF">{datetime.utcnow().isoformat(timespec="seconds")}Z</dcterms:created>
      <dcterms:modified xsi:type="dcterms:W3CDTF">{datetime.utcnow().isoformat(timespec="seconds")}Z</dcterms:modified>
    </cp:coreProperties>
    """

    app = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
      <Application>Energem</Application>
      <PresentationFormat>Energem Procurement Brief</PresentationFormat>
      <Slides>{len(slides)}</Slides>
      <Notes>0</Notes>
      <HiddenSlides>0</HiddenSlides>
      <MMClips>0</MMClips>
      <ScaleCrop>false</ScaleCrop>
      <HeadingPairs>
        <vt:vector size="2" baseType="variant">
          <vt:variant><vt:lpstr>Slides</vt:lpstr></vt:variant>
          <vt:variant><vt:i4>{len(slides)}</vt:i4></vt:variant>
        </vt:vector>
      </HeadingPairs>
      <TitlesOfParts>
        <vt:vector size="{len(slides)}" baseType="lpstr">
          <vt:lpstr>Title</vt:lpstr>
          <vt:lpstr>Overview</vt:lpstr>
          <vt:lpstr>Matrix</vt:lpstr>
        </vt:vector>
      </TitlesOfParts>
      <Company>Energem</Company>
      <LinksUpToDate>false</LinksUpToDate>
      <SharedDoc>false</SharedDoc>
      <HyperlinksChanged>false</HyperlinksChanged>
      <AppVersion>16.0000</AppVersion>
    </Properties>
    """

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types.strip())
        zf.writestr("_rels/.rels", rels.strip())
        zf.writestr("ppt/presentation.xml", presentation_xml.strip())
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels.strip())
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master.strip())
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels.strip())
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout.strip())
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels.strip())
        zf.writestr("ppt/theme/theme1.xml", theme.strip())
        zf.writestr("docProps/core.xml", core.strip())
        zf.writestr("docProps/app.xml", app.strip())
        for idx, slide_xml in enumerate(slides, start=1):
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide_xml.strip())
            zf.writestr(
                f"ppt/slides/_rels/slide{idx}.xml.rels",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>""",
            )
    return buffer.getvalue()
