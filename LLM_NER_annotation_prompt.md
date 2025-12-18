# 📚 Annotating 18th and 19th-Century Newspaper Book Advertisements (OCR Noisy Text)

## Task Overview

You are processing noisy OCR snippets from 19th-century book sale advertisements. These texts may contain spelling errors, fragments of old German, French, or Latin, inconsistent formatting, and missing information.

Each input snippet corresponds to **exactly one** advertisement and must be wrapped in a single `<ITEM>...</ITEM>` tag. Within each `<ITEM>`, you should annotate **all book descriptions** using one or more `<BIBL>` elements.

⚠️ A single `<ITEM>` may contain **multiple `<BIBL>` elements**, but there is always **exactly one `<ITEM>` per snippet**.

---

## Tagging Rules

Within each `<ITEM>`, wrap all book references using the following structure:

- `<BIBL>`: Wraps a full book description. Each advertisement can contain multiple `<BIBL>` elements.
- Inside `<BIBL>`, annotate the following elements **only if present** (never guess or infer missing data):

  - `<AUTHOR>...</AUTHOR>`
  - `<TITLE>...</TITLE>`
  - `<YEAR>...</YEAR>`
  - `<PLACE>...</PLACE>`
  - `<FORMAT>...</FORMAT>`
  - `<VOLUME>...</VOLUME>`
  - `<PRIZE>...</PRIZE>`

Do **not** annotate catalog structure such as:
- Phrases like `"Item:"`, `"Ferner:"`
- Seller information or address details
- Entry numbers (e.g., `"21."`)

These should remain **outside** `<BIBL>`, but still **inside** the enclosing `<ITEM>`.

---

## Style and Fidelity

- **Repeat the full original text** inside the `<ITEM>` exactly as given.
- **Do not correct OCR errors** or normalize spelling, hyphens, or numbers.
- **Do not hallucinate or invent** any missing information.
- Annotate what you see, not what you infer.

---

## Output Format

The output must consist of a single `<ITEM>` per input. Inside this, wrap each book with a `<BIBL>` and nested tags if present.

The output must be **valid XML**. Do not include markdown, explanations, or commentary. Always place XML tags inline with the original text unless the input includes line breaks.

---

# 📖 Examples

## Example 1
### INPUT ###
21. Bey Herrn Johann Heinrich Flick dem Buchbinder an der Gerbergaß ist zu haben: Johann Friederich Stapfers, Prediger Göttlichen Wortes, Grundlegung zur wahren Religion, Erster Theil, 8vò. 1746. à fl. 1. 15. xr.
### OUTPUT ###
<ITEM>21. Bey Herrn Johann Heinrich Flick dem Buchbinder an der Gerbergaß ist zu haben: <BIBL><AUTHOR>Johann Friederich Stapfers</AUTHOR>, Prediger Göttlichen Wortes, <TITLE>Grundlegung zur wahren Religion</TITLE>, Erster Theil, <FORMAT>8vò</FORMAT>. <YEAR>1746</YEAR>. à <PRIZE>fl. 1. 15. xr.</PRIZE></BIBL></ITEM>

## Example 2
### INPUT ###
Item: Werdmüllers (Beat) Predigt so bey Anlaß eines getauften Juden den 26ten May 1746. in Zürich gehalten worden, in 4tò. à 12. xr.
### OUTPUT ###
<ITEM>Item: <BIBL><AUTHOR>Werdmüllers (Beat)</AUTHOR> <TITLE>Predigt so bey Anlaß eines getauften Juden den 26ten May 1746. in Zürich gehalten worden</TITLE>, in <FORMAT>4tò</FORMAT>. à <PRIZE>12. xr.</PRIZE></BIBL></ITEM>

## Example 3
### INPUT ###
Ferner: Eydgnoßisches Stadt- und Land-Recht von J. J. Leu, vierter Theil 1746. in 4tò. à fl. 2.
### OUTPUT ###
<ITEM>Ferner: <BIBL><TITLE>Eydgnoßisches Stadt- und Land-Recht</TITLE> von <AUTHOR>J. J. Leu</AUTHOR>, vierter Theil <YEAR>1746</YEAR>. in <FORMAT>4tò</FORMAT>. à <PRIZE>fl. 2.</PRIZE></BIBL></ITEM>

## Example 4
### INPUT ###
Les Oeuvres de Monsieur de Molliere, 5. Tom. in 8vo. in raisonnablem Preiß.
### OUTPUT ###
<ITEM><BIBL><TITLE>Les Oeuvres</TITLE> de <AUTHOR>Monsieur de Molliere</AUTHOR>, <VOLUME>5. Tom.</VOLUME> in <FORMAT>8vo.</FORMAT> in raisonnablem Preiß.</BIBL></ITEM>

## Example 5
### INPUT ###
30. Bey Herrn Joh. Conrad von Mechel, in der Steinen-Vorstadt sind zu haben: Auserlesene Geistliche Lieder, aus den besten Dichteren, mit gans neuen leichten Melodien versehen, 8. Zurich 1769 à 54 kr. Dieses neue Lieder-Buch ist in der Form des bekannten Bachoffischen Gesangbuchs gedruckt, dasselbe enthält eine Sammlung der verständlichsten, kernhaftesten und gemeinnutzigsten Liedern der heutigen Dichteren; die Melodien sind mit ganz neuen und solchen Roten gedruckt, die denen geschriebenen sehr gleich sind. Alle diese Vorzuge, und dabey noch der geringe Preis dieses Wercks, lassen hoffen , daß dasselbe auch hier von denen Liebhabern der Musie mit geneigtem Beyfall werde aufgenommen werden.
### OUTPUT ###
<ITEM>30. Bey Herrn Joh. Conrad von Mechel, in der Steinen-Vorstadt sind zu haben: <BIBL><TITLE>Auserlesene Geistliche Lieder, aus den besten Dichteren, mit gans neuen leichten Melodien versehen</TITLE>, <FORMAT>8.</FORMAT> <PLACE>Zurich</PLACE> <YEAR>1769</YEAR> à <PRIZE>54 kr.</PRIZE></BIBL> Dieses neue Lieder-Buch ist in der Form des bekannten Bachoffischen Gesangbuchs gedruckt, dasselbe enthält eine Sammlung der verständlichsten, kernhaftesten und gemeinnutzigsten Liedern der heutigen Dichteren; die Melodien sind mit ganz neuen und solchen Roten gedruckt, die denen geschriebenen sehr gleich sind. Alle diese Vorzuge, und dabey noch der geringe Preis dieses Wercks, lassen hoffen , daß dasselbe auch hier von denen Liebhabern der Musie mit geneigtem Beyfall werde aufgenommen werden.</ITEM>

## Example 6
### INPUT ###
Der Historien-Saal, 6. Band 4to. in Pergament à fl. 6.
### OUTPUT ###
<ITEM><BIBL><TITLE>Der Historien-Saal</TITLE>, <VOLUME>6. Band</VOLUME> <FORMAT>4to</FORMAT>. in Pergament à <PRIZE>fl. 6</PRIZE></BIBL></ITEM>

## Example 7
### INPUT ###
Nouveau Vovage autour du Monde, par Monsieur le Gentil, en 3. Volum. 8vo. Amsterdam, per ein Gulden
### OUTPUT ###
<ITEM><BIBL><TITLE>Nouveau Vovage autour du Monde</TITLE>, par <AUTHOR>Monsieur le Gentil</AUTHOR>, en <VOLUME>3. Volum.</VOLUME> <FORMAT>8vo.</FORMAT> <PLACE>Amsterdam</PLACE>, per <PRIZE>ein Gulden</PRIZE></BIBL></ITEM>

## Example 8
### INPUT ###
UIrici Huberi Praelectiones Juris, gantz neu umb 2. Thaler
### OUTPUT ###
<ITEM><BIBL>UIrici Huberi <TITLE>Praelectiones Juris</TITLE>, gantz neu umb <PRIZE>2. Thaler</PRIZE></BIBL></ITEM>

## Example 9
### INPUT ###
7. Bey Herrn Daniel Haag dem Buchbinder sind folgende Bücher zu verkauffen: Moreri Dictionaire, fol. 6. Tom. gantz neu in Frantzös. schem Band. Ein gantz neuer in roht Leder gebundener Atlas von 20. Homännischen Carten Simlers Regiment Löbl. Eydgnoßschafft, in 4tò. Menantes Brieffsteller, 2. Tom, 8vò. Kyburtzens abgekürtzte Kinder-Bibel, in 8vò. Alt und Nen Testament, mit und ohne Kupfer.
### OUTPUT ###
7. <ITEM>Bey Herrn Daniel Haag dem Buchbinder sind folgende Bücher zu verkauffen: <BIBL><AUTHOR>Moreri</AUTHOR> <TITLE>Dictionaire</TITLE>, <FORMAT>fol.</FORMAT> <VOLUME>6. Tom.</VOLUME> gantz neu in Frantzös. schem Band.</BIBL> <BIBL>Ein gantz neuer in roht Leder gebundener <TITLE>Atlas von 20. Homännischen Carten</TITLE></BIBL> <BIBL><AUTHOR>Simlers</AUTHOR> <TITLE>Regiment Löbl. Eydgnoßschafft</TITLE>, in <FORMAT>4tò.</FORMAT></BIBL> <BIBL><AUTHOR>Menantes</AUTHOR> <TITLE>Brieffsteller</TITLE>, <VOLUME>2. Tom</VOLUME>, <FORMAT>8vò.</FORMAT></BIBL> <BIBL><AUTHOR>Kyburtzens</AUTHOR> abgekürtzte <TITLE>Kinder-Bibel</TITLE>, in <FORMAT>8vò.</FORMAT></BIBL> <BIBL><TITLE>Alt und Nen Testament</TITLE>, mit und ohne Kupfer.</BIBL></ITEM>

## Example 10
### INPUT ###
9. Der aus dem Reiche der Wissenschafften wohl versuchte Referendarius, oder auserlesene Sammlungen von allerhand vermischten Schrifften und Versuchen aus der Natur- Lehre, Artzney-Wissenschafft, natürlichen Theologie, und Rechts Gelehrsamkeit, Politic, Haushaltungs-Kunst, und uberhaubt was in anderen in fremden Sprachen heraus gekommenen Wochen-Schrifften und neuen Bücheren ꝛc. ꝛ6. gutes und nutzliches vorgekommen. 1ter und ater Theil, 4to. 1750. mit zerschiedenen Kupferstichen, in frantzösischen Band à fl. 3. 24. kr., in Ruck und Ecken aber à fl. 3. und ungebunden à fl. 2. 30. kr. Item, Das guldene Bilder-Psalmen-Buch, darinn alle von Luthero verteutschte Weissagungs-Lehr- Buß-Bett-Klag- und Danck-Psalmen des Hoherleuchteten Königs und Propheten Davids nach ihrem fürnehmsten Innhalt in 150. anmühtigen Bilderen, allen und jeden, besonders aber der lieben Jugend, zur heiligen Belustigung und heilsamer Erbauung sinnreich vorgestellt und in Kupfer gestochen, 8vò. Augspurg 1750. gebunden à fl. 1. 12. kr. ungebunden à fl. 1. sind im Berichthaus zu haben.
### OUTPUT ###
<ITEM><BIBL><TITLE>Der aus dem Reiche der Wissenschafften wohl versuchte Referendarius, oder auserlesene Sammlungen von allerhand vermischten Schrifften und Versuchen aus der Natur- Lehre, Artzney-Wissenschafft, natürlichen Theologie, und Rechts Gelehrsamkeit, Politic, Haushaltungs-Kunst, und uberhaubt was in anderen in fremden Sprachen heraus gekommenen Wochen-Schrifften und neuen Bücheren ꝛc. ꝛ6. gutes und nutzliches vorgekommen.</TITLE>, <VOLUME>1ter und ater Theil</VOLUME>, in <FORMAT>4to.</FORMAT>. <YEAR>1750</YEAR>. mit zerschiedenen Kupferstichen, in frantzösischen Band à <PRIZE>fl. 3. 24. kr.</PRIZE>, in Ruck und Ecken aber à <PRIZE>fl. 3.</PRIZE> und ungebunden à <PRIZE>fl. 2. 30. kr.</PRIZE></BIBL> Item, <BIBL><TITLE>Das guldene Bilder-Psalmen-Buch, darinn alle von Luthero verteutschte Weissagungs-Lehr- Buß-Bett-Klag- und Danck-Psalmen des Hoherleuchteten Königs und Propheten Davids nach ihrem fürnehmsten Innhalt in 150. anmühtigen Bilderen, allen und jeden, besonders aber der lieben Jugend, zur heiligen Belustigung und heilsamer Erbauung sinnreich vorgestellt und in Kupfer gestochen</TITLE>, <FORMAT>8vò.</FORMAT> <PLACE>Augspurg</PLACE> <YEAR>1750</YEAR>. gebunden à <PRIZE>fl. 1. 12. kr.</PRIZE> ungebunden à <PRIZE>fl. 1.</PRIZE> sind im Berichthaus zu haben.</BIBL></ITEM> 

---

## Response Format

Use the following format exactly for each annotation task:

```
<ITEM>[INSERT ANNOTATED XML]</ITEM>
```

---

## Final Notes

- Always wrap the full snippet in **one `<ITEM>`**.
- Inside the `<ITEM>`, annotate **each book description** using a `<BIBL>` tag.
- Use sub-tags (`<AUTHOR>`, `<TITLE>`, etc.) **only if the information is explicitly present**.
- **Do not alter** original OCR text — preserve errors.
- **Do not wrap catalog structure or seller info.**
- **Do not generate anything outside the XML.**
