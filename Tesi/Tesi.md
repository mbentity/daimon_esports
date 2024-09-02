
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
- docker run -p 3000:3000 daimon_esports

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
# 1 - Introduzione

Con l'avvento del videogioco competitivo, avviato dallo storico StarCraft, gli esports si sono man mano fatti strada tra pregiudizi e incertezze, per diventare nel nuovo decennio un pilastro dell'intrattenimento digitale.

Grazie a una generosa spinta dalla pandemia e a una presenza solida nella cultura di massa di Cina e Corea del Sud, il media ha raggiunto rilevanza globale, con picchi di ascolti in aumento di anno in anno (dai 3.8 milioni dei mondiali di League of Legends del 2020, ai 6.4 milioni dell'edizione del 2023) e ingenti montepremi (31 milioni di dollari durante l'anno 2023 solo contando i premi di Dota 2).

Tuttavia, è facile perdersi nei numeri e dimenticare il punto di partenza: l'industria degli esports è un investimento mirato ad appassionare e ispirare i giocatori, ma pochi studi si preoccupano di mantenere un sistema competitivo al di fuori dei circuiti ufficiali, nonostante la grande domanda.

L'idea di Daimon Esports è di emulare il sistema di automazione delle piattaforme e dei canali ufficiali del media, ma con una bassa barriera di ingresso e un focus sulle organizzazioni amatoriali, per permettere lo svilupparsi di campionati e eventi tenuti dalla community per la community.

Specificamente, il progetto si concentra su tre categorie di utenti principali:

- organizzatori di tornei e di squadre alla ricerca di una piattaforma dove gestire eventi e trovare un pubblico e una massa di giocatori;
- giocatori alla ricerca di nuove competizioni a cui prendere parte;
- spettatori interessati al panorama amatoriale degli esports.

Scopo della piattaforma è fornire a tutte e tre queste categorie una soluzione comoda e promettente alle loro esigenze.
# 2 - Progettazione

Come punto di partenza, analizziamo piattaforme esistenti che ricoprono, totalmente o parzialmente, le funzioni di Daimon Esports.

## Lolesports e Valorantesports

![[Pasted image 20240831233309.png]]

In giugno 2024, entrambi i portali esports dei principali titoli Riot Games, ovvero League of Legends e Valorant, hanno subito un radicale redesign. Questo ha portato alla perdita della caratteristica che ha ispirato principalmente il design grafico del progetto di Daimon Esports: un header orizzontale con la lista di partite in corso e in arrivo.

![[Pasted image 20240831233845.png]]
_un esempio dell'aspetto precedente della piattaforma Lolesports, tratto dalla Wayback Machine_

La scelta stilistica è innovativa, accattivante e funzionale, ed è in particolare molto efficace a motivare gli spettatori provenienti da una nicchia specifica a sperimentare qualcosa fuori dalla loro comfort zone: delle altre squadre, un'altra regione, o anche un tier completamente diverso di competizione.

Questo potenziale può essere applicato anche a uno strato ancora superiore di suddivisione del media: assortendo un calendario combinato di tutte le partite di tutti i titoli supportati dalla piattaforma, è possibile aumentare ulteriormente il watchtime, facendo leva sul fatto che la maggior parte dei giocatori non è limitata a un singolo titolo, ed è probabile che trovi interessanti anche competizioni di altri giochi, al di fuori degli orari della sua nicchia principale.

## Start.gg

![[Pasted image 20240831235024.png]]

Un esempio di piattaforma pensata esplicitamente per tornei amatoriali è invece Start.gg, provvisto di funzionalità come creazione dettagliata di eventi, organizzazione di fasi di registrazione e gestione di squadre. Tuttavia, come si può notare già dalla prima pagina, il portale è mirato esclusivamente a organizzatori e giocatori, tralasciando la terza categoria considerata da Daimon Esports, ovvero gli spettatori.

# Funzionalità

Identifichiamo dunque le funzionalità che il progetto deve fornire:

- Spettatori
	- consultazione degli eventi in corso
	- quest'ultima facilitata da un motore di ricerca
	- sintonizzazione sui canali di trasmissione di suddetti eventi
- Giocatori
	- iscrizione agli eventi, creando nuove squadre o partecipando a squadre esistenti
	- gestione delle squadre intestate al giocatore stesso
	- iscrizione a molteplici eventi, anche in periodi sovrapposti
	- gestione del proprio account, necessario per garantire un ruolo attivo sulla piattaforma
- Organizzatori
	- creazione e gestione di molteplici eventi

# Tecnologie

Eccezion fatta per il requisito fondamentale del progetto, ovvero un backend sviluppato in Django, tutte le altre scelte strumentistiche sono state guidate principalmente dall'esperienza di uso personale del sottoscritto, e dal fine di velocizzare lo sviluppo della piattaforma e poter concentrare gli sforzi di apprendimento su scelte di design piuttosto che tecniche, almeno per quanto riguarda competenze al di fuori delle necessità educative del corso.

Per questo motivo, come linguaggio per il frontend è stato scelto TypeScript, un superset di JavaScript, e come framework è stato scelto NextJS, un potente strumento basato su ReactJS, importante libreria di frontend dell'ambiente NodeJS.

Per accomodare tale scelta, è stato deciso di omettere l'uso dei templates di Django, e conferire invece all'applicativo una funzione quasi esclusivamente di backend, tramite l'utilizzo del Django Rest Framework, il quale permette al frontend in NextJS di comunicare comodamente con il backend. Si tratta inoltre di un design molto vicino a soluzioni analoghe nell'ecosistema JavaScript, in particolare ExpressJS, caratteristica da cui è stata notevolmente facilitata l'adozione della soluzione.
Al di fuori di questo contesto risiede la piattaforma admin, che è stata abilitata e mantenuta sfruttando le funzionalità interne di Django, ed è quindi accessibile direttamente connettendosi al backend.

Quanto al database, per minimizzare la complessità del progetto si è optato per mantenere l'opzione default di SQLite, mirata specificamente per progetti a bassa scalabilità, previa consapevolezza che, qualora si volesse espandere la scala della piattaforma, sarà d'obbligo una migrazione a una soluzione di database più espansiva, come MariaDB o PostgreSQL.

Analogo ragionamento per l'hosting di file generati dagli utenti: usare il filesystem del container del backend è una soluzione semplice e adatta per la bassa portata attuale del progetto, ma necessiterà di una migrazione a una soluzione di file hosting remoto, quale Amazon S3 o MinIO, in caso sia necessario un upscaling.

Entrambi i lati della piattaforma sono poi confezionati come container di Docker, con Alpine come scelta di distribuzione per le immagini, in quanto leggera ed efficiente, con basso consumo overhead di risorse.

- - -
![[Struttura Progetto.png]]
- - -
_struttura attuale del progetto._

- - -
![[Struttura Progetto AWS.png]]
- - -
_concept di struttura del progetto in caso di upscaling, sfruttando la suite di servizi di AWS._

# Diagramma ER

Studiamo ora una serie di entità e relazioni per rappresentare i dati necessari al funzionamento dell'applicazione.

Innanzitutto, abbiamo bisogno di un'entità per rappresentare gli utenti, contenente le credenziali di accesso.

Altra entità di necessità ovvia è quella che rappresenterà i tornei, e accanto ad essi abbiamo bisogno di una lista di discipline, così che ogni torneo possa essere disputato su un titolo diverso.

Scopo della piattaforma è facilitare la comunicazione tra organizzatori, giocatori e spettatori, senza scendere troppo nel dettaglio su come i tornei vengono organizzati, per cui dotiamo l'entità torneo di due attributi destinati ad essere popolati con dei link:
- un link di ritrovo, dove gli organizzatori disporranno la maggior parte delle regole e comunicheranno direttamente con i giocatori (piattaforme esemplari sono Discord oppure Telegram)
- un link di trasmissione, dove verrà messa in onda la competizione. Per facilitare l'implementazione della feature, si è deciso di limitare la compatibilità a YouTube e Twitch, siccome entrambe le piattaforme permettono di realizzare URL univoci per le trasmissioni.

Similarmente, limitiamo l'organizzazione temporale nel modo seguente:
- l'organizzatore deve specificare una fase di iscrizione e una fase di svolgimento, entrambe delimitate da due date ciascuna;
- è possibile creare squadre e partecipare a squadre esistenti solo durante la fase di iscrizione, terminata la quale le squadre vengono bloccate e il torneo può avere inizio;
- allo stesso modo, è possibile registrare partite come accadute solo durante la fase di svolgimento, così da permettere ad aspiranti partecipanti di farsi un'idea del periodo in cui il torneo si disputerà e dare loro modo di organizzarsi.
Tuttavia, non rimuoviamo la possibilità di sovrapporre le due fasi o modificare le date in seguito, al fine di dare la massima libertà possibile agli organizzatori.

Come menzionato, dall'entità torneo dobbiamo derivare altre due entità fondamentali, le squadre e le partite.
- Ogni squadra sarà caratterizzata dai tipici attributi: un nome, un tag (costituito da 2 a 4 caratteri presenti nel nome) e, eventualmente, un logo. La scelta di design più importante relativamente alle squadre però è la seguente: ogni utente può partecipare a N tornei, e in ciascuno può creare al massimo una squadra. Per questo motivo, ogni squadra è definita in base al proprio fondatore e al torneo a cui partecipa.
- Ogni partita è caratterizzata da una data e ora di svolgimento, e una durata prevista in minuti. Per partita si può intendere sia una partita già svolta, che una attualmente in corso, che una fissata per il futuro, ragion per cui dobbiamo adattare l'implementazione a queste esigenze. Le partite contengono riferimenti a entrambe le squadre e conteggi dei punteggi, da usare in caso di serie (incontri dove più di una partita viene giocata). I conteggi sono facoltativi, permettendo quindi di fissare partite senza conoscere il punteggio finale. Inoltre, il design dell'entità partita, unito alla libertà di impostazione degli attributi temporali dei tornei, permettono agli organizzatori anche di sfruttare la piattaforma come un archivio di tornei passati, e registrare eventi già accaduti al di fuori del portale.
	- Nota: per i fini della nostra implementazione, solo serie dispari sono supportate, in quanto il calcolo successivo delle classifiche non ammette pareggi.

La parte più importante del progetto sono però i giocatori, per cui aggiungiamo altre due entità: i player e le richieste.
- Così come un utente può creare più squadre, allo stesso modo un utente può partecipare a più squadre contemporaneamente, fintanto che si trovano tutte in tornei diversi. Di conseguenza, svilupperemo l'entità giocatore come una connessione tra un utente e una squadra, affidando all'applicativo la gestione delle eccezioni.
- Per regolare l'organizzazione delle squadre, si è optato per una semplice soluzione: fintanto che il massimo di giocatori non è stato raggiunto, qualsiasi utente può inviare a una squadra una richiesta di entrata. La richiesta viene poi consegnata al proprietario della squadra, che provvede ad accettarla o rifiutarla (il mittente può anche annullare la richiesta in un secondo momento, fintanto che non è stata già accettata o rifiutata). Si può considerare quindi la richiesta come un potenziale player, ragion per cui presenterà gli stessi attributi: un riferimento al giocatore e un riferimento alla squadra.

# Rappresentazione intermedia

La seguente lista rappresenta fedelmente l'implementazione eseguita tramite modelli Django.

- Users: gli utenti.
	- credenziali:
		- username alfanumerico
		- password
	- nome di display
	- ruolo condizionale di organizzatori, che può essere conferito a ciascun utente dagli amministratori, e permette di organizzare tornei.
- Disciplines: i titoli sui quali si disputeranno i tornei.
	- nome di display
- Tournaments: i tornei.
	- id dell'utente organizzatore
	- nome di display
	- una serie di date:
		- data di apertura delle iscrizioni
		- data di chiusura delle iscrizioni
		- data di apertura delle partite
		- data di chiusura delle partite
	- id della disciplina
	- limiti:
		- numero massimo di squadre
		- numero massimo di giocatori
	- link esterni:
		- piattaforma di streaming
		- piattaforma di ritrovo
- Team: le squadre di utenti che partecipano insieme a un torneo.
	- nome di display
	- tag: serie di poche lettere, generalmente incluse nel nome, usata durante il gioco come rimpiazzo del nome intero.
	- id dell'utente proprietario della squadra
	- id del torneo a cui è relativa la squadra
	- logo, facoltativo.
- Game: le partite disputate tra le squadre di un torneo.
	- id delle due squadre:
		- squadra 1
		- squadra 2
	- punteggi delle due squadre:
		- punteggio squadra 1
		- punteggio squadra 2
	- data e ora di inizio della partita
	- durata prevista della partita, in minuti
	- id del torneo a cui è relativa la partita
- Player: le associazioni tra gli utenti e le squadre di cui fanno parte.
	- id dell'utente
	- id della squadra
- Request: le richieste in attesa inviate dai giocatori ai proprietari delle squadra alle quali vogliono unirsi.
	- id degli utenti:
		- mittente
		- destinatario
	- id della squadra.

Ogni entità è inoltre identificata da un ID esadecimale di 12 cifre.

- - -
![[Diagramma ER.png]]
- - -
_rappresentazione grafica del diagramma ER._

# Scelte di implementazione

Nonostante non tutte le entità ne avessero necessità, si è deciso di assegnare a tutte un id esadecimale, così da aumentare la consistenza e favorire l'indicizzazione dei modelli per la consultazione via piattaforma admin.

Tutte le entità a eccezione di games, requests e players sono da considerarsi concrete, e come tali sono caratterizzate da un nome di display.
Le entità astratte sono invece connessioni concettuali tra entità concrete (spesso molti a molti)
- una partita rappresenta la congiunzione tra due squadre che si scontrano;
- un giocatore rappresenta la congiunzione tra un utente e la squadra di cui fa parte;
- una richiesta rappresenta la congiunzione tra un utente e la squadra di cui vuole fare parte.
Per questo motivo, non vi è necessità di nomenclatura, e quando si presenta, è possibile fare uso delle entità che le compongono: ad esempio, il nome di una partita sarà team1.tag vs team2.tag (NVE vs SOI), mentre il nome di un giocatore sarà team1.tag user.name (NVE Turty).

Si è scelto di denormalizzare leggermente il database, aggiungendo ripetizioni ove potesse aiutare performance e intuitività durante lo sviluppo:
- le richieste comprendono anche l'utente destinatario, per facilitarne il recupero da parte del proprietario della squadra;
- le partite comprendono anche il torneo, nonostante sia desumibile da una qualsiasi delle due squadre coinvolte, per una motivazione analoga.

Per l'autenticazione, si è optato per una combinazione di username alfanumerico e password, con l'utilizzo di JWT (Java Web Token) nell'implementazione. La dualità di attributi nominali dell'utente consente di avere un nome visibile complesso e libero, mantenendo tuttavia la semplicità di immissione del nome di login.

La nomina degli organizzatori è riservata esclusivamente agli amministratori, i quali possono elevare ad organizzatore qualsiasi utente tramite la piattaforma admin fornita da Django, con la semplice attivazione di un attributo booleano.

Adotteremo la filosofia CRUD (Create, Read, Update, Destroy) per pressoché tutte le entità relative al progetto.
# 3 - Implementazione

# Backend

Sfruttando Django e DRF, è necessario suddividere l'implementazione in progetti e applicazioni.
Ai fini del nostro portale, un approccio a singola applicazione è la soluzione adeguata, in quanto non ci sono partizioni delle entità del database particolarmente isolate, e di conseguenza nessuna esigenza particolare di generare più app.

### Django Project: daimon_esports

Nel progetto particolare rilevanza nutrono il file settings.py, contenente le impostazioni essenziali di Django, e il file urls.py, dove verranno specificati tutti gli entrypoint della nostra API in DRF.

#### Settings.py

Nonostante non sia raccomandato in ambito di produzione, per mantenere la dimostrazione semplice e non introdurre un proxy nel sistema si è deciso di mantenere la variabile `DEBUG` impostata su `true`. Siamo consapevoli di ciò che comporta, ma per i fini del progetto, lo consideriamo un compromesso accettabile.

Altre impostazioni degne di nota sono gli `ALLOWED_HOST`, limitati a `localhost` e `127.0.0.1` per consentire l'accesso unicamente da locale, le `INSTALLED_APPS`, dove abbiamo incluso tutti i moduli di cui faremo uso (in particolare la nostra app, DRF, l'estensione di DRF mirata ai JWT, e corsheaders, per prevenire difficoltà legate a CORS), l'impostazione degli URL e i ROOT per gestire file statici e file generati dagli utenti (i loghi delle squadre), le impostazioni per l'autenticazione con JWT, le impostazioni per CORS, e la configurazione dei logs.

#### Urls.py

Nel file degli URL troviamo tutte le rotte che l'applicativo esporrà all'internet pubblico. Di seguito riassumiamo graficamente l'albero di rotte:

- - -
![[Urls_Users.png]]
- - -
_utenti_

- - -
![[Urls_Tournaments.png]]
- - -
_tornei_

- - -
![[Urls_Teams.png]]
- - -
_squadre_

- - -
![[Urls_Games.png]]
- - -
_partite_

- - -
![[Urls_Other.png]]
- - -
_giocatori, richieste, discipline, piattaforma admin e root_

Nella scelta delle rotte da fornire, identifichiamo una serie di polizze:

- ogni URL deve essere completo, anche se non sono implementati tutti gli anelli della catena (ad esempio, /players/ e /players/id/ non sono implementati, solo /players/id/delete/).
- ogni elemento deve esporre le seguenti 4 operazioni:
	- create
	- <id\>/<property\> (read)
	- modify/<property\> (update)
	- delete
- ogni elemento viene definito al plurale.

Ci sono tuttavia alcune eccezioni:

- Essendo l'utente un'entità di competenza esclusiva del proprietario di suddetto utente, nessuna delle rotte relative agli utenti richiede di specificare l'id, in quanto verrà recuperato durante l'autorizzazione della richiesta. Inoltre, proprio per questo motivo, le rotte per gli utenti sono tutte definite al singolare.
- /user/create/ è rinominata a /user/register/ per conformarsi allo standard
- Le discipline non sono modificabili se non dagli amministratori, per cui ci interessa solamente implementare una singola rotta di get.
- Per esigenze di implementazione, sono state realizzate alcune rotte che non ricadono in nessuna delle categorie soprastanti. In particolare:
	- /tournaments/<id\>/cansubscribe: un controllo lato server che verifica se l'utente può iscriversi al torneo relativo all'id. Utile per ridurre i controlli necessari al frontend per nascondere all'utente funzionalità che potrebbe non avere il permesso di utilizzare.
	- /user/login: per effettuare il login.
	- /request/<id\>/accept: sia accept che delete risultano nell'eliminazione della richiesta. La differenza è che con accept, viene attivato l'effetto collaterale che gestisce l'inserimento del giocatore nel team. Inoltre, solo il destinatario di una richiesta può accettarla, mentre sia mittente che destinatario possono cancellare una richiesta, sebbene sul frontend l'operazione venga definita in due modi diversi (cancellazione e rifiuto).
	- /admin: per accedere alla piattaforma admin.
	- /tournaments/search: l'endpoint del motore di ricerca tornei, usato dagli spettatori per interrogare il database alla ricerca di eventi.

Il file urls.py ospita poi una regola speciale per servire i file statici, cosa che è resa possibile mantenendo DEBUG a true.

Tutte le rotte al di fuori della piattaforma admin fanno riferimento a una delle viste definite nella App, che analizziamo di seguito.

### Django App: daimon_esports_app

#### models.py

Il file models.py ospita tutti i modelli, ovvero la rappresentazione in codice Python delle tabelle del database. Avendo già esposto adeguatamente il diagramma del database nel precedente capitolo, ci concentriamo su alcune note:

- abbiamo creato una funzione, generate_hex_id, apposita per la generazione di identificatori casuali, usata da tutti i modelli. Ciascun modello, inoltre, esegue un controllo sulla rispettiva tabella, per verificare che non esista già un oggetto con lo stesso id (la probabilità è remota, ma non si sa mai).
- è presente la classe UserManager, usata dal sistema di autenticazione default di Django per gestire il modello utente, e funziona in tandem con il nostro modello personalizzato per garantire le capacità di autenticazione dell'app.

#### serializers.py

I Serializers sono un costrutto di DRF usato per decifrare input json in arrivo dal frontend e generare oggetti sulla base delle informazioni ricevute (e viceversa). La nostra implementazione corre quasi del tutto parallela all'insieme di modelli definiti nel file models.py, eccetto per alcuni dettagli importanti:

- avendo definito un livello di profondità di 1 per ciascuno dei serializers, è necessario mantenere due serializers per ogni oggetto che necessita di essere creato e letto, in quanto mantenerne uno solo significherebbe dover fornire al serializer qualsiasi riferimento esterno per intero. In questo modo, invece, possiamo limitarci a specificare lato client l'id dell'oggetto a cui ci si sta riferendo, e il serializer non creerà problemi.
- è stato personalizzato il serializer degli utenti, per impedire invii rischiosi della password, convalidarla in occasione di operazioni di autenticazione e prevenire l'impostazione illegale del ruolo di organizzatore.

#### views.py

Il file views.py è dove la maggior parte dell'implementazione del backend risiede: ogni url trasmette le richieste ricevute a una delle viste definite qui, le quali vengono poi elaborate al fine di eseguire operazioni sul database e/o inviare risposte al client.

Ogni vista sfrutta poi uno dei serializers definiti nell'apposito file per convertire i dati tra JSON e oggetti relativi ai modelli.

In particolare, compito assegnato alle viste è effettuare dei controlli di integrità su tutto l'input in entrata, affinchè tutte le operazioni svolte siano effettivamente autorizzate dall'identità dell'utente e dai constraints imposti dal design del sistema.

Ad esempio, la classe UserRegister esegue i seguenti controlli sui dati in entrata:

- il nome non deve essere già in uso, troppo lungo o troppo corto
- l'username non deve essere già in uso, troppo lungo o troppo corto, e deve essere alfanumerico
- la password non deve essere troppo lunga o troppo corta

Gli stessi controlli vengono effettuati separatamente da ciascuna delle viste che regolano invece la modifica dei singoli attributi.

#### admin.py

Il file admin.py è cruciale per la corretta visualizzazione e modifica degli elementi del database dalla piattaforma admin. Ogni classe in esso definita ha sintassi molto simile a quella delle classi serializer, dato che entrambi i concetti svolgono lo stesso ruolo: stabiliscono quali proprietà di ciascun modello devono essere gestite in quale modo. Nel nostro caso, ci limitiamo a nascondere l'id, in quanto non necessario per eseguire la maggior parte delle operazioni.

#### tests.py

In questo file abbiamo implementato una serie di test relativi ai modelli, al fine di verificare che tutte le operazioni diano il risultato sperato. Per ogni modello, vengono svolti i seguenti test:

- creazione
- generazione di id univoco
- rappresentazione sotto forma di stringa

# Frontend

Il frontend è implementato in NextJS, ed è provvisto di tutte le viste necessarie per un utilizzo completo della piattaforma.
Un notevole vantaggio di NextJS rispetto al suo predecessore, ReactJS, è la nuova /app directory, tramite la quale è possibile specificare molteplici pagine, tornando a un sistema analogo all'implementazione originaria di PHP, primo fra tutti. Questo consente di organizzare il contenuto del sito in maniera più articolata e intuitiva, simile alla struttura effettiva delle pagine visibili da browser.

Homepage: pagina per visualizzare un'anteprima dei contenuti più recenti, provvista dei collegamenti necessari per accedere al resto della piattaforma.
- Account: pagina per visualizzare e modificare tutte le impostazioni del proprio account, inclusa l'eliminazione.
	- Inbox: pagina per visualizzare, accettare e cancellare tutte le richieste in entrata e in uscita, con la possibilità di filtrare le richieste in arrivo in base alla squadra destinataria (utile per utenti titolari di molteplici squadre)
	- Login: pagina per eseguire il login, con un comodo link alla pagina di registrazione per chi ancora non possiede un account.
	- Register: pagina per eseguire la registrazione, con un comodo link alla pagina di login per chi ancora non possiede un account.
	- Teams: lista di squadre di cui l'utente fa parte.
	- Tournaments: lista di tornei organizzati dall'utente.
- Game
	- <id\>: pagina per visualizzare i dati della partita contrassegnata dall'id specifico, incluse le squadre coinvolte, i punteggi e il torneo di appartenenza. Se la partita è in corso, viene visualizzata anche la trasmissione dal vivo relativa.
		- Settings: pagina riservata al proprietario del torneo di cui la partita fa parte, usata per modificarne le impostazioni.
	- Create
		- <id\>: pagina riservata al proprietario del torneo contrassegnato dall'id specifico, usata per creare una nuova partita appartenente a suddetto torneo.
- Team
	- <id\>: pagina per visualizzare i dati della squadra contrassegnata dall'id specifico, inclusi i membri, il torneo di appartenenza e il proprietario.
		- Settings: pagina riservata al proprietario della squadra, usata per modificarne le impostazioni.
	- Create
		- <id\>: pagina usata per creare una squadra appartenente al torneo contrassegnato dall'id specifico.
- Tournament
	- <id\>: pagina per visualizzare i dati del torneo contrassegnato dall'id specifico, incluse le squadre, le date e la piattaforma di streaming.
		- Settings: pagina riservata al proprietario del torneo, usata per modificarne le impostazioni.
	- Create: pagina riservata agli organizzatori per creare un nuovo torneo.
	- Search: pagina provvista di barra di ricerca e numerosi filtri e controlli, per visualizzare a piacimento i tornei registrati sulla piattaforma.

### Funzionalità specifiche e scelte di sviluppo

- Not Found: il progetto è provvisto di una pagina default, visualizzata in caso di accesso a un url non definito.
- Su ogni pagina riservata a un utente autenticato, è presente un controllo che rimanda l'utente non autenticato alla pagina di login.
- Ogni operazione altamente distruttiva (eliminare un account, cancellare un torneo, sciogliere un team ecc.) attiverà un popup di conferma, per prevenire eliminazioni accidentali da parte degli utenti.
- Ogni azione presenta un feedback grafico nella forma di una notifica a schermo, così da fornire all'utente la conferma immediatadell'esito della propria azione; in caso di errore, la notifica riporta l'errore emesso dal backend.
- Ogni pagina presenta in alto a sinistra un pulsante per ritornare alla pagina principale, ad eccezione della pagina principale stessa.
- Il frontend sfrutta un context provider per mantenere globali variabili e metodi utilizzati dalla maggior parte dei componenti, quali contenuto e gestione di notifiche e popup, token di autenticazione e identità dell'utente. Questo semplifica la struttura del codice e previene pratiche malsane come il prop drilling.
- Alcune pagine (home, tornei e squadre) presentano uno speciale header, che riproduce la funzionalità chiave menzionata nell'introduzione: una lista scorribile in entrambe le direzioni di partite passate, in corso e future, opportunamente filtrate in base al contesto della pagina. Le stesse pagine inoltre presentano un'anteprima della trasmissione in diretta della partita in corso iniziata più di recente.
- per tutte le chiamate API è stata selezionata la libreria axios, la quale permette di effettuare chiamate di qualsiasi tipo a qualsiasi backend.
- per l'aspetto grafico si è optato per l'utilizzo di CSS puro: sebbene NextJS presenti compatibilità innata con Tailwind, l'utilizzo di CSS permette un controllo più fine sui componenti dal funzionamento meno ortodosso, come l'header scorribile menzionato in precedenza.
- per la maggior parte delle funzionalità presenti in più pagine, si è optato per la realizzazione di componenti a funzione che potessero essere riutilizzati ovunque tramite il passaggio di semplici parametri.
- Uso di TypeScript: specialmente nel contesto delle chiamate API, l'uso di TypeScript è stato cruciale, in quanto ha permesso di identificare immediatamente potenziali problemi di comunicazione tra frontend e backend, in caso di attributi con tipizzazioni ambigue (in particolare date e timestamps).
# 4 - Risultati

Al primo collegamento, la piattaforma si presenta in questa forma: in alto a sinistra il tasto di login, in alto a destra la barra di ricerca, immediatamente sotto la cronologia di partite, e in caso in cui una partita sia tuttora in corso, la preview della diretta ancora più in basso.

Notare la differenza di colori per le partite dell'header:
- azzurro scuro per le partite passate
- rosso acceso per le partite in corso
- azzurro chiaro per le partite in arrivo

![[Pasted image 20240902180326.png]]

Premendo sul tasto di login, si accede alla pagina di accesso, nella quale possiamo notare anche la presenza del pulsante di ritorno alla homepage.

![[Pasted image 20240902180553.png]]

Qualora la password fosse errata, si riceverà la seguente notifica:

![[Pasted image 20240902180640.png]]

La pagina di registrazione presenta una schermata analoga, con un messaggio a schermo in caso in cui le due ripetizioni della password fossero incongruenti.

![[Pasted image 20240902180734.png]]

La pagina dell'account è piuttosto semplice: ogni caratteristica è mostrata e accompagnata da un tasto per modificarla.

![[Pasted image 20240902181105.png]]

In caso si voglia cancellare l'account, è presente un popup di verifica:

![[Pasted image 20240902182521.png]]

La inbox è provvista di un filtro per selezionare le richieste in base al team.

![[Pasted image 20240902182018.png]]

La pagina per le partite presenta in prima vista i loghi e, qualora la partita sia in corso, la preview della diretta:

![[Pasted image 20240902182119.png]]

Altre informazioni presenti nella pagina delle partite:

![[Pasted image 20240902182132.png]]


La pagina del torneo mostra gli standings:

![[Pasted image 20240902182325.png]]

E la lista di partite filtrata in base al torneo:

![[Pasted image 20240902182403.png]]

La pagina della squadra mostra il logo e i partecipanti:

![[Pasted image 20240902182431.png]]
# 5 - Conclusione

Nel suo stato attuale, la piattaforma costituisce un buon punto di riferimento per qualsiasi orgnaizzatore di tornei e squadre, nonchè per giocatori e spettatori in cerca di nuovi eventi.

Allego una lista di potenziali funzionalità interessanti, omesse in questa iterazione della piattaforma:

- controllo avanzato anti-spoiler per le partite;
- collegamento di squadre su tornei diversi sotto lo stesso brand;
- collegamento a API ufficiali dei titoli supportati per mostrare le statistiche;
- sistema grafico di gironi e bracket gestito internamente alla piattaforma;
- sistema di notifiche acustiche browser, per venire notificati all'arrivo di nuove richieste.
# Bibliografia

- [Esports Charts](https://escharts.com)
- [LoL Esports](https://lolesports.com)
- [Valorant Esports](https://valorantesports.com)
- [Start.gg](https://www.start.gg)
- [Wayback Machine](https://web.archive.org)
- [AWS](https://aws.amazon.com)

# Tecnologie

- [TypeScript](https://www.typescriptlang.org)
- [NodeJS](https://nodejs.org/en)
- [ReactJS](https://react.dev)
- [NextJS](https://nextjs.org)
- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com)
- [DRF](https://www.django-rest-framework.org)
- [Docker](https://www.docker.com)
- [Alpine](https://alpinelinux.org)
- [Axios](https://axios-http.com)