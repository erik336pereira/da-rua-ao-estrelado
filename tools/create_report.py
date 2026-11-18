from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SHOTS = DOCS / "screenshots"
ASSETS = DOCS / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
OUT = DOCS / "Projeto_de_Sistemas_Interativos.docx"
REPO_URL = "https://github.com/erik336pereira/da-rua-ao-estrelado"

NAVY = "15345B"
BLUE = "168CC8"
GOLD = "F2BD42"
INK = "263447"
MUTED = "617080"
PALE = "EAF5FA"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def add_hyperlink(paragraph, text, url):
    relationship_id = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), BLUE)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.append(color)
    properties.append(underline)
    run.append(properties)
    text_node = OxmlElement("w:t")
    text_node.text = text
    run.append(text_node)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def set_cell_margins(cell, top=90, start=120, bottom=90, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("AS AVENTURAS DE UM JOGADOR  •  ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor.from_string(MUTED)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)


def configure_doc(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.64)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    for name, size, color in (("Title", 30, NAVY), ("Heading 1", 19, NAVY), ("Heading 2", 12, BLUE)):
        style = styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(5 if name == "Heading 1" else 3)
        style.paragraph_format.space_after = Pt(7 if name == "Heading 1" else 4)
        style.paragraph_format.keep_with_next = True
    footer = section.footer.paragraphs[0]
    add_page_number(footer)


def add_label(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text.upper())
    r.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string(BLUE)
    return p


def add_heading(doc, title, subtitle=None):
    doc.add_heading(title, level=1)
    if subtitle:
        p = doc.add_paragraph(subtitle)
        p.paragraph_format.space_after = Pt(10)
        for run in p.runs:
            run.italic = True
            run.font.color.rgb = RGBColor.from_string(MUTED)


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string(MUTED)


def character_sheet():
    entries = [
        ("player", "JOGADOR"),
        ("referee", "JUIZ"),
        ("goalie", "GOLEIRO / VAR"),
        ("fan", "TORCEDOR"),
        ("red_card_boss", "CARTAO VERMELHO"),
    ]
    cards = []
    for key, label in entries:
        src = ROOT / "assets" / "sprites" / f"{key}.png"
        sheet = Image.open(src).convert("RGBA")
        frame_w = 32 if key in ("red_card_boss", "player") else 24
        frame_h = 40 if key == "red_card_boss" else 32
        frame = sheet.crop((frame_w, 0, frame_w * 2, frame_h))
        frame = frame.resize((frame.width * 3, frame.height * 3), Image.Resampling.NEAREST)
        cards.append((label, frame))
    canvas = Image.new("RGBA", (1040, 245), (234, 245, 250, 255))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 19)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, sprite) in enumerate(cards):
        x = i * 208
        draw.rounded_rectangle((x + 8, 10, x + 200, 235), radius=8, fill=(255, 255, 255, 255), outline=(198, 219, 232, 255), width=2)
        sprite.thumbnail((142, 142), Image.Resampling.NEAREST)
        canvas.alpha_composite(sprite, (x + (208 - sprite.width) // 2, 27))
        box = draw.textbbox((0, 0), label, font=font)
        draw.text((x + (208 - (box[2] - box[0])) // 2, 190), label, font=font, fill=(21, 52, 91, 255))
    path = ASSETS / "personagens.png"
    canvas.save(path)
    return path


def add_image_pair(doc, left_path, left_caption, right_path, right_caption, width=3.3):
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    for cell, path, caption in zip(table.rows[0].cells, (left_path, right_path), (left_caption, right_caption)):
        cell.width = Inches(width + 0.12)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_margins(cell, 30, 45, 20, 45)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(str(path), width=Inches(width))
        c = cell.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_after = Pt(0)
        r = c.add_run(caption)
        r.italic = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor.from_string(MUTED)
    return table


def add_image_triplet(doc, entries, width=2.05):
    table = doc.add_table(rows=1, cols=3)
    table.autofit = False
    for cell, (path, caption) in zip(table.rows[0].cells, entries):
        cell.width = Inches(width + 0.1)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_margins(cell, 25, 35, 15, 35)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(str(path), width=Inches(width))
        c = cell.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_after = Pt(0)
        r = c.add_run(caption)
        r.italic = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor.from_string(MUTED)
    return table


def build():
    sheet_path = character_sheet()
    doc = Document()
    configure_doc(doc)

    # Página 1 — capa institucional
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    r = p.add_run("UNIVERSIDADE NOVE DE JULHO — UNINOVE")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor.from_string(NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DIRETORIA DOS CURSOS DE INFORMÁTICA")
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor.from_string(MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    r = p.add_run("PROJETO DE EXTENSÃO EM SISTEMAS INTERATIVOS")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor.from_string(BLUE)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(48)
    p.paragraph_format.space_after = Pt(16)
    r = p.add_run("AS AVENTURAS\nDE UM JOGADOR")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(32)
    r.font.color.rgb = RGBColor.from_string(NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Jogo de plataforma 2D com tema de futebol")
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor.from_string(MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(24)
    p.add_run().add_picture(str(SHOTS / "gameplay.png"), width=Inches(5.8))
    add_caption(doc, "Cena da fase — arte original em pixel art.")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(54)
    p.add_run("SÃO PAULO\n2026").bold = True

    # Página 2 — folha de rosto e integrantes editáveis
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    r = p.add_run("AS AVENTURAS DE UM JOGADOR")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor.from_string(NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(44)
    p.add_run("Projeto desenvolvido na disciplina Projeto de Extensão em Sistemas Interativos, como jogo de plataforma 2D para computador com a engine Godot.")
    p.paragraph_format.left_indent = Inches(1.0)
    p.paragraph_format.right_indent = Inches(1.0)
    p.paragraph_format.line_spacing = 1.25
    add_label(doc, "Integrantes do grupo")
    members = [
        ("Erik Pereira de Almeida — Líder", "924115897"),
        ("Felipe Gabriel Cruz Medeiros", "924100952"),
        ("Letícia da Silva Oliveira", "924103216"),
        ("Gabriel Santos de Jesus", "924110011"),
        ("Marcos Daniel Ribeiro Siriano", "924115034"),
    ]
    roster = doc.add_table(rows=len(members), cols=1)
    roster.autofit = False
    roster.columns[0].width = Inches(6.7)
    for n, row in enumerate(roster.rows, 1):
        cell = row.cells[0]
        cell.width = Inches(6.7)
        set_cell_shading(cell, PALE if n % 2 else "F7FAFC")
        set_cell_margins(cell, 70, 150, 70, 150)
        member_name, member_ra = members[n-1]
        cell.text = f"{n:02d}. {member_name}   —   RA: {member_ra}"
        for para in cell.paragraphs:
            para.paragraph_format.space_after = Pt(1)
            for run in para.runs:
                run.font.size = Pt(8.5)
    add_label(doc, "Orientação e disciplina")
    p = doc.add_paragraph()
    p.add_run("Professor: ").bold = True
    p.add_run("Leandro Fernandes da Mota")
    p = doc.add_paragraph()
    p.add_run("Disciplina: ").bold = True
    p.add_run("Projeto de Extensão em Sistemas Interativos")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(45)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("São Paulo\n2026")

    # Página 3 — sumário
    doc.add_page_break()
    add_heading(doc, "SUMÁRIO", "Estrutura do projeto e das entregas.")
    items = [
        ("1. Objetivo e proposta", "4"),
        ("2. História e ambientação", "4"),
        ("3. Recursos, personagens e cenários", "4"),
        ("4. Jogabilidade, controles e desafios", "5"),
        ("5. Telas e áudio", "5"),
        ("6. Página do jogo e distribuição", "6"),
        ("7. Referências e endereços", "6"),
    ]
    for name, page in items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(12)
        p.add_run(name)
        p.add_run("  " + "· " * 15 + "  " + page).font.color.rgb = RGBColor.from_string(MUTED)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(40)
    r = p.add_run("PLATAFORMA")
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(BLUE)
    doc.add_paragraph("Computador (Windows) e navegador compatível com a exportação Web de Godot. Jogo individual; não há modo multijogador.")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    r = p.add_run("TECNOLOGIA")
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(BLUE)
    doc.add_paragraph("Godot 4.7.2, GDScript, recursos gráficos e áudio originais preparados para o projeto.")

    # Página 4 — objetivo, história, arte
    doc.add_page_break()
    add_heading(doc, "1. OBJETIVO E PROPOSTA")
    doc.add_paragraph("Desenvolver um jogo de plataforma 2D no qual o jogador atravessa um percurso inspirado no futebol, enfrenta adversários e alcança o estádio. O projeto prioriza controles de teclado, leitura clara dos perigos, coleta de recursos e uma conclusão após a luta contra um chefe.")
    doc.add_heading("2. HISTÓRIA E AMBIENTAÇÃO", level=2)
    doc.add_paragraph("Um jovem jogador está a caminho de sua grande partida. Para chegar ao estádio, ele precisa cruzar ruas e áreas de acesso tomadas por desafios futebolísticos: o juiz lança cartões, o goleiro sai do gol para persegui-lo, a torcida atrapalha o caminho e um enorme Cartão Vermelho protege o portão final. Vencido o chefe, os portões se abrem e o atleta pode entrar no estádio, enquanto a frase ‘PORTÕES ABERTOS!’ salta suavemente acima da estrutura e dois fogos explodem sobre o telhado.")
    doc.add_heading("3. RECURSOS, PERSONAGENS E CENÁRIOS", level=2)
    doc.add_paragraph("A direção visual usa pixel art original com paleta azul, verde e terrosa. Os sprites têm quadros de movimento para corrida, cabeçada, carrinho e chute. O cenário combina céu em camadas, prédios, plataformas, gramado, terra e estádio; corações recuperam vida, bolas ampliam a munição e um troféu rende pontos após a derrota do chefe.")
    doc.add_picture(str(sheet_path), width=Inches(6.55))
    add_caption(doc, "Personagens originais: jogador, juiz, goleiro/VAR, torcedor e chefe Cartão Vermelho.")
    add_image_pair(doc, SHOTS / "gameplay.png", "Trecho da fase", SHOTS / "headbutt.png", "Sequência da cabeçada", width=3.12)
    add_image_pair(doc, SHOTS / "kick.png", "Chute com preparação, contato e recuperação", SHOTS / "trophy.png", "Troféu na plataforma após derrotar o chefe", width=3.12)

    # Página 5 — sistemas, inimigos, tela e áudio
    doc.add_page_break()
    add_heading(doc, "4. JOGABILIDADE, CONTROLES E DESAFIOS")
    controls = [
        ("Mover", "A / D ou setas esquerda/direita"),
        ("Pular", "Espaço, W ou seta para cima"),
        ("Cabeçada", "J — ataque de curta distância"),
        ("Carrinho", "K — investida rasteira"),
        ("Chute", "L — arremessa uma bola consumível"),
        ("Pausar / voltar", "P ou Esc"),
        ("Iniciar / continuar", "Enter; Espaço também inicia na tela de título"),
        ("Reiniciar durante a pausa", "R"),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    table.columns[0].width = Inches(1.55)
    table.columns[1].width = Inches(5.1)
    for i, title in enumerate(("AÇÃO", "TECLA / EFEITO")):
        cell = table.rows[0].cells[i]
        cell.text = title
        set_cell_shading(cell, NAVY)
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(255, 255, 255)
    set_repeat_table_header(table.rows[0])
    for row_index, (action, keys) in enumerate(controls):
        cells = table.add_row().cells
        cells[0].text = action
        cells[1].text = keys
        for cell in cells:
            set_cell_margins(cell, 60, 100, 60, 100)
            if row_index % 2 == 0:
                set_cell_shading(cell, PALE)
            for para in cell.paragraphs:
                para.paragraph_format.space_after = Pt(0)
                for run in para.runs:
                    run.font.size = Pt(8.5)
    doc.add_heading("Adversários e recursos", level=2)
    add_bullet(doc, "Juiz: patrulha e lança cartões amarelos; o contato e os projéteis causam dano.")
    add_bullet(doc, "Goleiro/VAR: persegue o jogador, pula para alcançar plataformas e tenta colidir com ele.")
    add_bullet(doc, "Torcedor: ocupa a rota e se movimenta pelo trecho em que aparece.")
    add_bullet(doc, "Chefe Cartão Vermelho: um cartão vermelho vivo, retangular, com braços e pernas. Ele arremessa cartões à distância e golpeia de perto; sua barra de vida precisa chegar a zero para abrir o portão.")
    add_bullet(doc, "O HUD acompanha vidas, bolas e pontuação. Corações restauram vida; bolas recuperam munição. A invulnerabilidade breve após dano evita golpes consecutivos instantâneos.")
    doc.add_heading("5. TELAS E ÁUDIO", level=2)
    doc.add_paragraph("O menu inicial concentra o botão de começar e acessos separados para Configurações e Controles. Na pausa, o jogador pode continuar, abrir essas telas ou reiniciar. Configurações oferece um controle deslizante de volume de 0% a 100%, ajustável com clique ou arraste. A tela de Controles reúne as teclas de movimento, pulo, ataques, pausa e reinício. Na vitória e na derrota, é possível iniciar um novo jogo ou voltar ao menu principal. Depois que o chefe é derrotado, ‘PORTÕES ABERTOS!’ aparece acima do estádio com uma animação leve de salto, acompanhada por dois fogos de artifício no alto do telhado. Músicas acompanham menu, fase e Game Over; efeitos sonoros acompanham pulo, ataques, chute, dano, acerto em inimigo e coleta de item.")
    add_image_triplet(doc, [
        (SHOTS / "gameplay.png", "Fase em andamento"),
        (SHOTS / "bonus.png", "Bônus de vida"),
        (SHOTS / "trophy.png", "Troféu após derrotar o chefe"),
    ])

    # Página 6 — página itch.io e endereços
    doc.add_page_break()
    add_heading(doc, "6. PÁGINA DO JOGO E DISTRIBUIÇÃO")
    add_label(doc, "Título da página")
    p = doc.add_paragraph()
    p.add_run("As aventuras de um jogador").bold = True
    add_label(doc, "Texto sugerido para itch.io")
    doc.add_paragraph("Uma partida inteira separa você do estádio! Corra, pule, use a cabeçada e o carrinho, e chute bolas para abrir caminho. Desvie dos cartões do juiz, fuja do goleiro que salta em sua direção e enfrente o chefão Cartão Vermelho. Recolha corações e bolas, sobreviva ao percurso e entre em campo.")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.add_run("Jogo individual de plataforma 2D para computador. Escolha a versão para Windows para baixar ou jogue a versão Web diretamente no navegador.")
    doc.add_heading("Materiais e publicação", level=2)
    add_bullet(doc, "Telas descritas: menu inicial, controles, configurações de volume, pausa, fase, derrota e vitória.")
    add_bullet(doc, "Pacotes preparados: versão Web em HTML5 para o itch.io e versão executável para Windows.")
    add_bullet(doc, "A página do jogo no itch.io ainda aguarda publicação. O código-fonte está disponível no repositório GitHub indicado nesta seção.")
    doc.add_heading("7. REFERÊNCIAS E ENDEREÇOS", level=2)
    fields = [
        ("URL da página do jogo no itch.io", "[Preencher após publicar]"),
        ("URL do código-fonte / repositório", REPO_URL + " (privado; solicitar acesso para visualizar)"),
        ("Imagens e recursos", "Arte, áudio, interface e código originais do projeto; engine Godot 4.7.2."),
    ]
    for label, value in fields:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(label + ": ")
        r.bold = True
        if label == "URL do código-fonte / repositório":
            add_hyperlink(p, REPO_URL, REPO_URL)
            p.add_run(" (privado; solicitar acesso para visualizar)")
        else:
            p.add_run(value)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    r = p.add_run("Estado da entrega")
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(BLUE)
    doc.add_paragraph("Projeto preparado para revisão acadêmica. O link do código-fonte está informado acima; o endereço do itch.io será incluído após a publicação.")

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
