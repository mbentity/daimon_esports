
# Daimon Esports

La seguente tesi descrive e sostiene lo sviluppo di Daimon Esports, un portale web dedicato alla creazione e gestione di competizioni esports principalmente amatoriali, senza escludere tuttavia potenziali applicazioni ufficiali.

![[Pasted image 20240831230240.png]]
_Schermata principale della piattaforma._

# Requisiti di Installazione

- Connessione a internet
- Dispositivo locale Linux, Windows o MAC
- Git
- Docker

# Installazione Backend

- git clone https://github.com/mbentity/daimon_esports
- docker build -t daimon_esports daimon_esports
- docker run -p 8000:8000 daimon_esports

# Installazione Frontend

- git clone https://github.com/mbentity/daimon_esports_frontend
- docker build -t daimon_esports_frontend daimon_esports_frontend
- docker run -p 3000:3000 daimon_esports_frontend

# Accesso

- in caso di necessità di effettuare test, è presente un account admin:
	- username: techweb
	- password: techweb

# Consegna

### Come riportato dalla mail di proposta del progetto:
"Applicazione Web per l'organizzazione, partecipazione e visione di tornei esports.
Pensata per essere utilizzabile da utenti anonimi e registrati:
- gli utenti anonimi possono consultare le classifiche di tutti i tornei, e sintonizzarsi sui canali di trasmissione delle partite attualmente in corso
- gli utenti registrati possono iscriversi a tornei, creando delle squadre o richiedendo di unirsi a squadre esistenti
- gli utenti registrati possono ricevere l'autorizzazione di organizzare tornei, specificando la disciplina, la piattaforma di ritrovo, il canale di trasmissione e le date di svolgimento
Il sistema deve consentire la ricerca di tornei in base a criteri come disciplina, data di inizio e disponibilità delle iscrizioni.
Il sistema deve gestire autonomamente i posti disponibili per ogni squadra e per ogni torneo, e permettere una basilare comunicazione tra utenti per inviare e approvare richieste di squadra.
Ogni azione deve essere modificabile e reversibile: gli organizzatori devono poter modificare o cancellare un torneo, i capi squadra devono poter modificare o sciogliere una squadra e i giocatori devono poter abbandonare una squadra, e di conseguenza il torneo."

# Struttura

Il progetto è suddiviso in tre parti:

- Tesi di presentazione
- Frontend: applicativo multipage in NextJS (Node, Typescript)
- Backend: API in Django Rest Framework (Django, Python)

Frontend e Backend sono dockerizzati, come desumibile dal processo di installazione, e devono essere eseguiti entrambi per il corretto funzionamento della piattaforma.
Le immagini Docker sono state costruite basandosi su Alpine, una distribuzione Linux leggera ed efficiente.
Una volta buildate e eseguite entrambe le immagini, il portale è raggiungibile in locale su http://localhost:3000, mentre la piattaforma admin è raggiungibile, sempre in locale, su http://localhost:8000/admin.

# Strumenti

Frontend e Backend sono stati sviluppati con Visual Studio Code come IDE di preferenza.
La tesi è stata scritta su Obsidian.md e compattata in PDF tramite Pandoc.