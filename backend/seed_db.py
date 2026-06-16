from neo4j_utils import db


def seed_data():
    print("Czyszczenie bazy...")
    db.query("MATCH (n) DETACH DELETE n")

    print("Zasilanie bazy danych...")
    cypher_query = """
    // ── 1. GATUNKI ──────────────────────────────────────────────────────────
    CREATE (sf:Genre   {name: 'Sci-Fi'}),
           (act:Genre  {name: 'Action'}),
           (dr:Genre   {name: 'Drama'}),
           (fant:Genre {name: 'Fantasy'}),
           (thr:Genre  {name: 'Thriller'}),
           (com:Genre  {name: 'Comedy'}),
           (hor:Genre  {name: 'Horror'}),
           (ani:Genre  {name: 'Animation'})

    // ── 2. REŻYSERZY ────────────────────────────────────────────────────────
    CREATE (nolan:Person     {name: 'Christopher Nolan'}),
           (villeneuve:Person{name: 'Denis Villeneuve'}),
           (tarantino:Person {name: 'Quentin Tarantino'}),
           (scorsese:Person  {name: 'Martin Scorsese'}),
           (russo:Person     {name: 'Russo Brothers'}),
           (gerwig:Person    {name: 'Greta Gerwig'}),
           (scott:Person     {name: 'Ridley Scott'}),
           (fincher:Person   {name: 'David Fincher'}),
           (spielberg:Person {name: 'Steven Spielberg'}),
           (anderson:Person  {name: 'Wes Anderson'}),
           (peele:Person     {name: 'Jordan Peele'}),
           (cfukunaga:Person {name: 'Cary Fukunaga'}),
           (wright:Person    {name: 'Edgar Wright'}),
           (cuaron:Person    {name: 'Alfonso Cuarón'})

    // ── 3. FILMY – NOLAN ────────────────────────────────────────────────────
    CREATE (inc:Movie  {title: 'Inception',          year: 2010, rating: 8.8}),
           (int:Movie  {title: 'Interstellar',        year: 2014, rating: 8.6}),
           (dk:Movie   {title: 'The Dark Knight',     year: 2008, rating: 9.0}),
           (opp:Movie  {title: 'Oppenheimer',         year: 2023, rating: 8.4}),
           (pre:Movie  {title: 'The Prestige',        year: 2006, rating: 8.5}),
           (ten:Movie  {title: 'Tenet',               year: 2020, rating: 7.4}),
           (mem:Movie  {title: 'Memento',             year: 2000, rating: 8.4})

    // ── 4. AKTORZY – PULA NOLANA ────────────────────────────────────────────
    CREATE (dicaprio:Person {name: 'Leonardo DiCaprio'}),
           (hardy:Person    {name: 'Tom Hardy'}),
           (bale:Person     {name: 'Christian Bale'}),
           (cillian:Person  {name: 'Cillian Murphy'}),
           (hathaway:Person {name: 'Anne Hathaway'}),
           (jackman:Person  {name: 'Hugh Jackman'}),
           (pearce:Person   {name: 'Guy Pearce'}),
           (washington:Person{name: 'John David Washington'})

    CREATE (nolan)-[:DIRECTED]->(inc), (nolan)-[:DIRECTED]->(int),
           (nolan)-[:DIRECTED]->(dk),  (nolan)-[:DIRECTED]->(opp),
           (nolan)-[:DIRECTED]->(pre), (nolan)-[:DIRECTED]->(ten),
           (nolan)-[:DIRECTED]->(mem)

    CREATE (dicaprio)-[:ACTED_IN {role: 'Cobb'}]->(inc),
           (hardy)-[:ACTED_IN    {role: 'Eames'}]->(inc),
           (hardy)-[:ACTED_IN    {role: 'Bane'}]->(dk),
           (bale)-[:ACTED_IN     {role: 'Batman'}]->(dk),
           (cillian)-[:ACTED_IN  {role: 'Oppenheimer'}]->(opp),
           (cillian)-[:ACTED_IN  {role: 'Scarecrow'}]->(dk),
           (cillian)-[:ACTED_IN  {role: 'Crosby'}]->(ten),
           (hathaway)-[:ACTED_IN {role: 'Brand'}]->(int),
           (hathaway)-[:ACTED_IN {role: 'Catwoman'}]->(dk),
           (jackman)-[:ACTED_IN  {role: 'Angier'}]->(pre),
           (bale)-[:ACTED_IN     {role: 'Borden'}]->(pre),
           (washington)-[:ACTED_IN{role: 'Protagonist'}]->(ten),
           (hardy)-[:ACTED_IN    {role: 'Fordie'}]->(ten),
           (pearce)-[:ACTED_IN   {role: 'Leonard Shelby'}]->(mem)

    // ── 5. MARVEL / DC ──────────────────────────────────────────────────────
    CREATE (avg:Movie  {title: 'Avengers: Endgame',         year: 2019, rating: 8.4}),
           (iron:Movie {title: 'Iron Man',                   year: 2008, rating: 7.9}),
           (bw:Movie   {title: 'Black Widow',                year: 2021, rating: 6.7}),
           (spid:Movie {title: 'Spider-Man: No Way Home',    year: 2021, rating: 8.2}),
           (suicide:Movie{title:'The Suicide Squad',         year: 2021, rating: 7.2}),
           (joker:Movie{title: 'Joker',                      year: 2019, rating: 8.4}),
           (cap:Movie  {title: 'Captain America: Civil War', year: 2016, rating: 7.8})

    CREATE (rdj:Person       {name: 'Robert Downey Jr.'}),
           (johansson:Person {name: 'Scarlett Johansson'}),
           (holland:Person   {name: 'Tom Holland'}),
           (margot:Person    {name: 'Margot Robbie'}),
           (sam_jackson:Person{name: 'Samuel L. Jackson'}),
           (phoenix:Person   {name: 'Joaquin Phoenix'}),
           (evans:Person     {name: 'Chris Evans'})

    CREATE (russo)-[:DIRECTED]->(avg), (russo)-[:DIRECTED]->(cap),
           (cfukunaga)-[:DIRECTED]->(bw)

    CREATE (rdj)-[:ACTED_IN       {role: 'Tony Stark'}]->(iron),
           (rdj)-[:ACTED_IN       {role: 'Tony Stark'}]->(avg),
           (rdj)-[:ACTED_IN       {role: 'Tony Stark'}]->(cap),
           (rdj)-[:ACTED_IN       {role: 'Lewis Strauss'}]->(opp),
           (johansson)-[:ACTED_IN {role: 'Natasha Romanoff'}]->(avg),
           (johansson)-[:ACTED_IN {role: 'Black Widow'}]->(bw),
           (johansson)-[:ACTED_IN {role: 'Natasha Romanoff'}]->(cap),
           (holland)-[:ACTED_IN   {role: 'Peter Parker'}]->(spid),
           (holland)-[:ACTED_IN   {role: 'Peter Parker'}]->(avg),
           (holland)-[:ACTED_IN   {role: 'Peter Parker'}]->(cap),
           (margot)-[:ACTED_IN    {role: 'Harley Quinn'}]->(suicide),
           (sam_jackson)-[:ACTED_IN{role:'Nick Fury'}]->(avg),
           (sam_jackson)-[:ACTED_IN{role:'Nick Fury'}]->(iron),
           (sam_jackson)-[:ACTED_IN{role:'Nick Fury'}]->(cap),
           (phoenix)-[:ACTED_IN   {role: 'Joker'}]->(joker),
           (evans)-[:ACTED_IN     {role: 'Captain America'}]->(avg),
           (evans)-[:ACTED_IN     {role: 'Steve Rogers'}]->(cap)

    // ── 6. BARBIE / SCORSESE / TARANTINO ────────────────────────────────────
    CREATE (barbie:Movie{title: 'Barbie',                     year: 2023, rating: 7.0}),
           (pulp:Movie  {title: 'Pulp Fiction',               year: 1994, rating: 8.9}),
           (once:Movie  {title: 'Once Upon a Time in Hollywood',year:2019,rating: 7.6}),
           (wolf:Movie  {title: 'The Wolf of Wall Street',     year: 2013, rating: 8.2}),
           (depart:Movie{title: 'The Departed',               year: 2006, rating: 8.5}),
           (kill1:Movie {title: 'Kill Bill: Vol. 1',          year: 2003, rating: 8.1})

    CREATE (gosling:Person{name: 'Ryan Gosling'}),
           (pitt:Person  {name: 'Brad Pitt'}),
           (damon:Person {name: 'Matt Damon'}),
           (nicholson:Person{name:'Jack Nicholson'})

    CREATE (gerwig)-[:DIRECTED]->(barbie),
           (tarantino)-[:DIRECTED]->(pulp),
           (tarantino)-[:DIRECTED]->(once),
           (tarantino)-[:DIRECTED]->(kill1),
           (scorsese)-[:DIRECTED]->(wolf),
           (scorsese)-[:DIRECTED]->(depart)

    CREATE (gosling)-[:ACTED_IN  {role: 'Ken'}]->(barbie),
           (margot)-[:ACTED_IN   {role: 'Barbie'}]->(barbie),
           (margot)-[:ACTED_IN   {role: 'Naomi'}]->(wolf),
           (dicaprio)-[:ACTED_IN {role: 'Rick Dalton'}]->(once),
           (dicaprio)-[:ACTED_IN {role: 'Jordan Belfort'}]->(wolf),
           (dicaprio)-[:ACTED_IN {role: 'Billy Costigan'}]->(depart),
           (pitt)-[:ACTED_IN     {role: 'Cliff Booth'}]->(once),
           (sam_jackson)-[:ACTED_IN{role:'Jules'}]->(pulp),
           (damon)-[:ACTED_IN    {role: 'Colin Sullivan'}]->(depart),
           (nicholson)-[:ACTED_IN{role:'Frank Costello'}]->(depart)

    // ── 7. VILLENEUVE & SCI-FI ──────────────────────────────────────────────
    CREATE (dune:Movie  {title: 'Dune',              year: 2021, rating: 8.0}),
           (dune2:Movie {title: 'Dune: Part Two',    year: 2024, rating: 8.5}),
           (br2049:Movie{title: 'Blade Runner 2049', year: 2017, rating: 8.0}),
           (arr:Movie   {title: 'Arrival',           year: 2016, rating: 7.9}),
           (enemy:Movie {title: 'Enemy',             year: 2013, rating: 6.9})

    CREATE (chalamet:Person{name: 'Timothée Chalamet'}),
           (zendaya:Person  {name: 'Zendaya'}),
           (isaac:Person    {name: 'Oscar Isaac'}),
           (ferguson:Person {name: 'Rebecca Ferguson'})

    CREATE (villeneuve)-[:DIRECTED]->(dune),
           (villeneuve)-[:DIRECTED]->(dune2),
           (villeneuve)-[:DIRECTED]->(br2049),
           (villeneuve)-[:DIRECTED]->(arr),
           (villeneuve)-[:DIRECTED]->(enemy)

    CREATE (chalamet)-[:ACTED_IN {role: 'Paul Atreides'}]->(dune),
           (chalamet)-[:ACTED_IN {role: 'Paul Atreides'}]->(dune2),
           (zendaya)-[:ACTED_IN  {role: 'Chani'}]->(dune),
           (zendaya)-[:ACTED_IN  {role: 'Chani'}]->(dune2),
           (zendaya)-[:ACTED_IN  {role: 'MJ'}]->(spid),
           (gosling)-[:ACTED_IN  {role: 'K'}]->(br2049),
           (hardy)-[:ACTED_IN    {role: 'Mad Max'}]->(br2049),
           (isaac)-[:ACTED_IN    {role: 'Duke Leto'}]->(dune),
           (ferguson)-[:ACTED_IN {role: 'Lady Jessica'}]->(dune),
           (ferguson)-[:ACTED_IN {role: 'Lady Jessica'}]->(dune2)

    // ── 8. KLASYKI ───────────────────────────────────────────────────────────
    CREATE (glat:Movie {title: 'Gladiator',            year: 2000, rating: 8.5}),
           (mat:Movie  {title: 'The Matrix',           year: 1999, rating: 8.7}),
           (fight:Movie{title: 'Fight Club',           year: 1999, rating: 8.8}),
           (se7en:Movie{title: 'Se7en',                year: 1995, rating: 8.6}),
           (schindler:Movie{title:"Schindler's List",  year: 1993, rating: 9.0}),
           (jaws:Movie {title: 'Jaws',                 year: 1975, rating: 8.0}),
           (asteroid:Movie{title:'Asteroid City',      year: 2023, rating: 6.6})

    CREATE (reeves:Person   {name: 'Keanu Reeves'}),
           (norton:Person   {name: 'Edward Norton'}),
           (neeson:Person   {name: 'Liam Neeson'}),
           (hanks:Person    {name: 'Tom Hanks'}),
           (blanchett:Person{name: 'Cate Blanchett'}),
           (spacey:Person   {name: 'Kevin Spacey'})

    CREATE (scott)-[:DIRECTED]->(glat),
           (fincher)-[:DIRECTED]->(fight),
           (fincher)-[:DIRECTED]->(se7en),
           (spielberg)-[:DIRECTED]->(schindler),
           (spielberg)-[:DIRECTED]->(jaws),
           (anderson)-[:DIRECTED]->(asteroid)

    CREATE (phoenix)-[:ACTED_IN  {role: 'Commodus'}]->(glat),
           (reeves)-[:ACTED_IN   {role: 'Neo'}]->(mat),
           (norton)-[:ACTED_IN   {role: 'Narrator'}]->(fight),
           (pitt)-[:ACTED_IN     {role: 'Tyler Durden'}]->(fight),
           (pitt)-[:ACTED_IN     {role: 'Mills'}]->(se7en),
           (spacey)-[:ACTED_IN   {role: 'John Doe'}]->(se7en),
           (neeson)-[:ACTED_IN   {role: 'Oskar Schindler'}]->(schindler),
           (blanchett)-[:ACTED_IN{role: 'June Douglas'}]->(asteroid)

    // ── 9. NOWE HITY (2022-2024) ────────────────────────────────────────────
    CREATE (poor:Movie {title: 'Poor Things',     year: 2023, rating: 7.9}),
           (holdovers:Movie{title:'The Holdovers',year: 2023, rating: 7.9}),
           (civil:Movie{title: 'Civil War',        year: 2024, rating: 7.2}),
           (napoleon:Movie{title:'Napoleon',       year: 2023, rating: 6.4})

    CREATE (stone:Person    {name: 'Emma Stone'}),
           (giamatti:Person {name: 'Paul Giamatti'}),
           (kirsten:Person  {name: 'Kirsten Dunst'})

    CREATE (scott)-[:DIRECTED]->(napoleon)
    CREATE (stone)-[:ACTED_IN   {role: 'Bella Baxter'}]->(poor),
           (giamatti)-[:ACTED_IN{role: 'Paul Hunham'}]->(holdovers),
           (kirsten)-[:ACTED_IN {role: 'Lee'}]->(civil)

    // ── 10. GATUNKI DLA NOWYCH FILMÓW ───────────────────────────────────────
    CREATE (inc)-[:BELONGS_TO]->(sf),   (int)-[:BELONGS_TO]->(sf),
           (dk)-[:BELONGS_TO]->(act),   (opp)-[:BELONGS_TO]->(dr),
           (avg)-[:BELONGS_TO]->(act),  (iron)-[:BELONGS_TO]->(act),
           (dune)-[:BELONGS_TO]->(sf),  (dune2)-[:BELONGS_TO]->(sf),
           (br2049)-[:BELONGS_TO]->(sf),(pulp)-[:BELONGS_TO]->(thr),
           (wolf)-[:BELONGS_TO]->(com), (barbie)-[:BELONGS_TO]->(com),
           (glat)-[:BELONGS_TO]->(dr),  (fight)-[:BELONGS_TO]->(thr),
           (se7en)-[:BELONGS_TO]->(thr),(mat)-[:BELONGS_TO]->(sf),
           (joker)-[:BELONGS_TO]->(dr), (depart)-[:BELONGS_TO]->(thr),
           (spid)-[:BELONGS_TO]->(act), (pre)-[:BELONGS_TO]->(thr),
           (mem)-[:BELONGS_TO]->(thr),  (ten)-[:BELONGS_TO]->(act),
           (arr)-[:BELONGS_TO]->(sf),   (once)-[:BELONGS_TO]->(dr),
           (kill1)-[:BELONGS_TO]->(act),(poor)-[:BELONGS_TO]->(dr),
           (asteroid)-[:BELONGS_TO]->(com),(napoleon)-[:BELONGS_TO]->(dr),
           (schindler)-[:BELONGS_TO]->(dr),(cap)-[:BELONGS_TO]->(act)

    

    // ── 11. RELACJE MIĘDZY AKTORAMI (ZNAJOMOŚCI) ────────────────────────────
    CREATE (dicaprio)-[:FRIENDS_WITH]->(pitt),
           (cillian)-[:FRIENDS_WITH]->(hardy),
           (margot)-[:FRIENDS_WITH]->(stone)
    """
    db.query(cypher_query)
    print("Sukces! Baza zawiera teraz ponad 100 węzłów i 200+ relacji.")


if __name__ == "__main__":
    seed_data()