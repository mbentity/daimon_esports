
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