# -*- coding: utf-8 -*-
"""Generiše PowerPoint prezentaciju o Velimiru Bati Živojinoviću (sa slikama)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
import os

SLIKE = "/home/user/sumski_kutak/slike"

# --- Paleta boja ---
TAMNO_CRVENA = RGBColor(0x7A, 0x12, 0x12)
CRVENA = RGBColor(0xB0, 0x1E, 0x1E)
ZLATNA = RGBColor(0xC9, 0xA2, 0x27)
TAMNA = RGBColor(0x1A, 0x1A, 0x1A)
SIVA = RGBColor(0x3D, 0x3D, 0x3D)
SVETLA = RGBColor(0xF4, 0xF1, 0xEA)
BELA = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def dodaj_pozadinu(slide, boja):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = boja


def dodaj_traku(slide, top, height, boja, left=0, width=None):
    sh = slide.shapes.add_shape(1, left, top, width if width else SW, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = boja
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def txt(slide, left, top, width, height, text, size, boja, bold=False,
        align=PP_ALIGN.LEFT, font="Calibri", italic=False, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = boja
    r.font.name = font
    return tb


def bullets(slide, left, top, width, height, stavke, size=18, boja=TAMNA,
            razmak=10, font="Calibri", bullet_boja=CRVENA):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (tekst, nivo) in enumerate(stavke):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = nivo
        p.space_after = Pt(razmak)
        p.space_before = Pt(0)
        oznaka = "•  " if nivo == 0 else "–  "
        r1 = p.add_run()
        r1.text = oznaka
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = bullet_boja if nivo == 0 else ZLATNA
        r1.font.name = font
        r2 = p.add_run()
        r2.text = tekst
        r2.font.size = Pt(size) if nivo == 0 else Pt(size - 2)
        r2.font.color.rgb = boja
        r2.font.name = font
    return tb


def slika_cover(slide, ime, left, top, width, height, border=True):
    """Ubacuje sliku tako da popuni okvir (cover), sa zlatnim ramom."""
    path = os.path.join(SLIKE, ime)
    iw, ih = Image.open(path).size
    target = width / height
    src = iw / ih
    pic = slide.shapes.add_picture(path, left, top, width, height)
    if src > target:
        c = (1 - target / src) / 2
        pic.crop_left = c
        pic.crop_right = c
    else:
        c = (1 - src / target) / 2
        pic.crop_top = c
        pic.crop_bottom = c
    if border:
        pic.line.color.rgb = ZLATNA
        pic.line.width = Pt(3)
    return pic


def potpis(slide, left, top, width, tekst):
    tb = txt(slide, left, top, width, Inches(0.3), tekst, 9, SIVA,
             align=PP_ALIGN.CENTER, italic=True)
    return tb


def naslov_slajda(slide, broj, naslov):
    dodaj_traku(slide, 0, Inches(1.25), TAMNO_CRVENA)
    dodaj_traku(slide, Inches(1.25), Emu(60000), ZLATNA)
    txt(slide, Inches(0.4), Inches(0.18), Inches(0.9), Inches(0.9),
        str(broj).zfill(2), 30, ZLATNA, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(slide, Inches(1.35), Inches(0.18), Inches(11.4), Inches(0.9),
        naslov, 30, BELA, bold=True, anchor=MSO_ANCHOR.MIDDLE)


# ============================================================
# SLAJD 1 — Naslovna
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, TAMNA)
dodaj_traku(s, 0, Inches(0.35), CRVENA)
dodaj_traku(s, SH - Inches(0.35), Inches(0.35), CRVENA)
# portret desno
slika_cover(s, "bata1.jpg", Inches(8.7), Inches(1.15), Inches(3.9), Inches(5.2))
txt(s, Inches(0.7), Inches(0.95), Inches(7.7), Inches(0.6),
    "MATURSKA / SEMINARSKA PREZENTACIJA", 15, ZLATNA, bold=True)
dodaj_traku(s, Inches(2.2), Emu(50000), ZLATNA, left=Inches(0.7), width=Inches(7.5))
txt(s, Inches(0.7), Inches(2.45), Inches(7.7), Inches(2.0),
    "VELIMIR\n„BATA“ ŽIVOJINOVIĆ", 40, BELA, bold=True, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.7), Inches(4.7), Inches(7.7), Inches(1.3),
    "Život i uloge — s posebnim osvrtom na ulogu Gvozdena u filmu „Lepa sela lepo gore“ (1996)",
    19, SVETLA, italic=True)
txt(s, Inches(0.7), Inches(6.4), Inches(7.7), Inches(0.6),
    "1933 — 2016  •  legenda jugoslovenskog i srpskog filma", 14, ZLATNA)

# ============================================================
# SLAJD 2 — Sadržaj
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 2, "Sadržaj prezentacije")
bullets(s, Inches(1.2), Inches(1.7), Inches(11), Inches(5.4), [
    ("Ko je bio Bata Živojinović?", 0),
    ("Detinjstvo, mladost i školovanje", 0),
    ("Filmska karijera i najpoznatije uloge", 0),
    ("Televizijske uloge", 0),
    ("Politički angažman", 0),
    ("Film „Lepa sela lepo gore“ — o čemu se radi", 0),
    ("Uloga Gvozdena — analiza lika", 0),
    ("Značaj uloge i poruka filma", 0),
    ("Nagrade, priznanja i nasleđe", 0),
    ("Zaključak", 0),
], size=20, razmak=11)

# ============================================================
# SLAJD 3 — Ko je bio
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 3, "Ko je bio Bata Živojinović?")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.3), Inches(5.4), [
    ("Jedan od najpoznatijih i najplodnijih glumaca u istoriji jugoslovenskog i srpskog filma.", 0),
    ("Tokom karijere igrao je u više od 300 filmova i televizijskih ostvarenja.", 0),
    ("Postao je prepoznatljiv kao simbol „partizanskih“ ratnih filmova i otelotvorenje narodnog junaka.", 0),
    ("Voljen kod publike zbog topline, autentičnosti i snažne ekranske pojave.", 0),
    ("U drugom delu života bavio se i politikom.", 0),
], size=18, razmak=11)
dodaj_traku(s, Inches(1.7), Inches(2.55), TAMNO_CRVENA, left=Inches(8.3), width=Inches(4.5))
txt(s, Inches(8.55), Inches(1.9), Inches(4.0), Inches(0.5),
    "LIČNA KARTA", 17, ZLATNA, bold=True)
bullets(s, Inches(8.55), Inches(2.5), Inches(4.0), Inches(1.8), [
    ("Puno ime: Velimir Živojinović", 0),
    ("Nadimak: Bata", 0),
    ("Rođen: 5. jun 1933, Koraćica", 0),
    ("Preminuo: 22. maj 2016, Beograd", 0),
], size=13, boja=BELA, razmak=8, bullet_boja=ZLATNA)
slika_cover(s, "bata2.jpg", Inches(8.3), Inches(4.45), Inches(4.5), Inches(2.5))

# ============================================================
# SLAJD 4 — Detinjstvo i školovanje
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 4, "Detinjstvo, mladost i školovanje")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.4), Inches(5.4), [
    ("Rođen je 5. juna 1933. u selu Koraćica, u podnožju planine Kosmaj, blizu Mladenovca.", 0),
    ("Detinjstvo je proveo u skromnim, seoskim uslovima, što je kasnije uticalo na njegove „narodne“ uloge.", 0),
    ("Ljubav prema glumi otkrio je još u mladosti.", 0),
    ("Diplomirao je na Akademiji za pozorišnu umetnost u Beogradu.", 0),
    ("Karijeru je započeo u pozorištu, a ubrzo prešao na film, gde je stekao najveću slavu.", 0),
], size=18, razmak=12)
slika_cover(s, "kosmaj.jpg", Inches(8.4), Inches(1.7), Inches(4.4), Inches(4.6))
potpis(s, Inches(8.4), Inches(6.35), Inches(4.4), "Planina Kosmaj, kraj odakle potiče")

# ============================================================
# SLAJD 5 — Filmska karijera
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 5, "Filmska karijera i najpoznatije uloge")
bullets(s, Inches(0.7), Inches(1.65), Inches(7.5), Inches(5.5), [
    ("Najveću popularnost stekao je u partizanskim ratnim filmovima, tumačeći hrabre borce i komandante:", 0),
    ("„Bitka na Neretvi“ (1969)", 1),
    ("„Most“ (1969)", 1),
    ("„Valter brani Sarajevo“ (1972)", 1),
    ("„Sutjeska“ (1973) — uz Ričarda Bartona", 1),
    ("Igrao je i u komedijama, dramama i istorijskim filmovima — veliki glumački raspon.", 0),
    ("Njegova pojava postala je zaštitni znak čitave epohe domaćeg filma.", 0),
], size=17, razmak=8)
slika_cover(s, "bata3.jpg", Inches(8.4), Inches(1.9), Inches(4.4), Inches(4.4))

# ============================================================
# SLAJD 6 — Televizijske uloge
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 6, "Televizijske uloge")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.4), Inches(5.4), [
    ("Pored filma, bio je veoma popularan i na malim ekranima.", 0),
    ("Glumio je u kultnim TV serijama koje su pratile generacije gledalaca:", 0),
    ("„Otpisani“ i „Povratak otpisanih“ — priče o beogradskim ilegalcima u Drugom svetskom ratu.", 1),
    ("Učestvovao je u brojnim TV dramama i serijama tokom decenija.", 0),
    ("Zahvaljujući televiziji, postao je omiljen u svakom domu bivše Jugoslavije.", 0),
], size=18, razmak=12)
slika_cover(s, "bata1.jpg", Inches(8.4), Inches(1.7), Inches(4.4), Inches(4.9))

# ============================================================
# SLAJD 7 — Politika
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 7, "Politički angažman")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.4), Inches(5.4), [
    ("U drugom delu života aktivno se bavio politikom.", 0),
    ("Bio je član Socijalističke partije Srbije (SPS).", 0),
    ("Više puta je biran za narodnog poslanika u Skupštini.", 0),
    ("Ulazak u politiku propraćen je velikom pažnjom javnosti — zbog ogromne popularnosti koju je stekao kao glumac.", 0),
    ("Publika ga je pre svega pamtila kao velikog umetnika.", 0),
], size=18, razmak=12)
slika_cover(s, "skupstina.jpg", Inches(8.4), Inches(2.1), Inches(4.4), Inches(3.0))
potpis(s, Inches(8.4), Inches(5.15), Inches(4.4), "U Skupštini Srbije (1990-e)")

# ============================================================
# SLAJD 8 — O filmu Lepa sela lepo gore
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 8, "Film „Lepa sela lepo gore“ (1996)")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.5), Inches(5.4), [
    ("Reditelj: Srđan Dragojević.", 0),
    ("Jedan od najznačajnijih i najpotresnijih srpskih filmova o ratu u Bosni (1992–1995).", 0),
    ("Radnja prati grupu srpskih boraca zarobljenih u tunelu, okruženih neprijateljskim snagama.", 0),
    ("Kroz potresne scene prikazuje besmisao rata i raspad nekadašnjeg „bratstva i jedinstva“.", 0),
    ("Antiratni film — ne slavi rat, već pokazuje njegovu tragediju i ljudsku patnju.", 0),
], size=18, razmak=11)
dodaj_traku(s, Inches(1.7), Inches(5.1), TAMNO_CRVENA, left=Inches(8.45), width=Inches(4.35))
txt(s, Inches(8.7), Inches(1.95), Inches(3.85), Inches(0.6),
    "ZANIMLJIVO", 17, ZLATNA, bold=True)
bullets(s, Inches(8.7), Inches(2.7), Inches(3.9), Inches(4.0), [
    ("Tunel je simbol — bezizlazna situacija i zarobljenost u mržnji rata.", 0),
    ("Film je dobio brojne nagrade i prikazivan je širom sveta.", 0),
    ("Naziv potiče iz crnog humora kojim se borci brane od strave rata.", 0),
], size=14, boja=BELA, razmak=12, bullet_boja=ZLATNA)

# ============================================================
# SLAJD 9 — Uloga Gvozdena
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 9, "Uloga Gvozdena — analiza lika")
bullets(s, Inches(0.7), Inches(1.65), Inches(7.5), Inches(5.5), [
    ("Bata Živojinović tumači Gvozdena — starijeg, iskusnog borca među zarobljenim vojnicima.", 0),
    ("Gvozden je nekadašnji radnik koji je iskreno verovao u ideale „bratstva i jedinstva“ socijalističke Jugoslavije.", 0),
    ("Predstavlja stariju generaciju — onu koja je gradila zajedničku zemlju i ne može da prihvati da se ona ruši u krvi.", 0),
    ("Kako rat odmiče, sve više gubi nadu i razočaran je u sve oko sebe.", 0),
    ("Tragičan lik — simbol sloma jednog sistema vrednosti i jedne epohe.", 0),
    ("U trenutku potpunog očaja donosi sudbonosnu, samoubilačku odluku — jedna od najupečatljivijih scena filma.", 0),
], size=17, razmak=9)
slika_cover(s, "bata3.jpg", Inches(8.4), Inches(1.9), Inches(4.4), Inches(4.4))
potpis(s, Inches(8.4), Inches(6.35), Inches(4.4), "Bata Živojinović — legenda domaćeg glumišta")

# ============================================================
# SLAJD 10 — Značaj uloge
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 10, "Značaj uloge i poruka filma")
bullets(s, Inches(1.0), Inches(1.7), Inches(11.3), Inches(5.4), [
    ("Uloga Gvozdena je posebno značajna jer Batu Živojinovića vidimo u potpuno novom svetlu.", 0),
    ("Glumac koji je decenijama bio simbol partizanskih, pobedničkih junaka, sada igra slomljenog, razočaranog čoveka.", 0),
    ("Stvara se snažan kontrast: nekadašnji „heroj bratstva i jedinstva“ suočava se sa raspadom svega u šta je verovao.", 0),
    ("Poruka filma kroz Gvozdena: rat uništava ne samo živote, već i ideale i ljudskost.", 0),
    ("Njegova uloga gledaocu prenosi tugu, gubitak i besmislenost sukoba.", 0),
], size=19, razmak=13)

# ============================================================
# SLAJD 11 — Nagrade i nasleđe
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, SVETLA)
naslov_slajda(s, 11, "Nagrade, priznanja i nasleđe")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.3), Inches(5.4), [
    ("Osvojio je brojne nagrade, među kojima i prestižne Zlatne arene na festivalu u Puli.", 0),
    ("Dobitnik je priznanja za životno delo i mnogih drugih umetničkih nagrada.", 0),
    ("Smatra se jednim od najvećih glumaca ovih prostora svih vremena.", 0),
    ("Preminuo je 22. maja 2016. u Beogradu, u 83. godini.", 0),
    ("Njemu u čast izdata je i poštanska marka; filmovi mu se i danas rado gledaju.", 0),
], size=18, razmak=11)
slika_cover(s, "pula.jpg", Inches(8.4), Inches(1.75), Inches(4.4), Inches(2.55))
potpis(s, Inches(8.4), Inches(4.32), Inches(4.4), "Arena u Puli — dom filmskog festivala")
slika_cover(s, "marka.jpg", Inches(8.4), Inches(4.75), Inches(4.4), Inches(2.1))
potpis(s, Inches(8.4), Inches(6.88), Inches(4.4), "Poštanska marka Srbije (2023)")

# ============================================================
# SLAJD 12 — Zaključak
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, TAMNA)
dodaj_traku(s, 0, Inches(0.35), CRVENA)
dodaj_traku(s, SH - Inches(0.35), Inches(0.35), CRVENA)
txt(s, Inches(1), Inches(0.9), Inches(11.3), Inches(0.9),
    "ZAKLJUČAK", 36, ZLATNA, bold=True, align=PP_ALIGN.CENTER)
bullets(s, Inches(1.6), Inches(2.2), Inches(10.1), Inches(4.0), [
    ("Bata Živojinović je svojim talentom i radom obeležio čitavu epohu domaćeg filma.", 0),
    ("Od hrabrih partizanskih junaka do tragičnog Gvozdena, pokazao je izuzetan glumački raspon.", 0),
    ("Uloga u filmu „Lepa sela lepo gore“ potvrdila je njegovu veličinu i u ozbiljnim, antiratnim ostvarenjima.", 0),
    ("Ostaje upamćen kao legenda i jedan od najvoljenijih glumaca naših prostora.", 0),
], size=20, boja=SVETLA, razmak=16, bullet_boja=ZLATNA)

# ============================================================
# SLAJD 13 — Hvala / Izvori
# ============================================================
s = prs.slides.add_slide(BLANK)
dodaj_pozadinu(s, TAMNO_CRVENA)
dodaj_traku(s, Inches(2.7), Emu(50000), ZLATNA, left=Inches(2.5), width=Inches(8.3))
txt(s, Inches(1), Inches(1.9), Inches(11.3), Inches(1.2),
    "HVALA NA PAŽNJI!", 44, BELA, bold=True, align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1), Inches(3.1), Inches(11.3), Inches(0.7),
    "Pitanja i diskusija dobrodošli", 20, ZLATNA, align=PP_ALIGN.CENTER, italic=True)
txt(s, Inches(1), Inches(4.4), Inches(11.3), Inches(0.5),
    "Izvori teksta:", 15, ZLATNA, align=PP_ALIGN.CENTER, bold=True)
txt(s, Inches(1.5), Inches(4.8), Inches(10.3), Inches(0.5),
    "Wikipedia i dostupni filmski i biografski materijali", 13, SVETLA,
    align=PP_ALIGN.CENTER)
txt(s, Inches(1), Inches(5.5), Inches(11.3), Inches(0.5),
    "Fotografije:", 15, ZLATNA, align=PP_ALIGN.CENTER, bold=True)
txt(s, Inches(1.2), Inches(5.9), Inches(10.9), Inches(1.0),
    "Wikimedia Commons — portreti i fotografija iz Skupštine: Medija centar Beograd / "
    "Stevan Kragujević (CC BY-SA 3.0); Kosmaj i Arena u Puli (CC BY-SA); "
    "poštanska marka: Pošta Srbije (javno vlasništvo).",
    11, SVETLA, align=PP_ALIGN.CENTER)

prs.save("/home/user/sumski_kutak/Bata_Zivojinovic_prezentacija.pptx")
print("Sačuvano. Broj slajdova:", len(prs.slides._sldIdLst))
