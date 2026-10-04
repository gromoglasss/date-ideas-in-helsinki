# date-ideas-in-helsinki
* Sovellus, johon käyttäjät voivat jakaa treffi-ideoita.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen treffi-ideoita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ideoitaan.
* Käyttäjä näkee sovellukseen lisätyt treffi-ideat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ideat.
* Kättäjä pystyy etsimään treffi-ideoita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä ideoita.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät ideat.
* Käyttäjä pystyy valitsemaan idealle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on pääasiallisen tietokohteen lisäksi toissijainen idea, joka täydentää pääasiallista ideaa. Käyttäjä pystyy lisäämään toissijaisia ideoita omiin ja muiden käyttäjien ideoihin liittyen.

## Sovelluksen käynnistäminen paikallisesti

Tarvitset Python 3:n ja Gitin.

1. Kloonaa repositorio ja siirry projektikansioon:

   ```bash
   git clone https://github.com/gromoglasss/date-ideas-in-helsinki.git
   cd date-ideas-in-helsinki
   ```

2. Luo virtuaaliympäristö:

   ```bash
   python -m venv .venv
   ```

3. Aktivoi virtuaaliympäristö.

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Asenna Flask ja käynnistä sovellus:

   ```bash
   python -m pip install Flask
   python -m flask --app app run --debug
   ```

5. Avaa selaimessa <http://127.0.0.1:5000>.

Tietokanta luodaan ja esimerkkitiedot lisätään automaattisesti sovelluksen
ensimmäisen käynnistyksen yhteydessä.

# Kuinka käyttää sovellusta:
* Jotta voisit lisätä ja muokata omia ideoitasi, sinun täytyy kirjautua sisään painamalla "kirjaudu sisään" nappia.
* Jos sinulla ei ole vielä käyttäjää, voit luoda sen painamalla "Rekisteröyidy" nappia.
* Voit lisätä omia ideoitasi "Lisää uusi idea" napista painamalla.
* Idealle pitää antaa otsikko. Kuva, kuvaus ja luokittelut ovat vapaaehtoisia.
* Idealle voi valita luokittelut (hinta, paikka ja vuodenaika).
* Pääset muokkaamaan ja poistamaan omat ideasi päänäkymästä.
* Voit etsiä ideoita hakukentän avulla.
* Idean otsikkoa painamalla pääset idean sivulle, jossa voit lukea ja kirjoittaa kommentteja.
* Käyttäjän nimeä painamalla näet käyttäjän sivun, jossa on käyttäjän tilastot ja ideat.
* Voit kirjautua ulos halutessasi painamalla "kirjaudu ulos" nappia. 

## Sovelluksen testaus suurella tietomäärällä

Sovellusta testattiin suurella tietomäärällä tiedoston `seed.py` avulla.
Skripti luo tietokantaan 1000 käyttäjää, 100 000 ideaa ja miljoona kommenttia.
Huom: skripti poistaa kaikki aiemmat tiedot tietokannasta.

```bash
python seed.py
```

Sivujen latausajat (keskiarvo viidestä latauksesta):

| Sivu | Ilman indeksejä | Indeksien kanssa |
| --- | --- | --- |
| Etusivu, sivu 1 | 1,75 s | 0,005 s |
| Etusivu, sivu 5000 | 1,75 s | 0,08 s |
| Etusivu, sivu 10000 (viimeinen) | 1,81 s | 0,15 s |
| Haku | 1,75 s | 0,02 s |
| Idean sivu | 0,05 s | 0,001 s |
| Käyttäjän sivu | 0,06 s | 0,001 s |

Etusivulla näytetään jokaisen idean kommenttien määrä, joten ilman indeksiä
tietokannan pitää käydä läpi kaikki miljoona kommenttia jokaisella latauksella.
Tiedostossa `schema.sql` olevat indeksit (esim. `comments (idea_id)`) nopeuttavat
tätä huomattavasti. Etusivu näyttää ideat sivuittain (10 ideaa per sivu), joten
sivu pysyy nopeana, vaikka ideoita on paljon. Myöhemmät sivut ovat hieman
hitaampia, koska `OFFSET` joutuu ohittamaan aiemmat rivit.

## Pylint

Pylint-raportti löytyy tiedostosta [pylint-report.md](pylint-report.md).

(en suorittanut kurssia viime periodissa niin jatkan samaa projektia tässä periodissa)
