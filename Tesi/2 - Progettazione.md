
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