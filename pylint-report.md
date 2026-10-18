# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:107:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:115:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:140:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:171:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:212:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:249:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:274:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:305:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:324:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
config.py:2:0: C0103: Constant name "database_file" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:21:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module ideas
ideas.py:1:0: C0114: Missing module docstring (missing-module-docstring)
ideas.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:113:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
ideas.py:133:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 8.61/10
```

Käydään seuraavaksi läpi raportin ilmoitukset ja perustellaan, miksi niitä ei ole korjattu.

## Docstring-ilmoitukset

Suurin osa ilmoituksista on seuraavanlaisia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
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

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset:

```
db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:21:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Ilmoitukset koskevat tiedoston `db.py` funktioita `execute` ja `query`, jotka on toteutettu
kurssimateriaalin mukaisesti:

```python
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
```

Parametrin oletusarvona oleva tyhjä lista luodaan vain kerran, ja sama listaolio on
käytössä kaikissa kutsuissa, joissa parametria ei anneta. Tästä voisi tulla ongelma,
jos funktio muuttaisi listan sisältöä, koska muutos näkyisi myös myöhemmissä kutsuissa.
Funktiot kuitenkin vain välittävät listan SQLite-kirjastolle eivätkä muuta sitä,
joten oletusarvosta ei ole tässä haittaa.
