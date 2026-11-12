from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

out = Path(__file__).with_name("Guia_Tecnico_Avantio_Fotos_Gestor_em_Lote.docx")

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.7)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.8)
sec.right_margin = Inches(0.8)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10.5)
styles["Normal"].paragraph_format.space_after = Pt(5)
styles["Normal"].paragraph_format.line_spacing = 1.08
styles["Title"].font.name = "Aptos Display"
styles["Title"].font.size = Pt(25)
styles["Title"].font.bold = True
styles["Title"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 1"].font.name = "Aptos Display"
styles["Heading 1"].font.size = Pt(16)
styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 1"].paragraph_format.space_before = Pt(13)
styles["Heading 1"].paragraph_format.space_after = Pt(5)
styles["Heading 1"].paragraph_format.keep_with_next = True
styles["Heading 2"].font.name = "Aptos Display"
styles["Heading 2"].font.size = Pt(12.5)
styles["Heading 2"].font.color.rgb = RGBColor(47, 117, 181)
styles["Heading 2"].paragraph_format.keep_with_next = True


def add_code_block(text, font_size=9.5):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.15)
    paragraph.paragraph_format.right_indent = Inches(0.1)
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1.0
    p_pr = paragraph._p.get_or_add_pPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), "F2F5F8")
    p_pr.append(shading)
    run = paragraph.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(font_size)
    return paragraph

title = doc.add_heading("Avantio Fotos — Gestor em lote", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p = doc.add_paragraph("Guia técnico de referência • HTML/DevTools confirmados • atualizado em 16/10/2026")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.runs[0].font.size = Pt(10)
p.runs[0].font.color.rgb = RGBColor(100, 100, 100)

doc.add_paragraph(
    "Objetivo: documentar os seletores, IDs, eventos e regras descobertos na interface de edição de fotografias do Avantio, "
    "para retomar o projeto noutra conversa sem voltar a recolher os mesmos dados."
)

doc.add_heading("1. Estado do projeto", level=1)
for item in [
    "A estrutura principal dos campos foi identificada.",
    "Os IDs das categorias de fotografia foram recolhidos.",
    "O comportamento do componente de traduções CRSMI18N foi lido no código-fonte.",
    "A validação e o botão de guardar foram identificados.",
    "A correspondência entre cada foto do JSON/MTPhomes e a fotografia correta na galeria Avantio ainda NÃO foi implementada nem testada.",
    "Ainda não foi validado que os valores persistem após guardar. Não executar alterações em lote antes de um teste controlado com uma única foto.",
]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("2. Categoria da fotografia", level=1)
doc.add_paragraph('Seletor: select#selectTipos[name="SelectTipos"]')
doc.add_paragraph("O seletor tem a classe width100. O valor atual observado no HTML de exemplo era 0.")
categories = [
    ("0", "--Nenhum--"), ("14", "Balcão"), ("16", "Cafeteria"),
    ("20", "Child's bedroom"), ("1", "Cozinha"), ("10", "Detalhes"),
    ("9", "Exterior"), ("2", "Fachada"), ("8", "Garagem"), ("5", "Jardim"),
    ("11", "Outros"), ("6", "Piscina"), ("18", "Plano"), ("4", "Quarto de banho"),
    ("3", "Quarto de cama"), ("13", "Receção"), ("19", "Resort"),
    ("12", "Sala de estar"), ("15", "Sala de jantar"), ("7", "Terraço"),
    ("17", "Visualizações"),
]
table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = "Light Shading Accent 1"
table.rows[0].cells[0].text = "ID/value"
table.rows[0].cells[1].text = "Categoria"
for val, name in categories:
    cells = table.add_row().cells
    cells[0].text = val
    cells[1].text = name
for row in table.rows:
    for cell in row.cells:
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for paragraph in cell.paragraphs:
            paragraph.paragraph_format.space_after = Pt(2)
            for run in paragraph.runs:
                run.font.size = Pt(9.5)

doc.add_heading("3. Acessibilidade", level=1)
doc.add_paragraph('Seletor: input#checkbox_accessibility[name="checkbox_accessibility"]')
doc.add_paragraph('HTML observado: type="checkbox", class="ios-toggle checkBoxIos", value="false", checked=false.')
doc.add_paragraph("O checkbox tem onclick=\"toggleCheckboxAccessibility()\".")
doc.add_paragraph("Função confirmada:")
add_code_block(
    "function toggleCheckboxAccessibility() {\n"
    "    checkbox = $('#checkbox_accessibility').val();\n"
    "    $('#checkbox_accessibility').val(checkbox === 'true' ? 'false' : 'true');\n"
    "    $('#accessibilityWarning').toggle();\n"
    "    $('#accessibilitySelector').toggle();\n"
    "}"
)
doc.add_paragraph(
    "Importante: a função alterna o atributo value e mostra/esconde #accessibilityWarning e #accessibilitySelector. "
    "O projeto assume que a acessibilidade deve ficar desativada para as fotografias, salvo instrução explícita em contrário. "
    "Não alternar o checkbox cegamente; comparar primeiro o estado pretendido com o estado atual e respeitar o comportamento da interface."
)

doc.add_heading("4. Idiomas e campos SEO", level=1)
doc.add_paragraph("IDs de idioma Avantio confirmados:")
for item in ["Português (PT) = 10", "Espanhol (ES) = 1", "Inglês (UK) = 2", "Francês = 5"]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("4.1 Padrão dos names", level=2)
for item in [
    'i18n[easytour_descripciones][ID_FOTO][ID_IDIOMA][title]',
    'i18n[easytour_descripciones][ID_FOTO][ID_IDIOMA][descripcion]',
    'i18n[easytour_descripciones][ID_FOTO][ID_IDIOMA][alt]',
]:
    add_code_block(item)
doc.add_paragraph("ID_FOTO é dinâmico: não usar o ID 127586536 como constante. Esse ID era apenas o exemplo no HTML fornecido.")

for label, visible, translated, limit in [
    (
        "Título",
        "#i18n_easytour_descripciones_title_ID_FOTO_10",
        "#i18n_easytour_descripciones_title_ID_FOTO_ID_IDIOMA_hiddenField",
        "70 caracteres",
    ),
    (
        "Descrição",
        "#i18n_easytour_descripciones_descripcion_ID_FOTO_10",
        "#i18n_easytour_descripciones_descripcion_ID_FOTO_ID_IDIOMA_hiddenField",
        "Não identificado",
    ),
    (
        "Alt",
        "#i18n_easytour_descripciones_alt_ID_FOTO_10",
        "#i18n_easytour_descripciones_alt_ID_FOTO_ID_IDIOMA_hiddenField",
        "125 caracteres",
    ),
]:
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run(f"{label} — limite: {limit}")
    run.bold = True
    doc.add_paragraph("Campo visível em português (PT):")
    add_code_block(visible)
    doc.add_paragraph("Campo oculto de tradução (substituir ID_FOTO e ID_IDIOMA):")
    add_code_block(translated)
doc.add_paragraph("Classes:")
for item in [
    "Título: .seoTitleI18N .seoI18N (input)",
    "Descrição: .seoDesc18N .seoI18N (textarea)",
    "Alt: .seoAltI18N .seoI18N (input)",
]:
    doc.add_paragraph(item, style="List Bullet")
doc.add_paragraph(
    "Os campos visíveis de PT e os campos ocultos de tradução podem ter o mesmo atributo name mas IDs diferentes. "
    "Não preencher indiscriminadamente todos os elementos pelo mesmo name."
)

doc.add_heading("5. Componente CRSMI18N e botão Aceitar", level=1)
doc.add_paragraph("Ficheiro encontrado: CRSMI18N.js?v=7.2.4.7")
for item in [
    "setUpEvents(): liga o clique do campo/ícone de tradução a startModal().",
    "startModal(): abre a janela e foca o campo principal oculto.",
    "showModal(): guarda uma cópia dos valores existentes, move os campos de tradução para a janela e liga os botões.",
    "Aceitar (.i18nAceptarButton): chama validateTranslations(); se válido, fecha a janela.",
    "Cancelar (.i18nCancelButton): fecha a janela e restaura os valores que existiam antes de abrir.",
    "closeModal(): devolve os campos para o contentor oculto e chama saveVisibleElement().",
    "saveVisibleElement(): copia o valor de .i18nMainHiddenField para o campo visível.",
    "updateLanguageHelper(): recalcula o indicador de traduções pendentes depois de aceitar.",
    "Neste campo de descrição, options.required era 'none', pelo que validateTranslations() não exige que todos os idiomas estejam preenchidos.",
]:
    doc.add_paragraph(item, style="List Bullet")
doc.add_paragraph("Seletor do botão Aceitar: .i18nAceptarButton")
doc.add_paragraph("Seletor do botão Cancelar: .i18nCancelButton")
doc.add_paragraph("A janela de exemplo tinha um ID terminado em _modal, por exemplo #i18n_easytour_descripciones_descripcion_127586536_10_modal.")

doc.add_heading("6. Validação e gravação da fotografia", level=1)
doc.add_paragraph("Formulário de edição: #EditView (name=\"EditView\", action hidden com valor \"Save\").")
doc.add_paragraph("Botão Guardar: #editViewSave. O seletor #save não existe no contexto verificado.")
doc.add_paragraph("O botão está associado a este comportamento:")
add_code_block(
    "$('#editViewSave').on('click', function (event) {\n"
    "    if (prep_save() == true) {\n"
    "        var the_form = $('#EditView');\n"
    "        the_form.submit();\n"
    "    }\n"
    "});"
)
doc.add_paragraph("prep_save() verifica se #nombre está vazio. Se estiver vazio, mostra .errorNombreFoto e não submete; se não estiver vazio, permite a submissão.")
doc.add_paragraph("Usar o botão real #editViewSave para respeitar a validação da interface. A submissão ainda precisa de ser verificada: não assumir que os dados persistiram só porque o clique ocorreu.")
doc.add_paragraph("Página de detalhe: form#form; contém module=Fotos, record dinâmico e botão Editar. prep_edit() muda action para EditView. Não usar prep_delete() nem o botão Eliminar.")

doc.add_heading("7. Galeria e identificação de fotos", level=1)
doc.add_paragraph("Elementos observados na galeria:")
for item in [
    "li.imagenGaleria[data-idimg][data-orden]",
    ".editarElementGaleria",
    ".selectImage com atributo data-urlimagedetail",
    ".contentPrincipalImage.urlImagen para a imagem de miniatura (o elemento img pode ser apenas um SVG genérico).",
]:
    doc.add_paragraph(item, style="List Bullet")
doc.add_paragraph(
    "O ID da foto Avantio é dinâmico. Não confiar apenas em numero/ordem do JSON, porque a ordem e o conjunto de fotos de MTPhomes podem diferir da galeria Avantio. "
    "É obrigatório desenvolver e testar a correspondência por URL/conteúdo visual antes de editar."
)

doc.add_heading("8. JSON de entrada esperado", level=1)
json_text = '''{
  "alojamento": "Nome do alojamento",
  "pageId": "ID da página Notion",
  "urlAnuncio": "URL do anúncio de origem",
  "totalFotos": 1,
  "fotos": [
    {
      "numero": 1,
      "url": "URL da foto de origem",
      "nome": "Descrição de referência da imagem",
      "etiqueta": {"nome": "Piscina", "id": 6},
      "acessibilidade": false,
      "descricao": {"pt": "...", "es": "...", "en": "...", "fr": "..."},
      "titulo": {"pt": "...", "es": "...", "en": "...", "fr": "..."},
      "alt": {"pt": "...", "es": "...", "en": "...", "fr": "..."},
      "sucesso": true
    }
  ]
}'''
p = doc.add_paragraph()
add_code_block(json_text, font_size=8.5)
doc.add_paragraph("Não fazer chamadas adicionais ao Groq para reconstruir o conteúdo se o JSON existente puder ser reutilizado.")

doc.add_heading("9. Plano de teste seguro", level=1)
for item in [
    "Criar modo de pré-visualização: mostrar os dados que seriam escritos, sem guardar.",
    "Confirmar manualmente que a foto selecionada no Avantio corresponde à foto do JSON, usando URL e/ou conteúdo visual.",
    "Executar apenas uma foto de teste.",
    "Preencher e aceitar traduções, validar categoria e manter acessibilidade desativada.",
    "Guardar clicando no botão real.",
    "Verificar após a gravação/reabertura que título, descrição, alt, categoria e estado de acessibilidade persistiram.",
    "Só depois de um teste aprovado, implementar o processamento em lote com confirmação explícita e registo dos resultados.",
]:
    doc.add_paragraph(item, style="List Number")

doc.add_heading("10. Dados ainda por confirmar", level=1)
for item in [
    "Correspondência automática entre as fotos do JSON e as fotos reais no Avantio.",
    "Estratégia robusta para abrir a foto certa e obter o ID dinâmico.",
    "Comportamento real de persistência após guardar e método de confirmação do sucesso.",
    "Eventuais eventos específicos do selectTipos ao alterar a categoria (o HTML observado não mostrou onchange).",
]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("11. Como retomar este projeto noutra conversa", level=1)
doc.add_paragraph(
    "Anexar este documento e dizer: “Vamos continuar o projeto Avantio Fotos — Gestor em lote. "
    "Usa este guia técnico como referência, não repitas a recolha dos dados já confirmados e vamos começar pelo modo de teste/preview para uma única foto. "
    "A correspondência JSON ↔ fotografia Avantio ainda não está testada.”"
)

doc.save(out)
print(f"Documento criado: {out}")
