# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:137:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:148:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:156:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:179:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:210:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:227:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:258:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:277:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
config.py:2:0: C0103: Constant name "database_file" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module ideas
ideas.py:1:0: C0114: Missing module docstring (missing-module-docstring)
ideas.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:78:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:114:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:124:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:138:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:149:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:166:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:71:0: C0116: Missing function or method docstring (missing-function-docstring)
Your code has been rated at 8.83/10 (previous run: 8.83/10, +0.00)
```

Käydään seuraavaksi läpi raportin ilmoitukset ja perustellaan, miksi niitä ei ole korjattu.

## Docstring-ilmoitukset

Suurin osa ilmoituksista on seuraavanlaisia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja.
Sovelluksen kehityksessä on tehty tietoinen päätös olla käyttämättä docstring-kommentteja,
koska funktioiden nimet kertovat jo, mitä funktiot tekevät.

## Vakion nimi

Raportissa on seuraavat ilmoitukset:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
config.py:2:0: C0103: Constant name "database_file" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Pylint tulkitsee nämä muuttujat vakioiksi, joiden nimet tulisi kirjoittaa isoilla kirjaimilla.
Kyseessä ovat kuitenkin asetukset, joita voi muuttaa omalla koneella, joten
pienet kirjaimet on valittu tarkoituksella samaan tapaan kuin kurssimateriaalissa.
