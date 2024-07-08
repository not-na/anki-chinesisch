# Anki Chinesisch Deck

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI tests status badge](https://github.com/not-na/anki-chinesisch/actions/workflows/test.yaml/badge.svg)


Anki Deck for learning Mandarin from German, based on language courses offered by
TU Berlin ZEMS. Note that this deck and the rest of the documentation are in german, as
it is primarily meant for german speakers.

## Verwendung

Die jeweils neueste Version kann in den
[GitHub Releases](https://github.com/not-na/anki-chinesisch/releases/latest) heruntergeladen
und manuell installiert werden. Dazu die Datei nach dem Herunterladen via `File > Import...` bzw.
`Datei > Importieren ...` importieren. Die Standardeinstellungen sind in der Regel ausreichend.

Die auf [AnkiWeb veröffentlichte Version](https://ankiweb.net/shared/info/1038468378) ist
eventuell nicht immer aktuell, es wird empfohlen das Deck wie oben beschrieben direkt herunterzuladen.

Zum Updaten auf eine neuere Version kann das Deck in der Regel einfach neu importiert werden,
Anki sollte dabei automatisch Änderungen anwenden. Bitte **vor** dem Updaten die entsprechenden
Release-Notes lesen, falls es besondere Dinge zu beachten gibt. Sonst könnte möglicherweise
Lernfortschritt verloren gehen.

Für fortgeschrittene Nutzer gibt es auch die Möglichkeit, das Deck mittels CrowdAnki
direkt aus dem Repository zu installieren. Grob zusammengefasst sollte dafür das
Repository in ein lokales Verzeichnis [gecloned](https://github.com/git-guides/git-clone)
werden und danach mittels des `File > CrowdAnki: Import from disk` Befehls (Details
[hier](https://github.com/Stvad/CrowdAnki#import)) importiert werden.

## CrowdAnki

Dieses Repository nutzt [CrowdAnki](https://ankiweb.net/shared/info/1788670778), ein
Anki-Addon, welches kollaboratives Bearbeiten von Anki Decks via
[Git](https://git-scm.com/) ermöglicht. 

**CrowdAnki ist nicht notwendig wenn das Deck lediglich benutzt werden soll ohne
Bearbeitungen vorzunehmen, siehe dazu Abschnitt [Verwendung](#verwendung) weiter oben.**

Um Änderungsvorschläge (Pull Requests) einzureichen, ist CrowdAnki notwendig. Für nicht
Git-erfahrene Nutzer wird empfohlen, Änderungen und Korrekturen als
[neuen Issue](https://github.com/not-na/anki-chinesisch/issues/new) einzureichen, welche
dann manuell umgesetzt werden können. Hierfür ist logischerweise kein CrowdAnki und auch
keine Git-Erfahrung notwendig.

### AnkiDroid und andere mobile Apps

Da es manchmal Probleme dabei gibt, Anki Decks manuell in mobile Apps zu importieren, wird
der Import via Anki Desktop empfohlen. Danach kann das Deck sehr einfach mittels eines kostenlosen
AnkiWeb-Accounts auf das Smartphone synchronisiert werden.

## Beitragen

Entweder per Issue oder per Pull Request.

Kurfassung für Pull Requests: Repository forken, Änderungen vornehmen, CrowdAnki-Export in geforktes
lokales Repository, Änderungen committen und pushen, Pull Request von eigenem Repository
an dieses Repository stellen, auf Merge warten.

TODO: Mehr details, styleguide etc.
