from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SHOTS = DOCS / "screenshots"
OUT = DOCS / "Projeto_de_Sistemas_Interativos.pdf"
REPO_URL = "https://github.com/erik336pereira/da-rua-ao-estrelado"
ITCH_URL = "https://erik336.itch.io/da-rua-ao-estrelado"
NAVY = colors.HexColor("#15345B")
BLUE = colors.HexColor("#168CC8")
GOLD = colors.HexColor("#F2BD42")
INK = colors.HexColor("#263447")
MUTED = colors.HexColor("#617080")
PALE = colors.HexColor("#EAF5FA")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name="CoverSmall", parent=styles["Normal"], fontName="Helvetica", fontSize=11, leading=16, textColor=MUTED, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=NAVY, spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle(name="Subhead", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=BLUE, spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="Label", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=BLUE, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="Bullet2", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.8, leading=11.5, textColor=INK, leftIndent=13, firstLineIndent=-9, spaceAfter=2))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name="TableText", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK))
styles.add(ParagraphStyle(name="Center", parent=styles["BodyText"], fontName="Helvetica", fontSize=10, leading=14, textColor=INK, alignment=TA_CENTER))


def P(text, style="Body2"):
    return Paragraph(text, styles[style])


def add_bullet(story, text):
    story.append(P("• &nbsp;" + text, "Bullet2"))


def screenshot_pair(a, caption_a, b, caption_b, width=3.15):
    cells = []
    for path, caption in ((a, caption_a), (b, caption_b)):
        img = Image(str(path), width=width * inch, height=1.77 * inch, kind="proportional")
        cells.append([img, P(caption, "Small")])
    table = Table([cells], colWidths=[3.32 * inch, 3.32 * inch], hAlign="CENTER")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return table


def screenshot_triplet(entries):
    cells = []
    for path, caption in entries:
        img = Image(str(path), width=2.06 * inch, height=1.16 * inch, kind="proportional")
        cells.append([img, P(caption, "Small")])
    table = Table([cells], colWidths=[2.2 * inch] * 3, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(colors.HexColor("#D6E3EB"))
    canvas.setLineWidth(0.6)
    canvas.line(0.72 * inch, h - 0.42 * inch, w - 0.72 * inch, h - 0.42 * inch)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.72 * inch, h - 0.32 * inch, "PROJETO DE EXTENSÃO EM SISTEMAS INTERATIVOS")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(w - 0.72 * inch, 0.34 * inch, f"DA RUA AO ESTRELADO  •  {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, rightMargin=0.72 * inch, leftMargin=0.72 * inch,
        topMargin=0.58 * inch, bottomMargin=0.58 * inch,
        title="Projeto de Extensão em Sistemas Interativos — Da Rua ao Estrelado",
        author="Projeto de Extensão em Sistemas Interativos",
    )
    story = []

    # Página 1 — capa
    story += [Spacer(1, 0.3 * inch), P("UNIVERSIDADE NOVE DE JULHO — UNINOVE", "CoverSmall"),
              P("DIRETORIA DOS CURSOS DE INFORMÁTICA", "CoverSmall"), Spacer(1, 0.12 * inch),
              P("PROJETO DE EXTENSÃO EM SISTEMAS INTERATIVOS", "Label"), Spacer(1, 0.4 * inch),
              P("DA RUA AO<br/>ESTRELADO", "DocTitle"),
              P("Jogo de plataforma 2D com tema de futebol", "CoverSmall"), Spacer(1, 0.25 * inch)]
    story.append(Image(str(SHOTS / "gameplay.png"), width=5.95 * inch, height=3.35 * inch, kind="proportional"))
    story += [P("Cena da fase — arte original em pixel art.", "Small"), Spacer(1, 0.65 * inch),
              P("SÃO PAULO<br/>2026", "Center")]

    # Página 2 — folha de rosto e integrantes
    story += [PageBreak(), Spacer(1, 0.15 * inch), P("DA RUA AO ESTRELADO", "Section"),
              Spacer(1, 0.3 * inch), P("Projeto desenvolvido na disciplina Projeto de Extensão em Sistemas Interativos, como jogo de plataforma 2D para computador com a engine Godot.", "Center"),
              Spacer(1, 0.25 * inch), P("INTEGRANTES DO GRUPO", "Label")]
    members = [
        ("Erik Pereira de Almeida — Líder", "924115897"),
        ("Felipe Gabriel Cruz Medeiros", "924100952"),
        ("Letícia da Silva Oliveira", "924103216"),
        ("Gabriel Santos de Jesus", "924110011"),
        ("Marcos Daniel Ribeiro Siriano", "924115034"),
    ]
    rows = [[P(f"{number:02d}. {name}   —   RA: {ra}", "TableText")]
            for number, (name, ra) in enumerate(members, 1)]
    roster = Table(rows, colWidths=[6.64 * inch], rowHeights=[0.38 * inch] * len(members))
    roster.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C7DAE5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [roster, Spacer(1, 0.2 * inch), P("ORIENTAÇÃO E DISCIPLINA", "Label"),
              P("<b>Professor:</b> Leandro Fernandes da Mota<br/><b>Disciplina:</b> Projeto de Extensão em Sistemas Interativos", "Body2"),
              Spacer(1, 0.42 * inch), P("São Paulo<br/>2026", "Center")]

    # Página 3 — sumário
    story += [PageBreak(), P("SUMÁRIO", "Section"), P("Estrutura do projeto e das entregas.", "Small"), Spacer(1, 0.15 * inch)]
    toc = [
        ("1. Objetivo e proposta", "4"), ("2. História e ambientação", "4"),
        ("3. Recursos, personagens e cenários", "4"), ("4. Jogabilidade, controles e desafios", "5"),
        ("5. Telas e áudio", "5"), ("6. Página do jogo e distribuição", "6"),
        ("7. Referências e endereços", "6"),
    ]
    toc_rows = [[P(t, "Body2"), P(p, "Body2")] for t, p in toc]
    toc_table = Table(toc_rows, colWidths=[5.85 * inch, 0.5 * inch], rowHeights=[0.43 * inch] * len(toc))
    toc_table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, colors.HexColor("#D6E3EB")),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [toc_table, Spacer(1, 0.55 * inch), P("PLATAFORMA", "Label"),
              P("Computador (Windows) e navegador compatível com a exportação Web de Godot. Jogo individual; não há modo multijogador.", "Body2"),
              Spacer(1, 0.15 * inch), P("TECNOLOGIA", "Label"),
              P("Godot 4.7.2, GDScript, recursos gráficos e áudio originais preparados para o projeto.", "Body2")]

    # Página 4 — objetivo, narrativa, arte
    story += [PageBreak(), P("1. OBJETIVO E PROPOSTA", "Section"),
              P("Desenvolver um jogo de plataforma 2D no qual o jogador atravessa um percurso inspirado no futebol, enfrenta adversários e alcança o estádio. O projeto prioriza controles de teclado, leitura clara dos perigos, coleta de recursos e uma conclusão após a luta contra um chefe.", "Body2"),
              P("2. HISTÓRIA E AMBIENTAÇÃO", "Subhead"),
              P("Um jovem jogador está a caminho de sua grande partida. Para chegar ao estádio, ele precisa cruzar ruas e áreas de acesso tomadas por desafios futebolísticos: o juiz lança cartões, o goleiro sai do gol para persegui-lo, a torcida atrapalha o caminho e um enorme Cartão Vermelho protege o portão final. Vencido o chefe, os portões se abrem e o atleta pode entrar no estádio, enquanto a frase ‘PORTÕES ABERTOS!’ salta suavemente acima da estrutura e dois fogos explodem sobre o telhado.", "Body2"),
              P("3. RECURSOS, PERSONAGENS E CENÁRIOS", "Subhead"),
              P("A direção visual usa pixel art original com paleta azul, verde e terrosa. Os sprites têm quadros de movimento para corrida, cabeçada, carrinho e chute. O cenário combina céu em camadas, prédios, plataformas, gramado, terra e estádio; corações recuperam vida, bolas ampliam a munição e um troféu rende pontos após a derrota do chefe.", "Body2")]
    story.append(Image(str(DOCS / "assets" / "personagens.png"), width=6.65 * inch, height=1.57 * inch, kind="proportional"))
    story += [P("Personagens originais: jogador, juiz, goleiro/VAR, torcedor e chefe Cartão Vermelho.", "Small"),
              screenshot_pair(SHOTS / "gameplay.png", "Trecho da fase", SHOTS / "headbutt.png", "Sequência da cabeçada", width=3.12),
              screenshot_pair(SHOTS / "kick.png", "Chute com preparação, contato e recuperação", SHOTS / "trophy.png", "Troféu na plataforma após derrotar o chefe", width=3.12)]

    # Página 5 — controles, inimigos e telas
    story += [PageBreak(), P("4. JOGABILIDADE, CONTROLES E DESAFIOS", "Section")]
    control_data = [[P("AÇÃO", "TableHead"), P("TECLA / EFEITO", "TableHead")]]
    controls = [
        ("Mover", "A / D ou setas esquerda/direita"), ("Pular", "Espaço, W ou seta para cima"),
        ("Cabeçada", "J — ataque de curta distância"), ("Carrinho", "K — investida rasteira"),
        ("Chute", "L — arremessa uma bola consumível"), ("Pausar / voltar", "P ou Esc"),
        ("Iniciar / continuar", "Enter; Espaço também inicia na tela de título"),
        ("Reiniciar durante a pausa", "R"),
    ]
    control_data += [[P(a, "TableText"), P(k, "TableText")] for a, k in controls]
    control_table = Table(control_data, colWidths=[1.8 * inch, 4.8 * inch], rowHeights=[0.28 * inch] + [0.3 * inch] * len(controls))
    control_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C7DAE5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [control_table, P("Adversários e recursos", "Subhead")]
    for text in [
        "Juiz: patrulha e lança cartões amarelos; contato e projéteis causam dano.",
        "Goleiro/VAR: persegue o jogador, pula para alcançar plataformas e tenta colidir com ele.",
        "Torcedor: ocupa a rota e se movimenta pelo trecho em que aparece.",
        "Chefe Cartão Vermelho: cartão vermelho vivo, retangular, com braços e pernas. Arremessa cartões à distância e golpeia de perto; é preciso derrotá-lo para abrir o portão.",
        "O HUD acompanha vidas, bolas e pontuação. Corações restauram vida; bolas recuperam munição. A breve invulnerabilidade após dano evita golpes instantâneos consecutivos.",
    ]:
        add_bullet(story, text)
    story += [P("5. TELAS E ÁUDIO", "Subhead"),
              P("O menu inicial concentra o botão de começar e acessos separados para Configurações e Controles. Na pausa, o jogador pode continuar, abrir essas telas ou reiniciar. Configurações oferece um controle deslizante de volume de 0% a 100%, ajustável com clique ou arraste. A tela de Controles reúne as teclas de movimento, pulo, ataques, pausa e reinício. Na vitória e na derrota, é possível iniciar um novo jogo ou voltar ao menu principal. Depois que o chefe é derrotado, ‘PORTÕES ABERTOS!’ aparece acima do estádio com uma animação leve de salto, acompanhada por dois fogos de artifício no alto do telhado. Músicas acompanham menu, fase e Game Over; efeitos sonoros acompanham pulo, ataques, chute, dano, acerto em inimigo e coleta de item.", "Body2"),
              screenshot_triplet([
                  (SHOTS / "gameplay.png", "Fase em andamento"),
                  (SHOTS / "bonus.png", "Bônus de vida"),
                  (SHOTS / "trophy.png", "Troféu após derrotar o chefe"),
              ])]

    # Página 6 — publicação e endereços editáveis
    story += [PageBreak(), P("6. PÁGINA DO JOGO E DISTRIBUIÇÃO", "Section"), P("TÍTULO DA PÁGINA", "Label"),
              P("<b>Da Rua ao Estrelado</b>", "Body2"), P("TEXTO SUGERIDO PARA ITCH.IO", "Label"),
              P("Uma partida inteira separa você do estádio! Corra, pule, use a cabeçada e o carrinho, e chute bolas para abrir caminho. Desvie dos cartões do juiz, fuja do goleiro que salta em sua direção e enfrente o chefão Cartão Vermelho. Recolha corações e bolas, sobreviva ao percurso e entre em campo.", "Body2"),
              P("Jogo individual de plataforma 2D para computador. Escolha a versão para Windows para baixar ou jogue a versão Web diretamente no navegador.", "Body2"),
              P("MATERIAIS E PUBLICAÇÃO", "Subhead")]
    for text in [
        "Telas descritas: menu inicial, controles, configurações de volume, pausa, fase, derrota e vitória.",
        "Pacotes preparados: versão Web em HTML5 para o itch.io e versão executável para Windows.",
        "O jogo está publicado no itch.io e pode ser acessado pelo endereço informado nesta seção. O código-fonte está disponível publicamente no GitHub pelo endereço indicado abaixo.",
    ]:
        add_bullet(story, text)
    story += [P("7. REFERÊNCIAS E ENDEREÇOS", "Subhead")]
    refs = [
        ("URL da página do jogo no itch.io", f'<link href="{ITCH_URL}" color="#168CC8">{ITCH_URL}</link>'),
        ("URL do código-fonte / repositório", f'<link href="{REPO_URL}" color="#168CC8">{REPO_URL}</link>'),
        ("Imagens e recursos", "Arte, áudio, interface e código originais; engine Godot 4.7.2."),
    ]
    for label, value in refs:
        story.append(P(f"<b>{label}:</b> {value}", "Body2"))
    story += [Spacer(1, 0.12 * inch), P("ESTADO DA ENTREGA", "Label"),
              P("Projeto publicado no itch.io e com código-fonte público no GitHub. Os dois endereços estão informados acima.", "Body2")]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    build()
