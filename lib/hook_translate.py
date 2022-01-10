# -*- coding: utf-8 -*-
# get language for hooks
def lang():
    from pyrevit.userconfig import user_config
    language_list = [
        "EN",
        "SK",
        "DE",
        "FR",
        ]
    try:
        lang_index = user_config.CustomToolsSettings.language
    except:
        user_config.CustomToolsSettings.language = def_language
        lang_index = def_language

    return language_list[lang_index]

# dictionary of texts in the hooks in various languages
# do not edit manually, this dictionary is created from an airtable base
# all changes should be made there
hook_texts = {
# SLOVAK
"SK":{
"Shared Parameters":{
"text":
"POZOR!\n\n\
Pri vytváraní nového Shared Parametru si najskôr pozrite, či už podobný parameter nie je vytvorený.\n\n\
- Použite funkciu 'Shared Parameter Schedule'.\n\
- Nepoužívajte diakritiku.",
"buttons":
["Zobraziť zoznam Shared Parametrov na Wiki",
"Upraviť Parametre",
"Zrušiť"],
},
"Revit Build":{
"text":
"POZOR!\n\n\
Používaš zlý Revit Build! To môže poškodiť model.\n\
\n\
Správne Revit Buildy sú ",
"buttons":
["Chcem len otvoriť súbor bez synchronizácie",
"Ako môžem tento problém opraviť?"],
},
"View, Schedule or Sheet Deletion":{
"text":
"POZOR!\n\n\
Chceš naozaj vymazať tieto Views?\n",
"buttons":
["Zrušiť",
"Delete"],
},
"Save List Of Opened Views":{
"text":
"Chceš uložiť zoznam otvorených Views?",
"buttons":
["Uložiť",
"Preskočiť",
"Zistiť viac"],
},
"Roof by Extrusion":{
"text":
"POZOR!\n\n\
Roof By Extrusion by sa mali používať len výnimočne.\n\
Ak potrebuješ spraviť strechu v spáde, použi Floor a nastav spád.\n\
Strechám vymodelovaným ako Roof by Extrusion sa nedá upraviť pôdorysný obrys inak ako Voidom.",
"buttons":
["Vytvoriť Roof by Extrusion",
"Zrušiť",
"Viac info o Roof by Extrusion"],
},
"Load Family":{
"text":
"POZOR!\n\n\
Family by mala mať veľkosť pod 1 MB.\n\
Pred naloadovaním si vždy skontroluj veľkosť súboru.\n\n\
Nie je Family príliš detailne vymodelovaná?",
"buttons":
["Zrušiť",
"Naloadovať",
"Viac info o veľkosti Families"],
},
"Link CAD file in 3D":{
"text":
"POZOR!\n\n"
"Nezašrktol si možnosť 'Current View Only'.\n"
"Tým pádom linkuješ CAD súbor do 3D!",
"buttons":
["Zrušiť",
"OK, potrebujem DWG v 3D",
"Viac info o Linkovaní CAD súborov"],
},
"Link CAD file":{
"text":
"POZOR!\n\n\
CAD súbory môžu poškodiť revitový model.\n\
Spravil si všetko podľa návodu nižšie?",
"buttons":
["Link CAD",
"Zrušiť",
"Viac info o Linkovaní CAD súborov"],
},
"In Place Family":{
"text":
"POZOR!\n\n\
In Place Families by mali byť použité len vo výnimočných prípadoch,\n\
keďže majú oproti Loadable Families veľa nevýhod: \n\
- problematické vykazovanie\n\
- nemajú identifikáciu o levele, na ktorom sú umiestnené\n\
- pri skopírovaní prvku vzniká nový nezávislý originál\n\
- nemožnosť modelovať parametricky\n\n\
Chceš naozaj vytvoriť In Place Family?",
"buttons":
["Vytvoriť",
"Zrušiť",
"Viac info o In Place Families"],
},
"Import CAD file":{
"text":
"POZOR!\n\n\
Importovať CAD súbory by si mal len výnimočne.\n\
Nikdy neimportuj CAD priamo do modelu, ale do čistého RVT súboru.\n\n\
Si si istý, že vieš, čo robíš?",
"buttons":
["Importovať",
"Zrušiť",
"Viac info o Importovaní CAD súborov"],
},
"Unpin":{
"text":
"POZOR!\n\n\
Chceš naozaj odpinovať tento element?\n\
Elementy sú väčšinou zapinované kvôli tomu, aby nimi náhodou niekto nepohol.\n\n\
Chceš to naozaj urobiť?",
"buttons":
["Unpin",
"Zrušiť",
"Viac info o Pin/Unpin"],
},
"Project Parameters":{
"text":
"POZOR!\n\n\
Pri vytváraní nového Shared Parametru si najskôr pozrite, či už podobný parameter nie je vytvorený. Nepoužívajte diakritiku.\n\n\
- Použite funkciu 'Shared Parameter Schedule'.\n\
- Nepoužívajte diakritiku.",
"buttons":
["Zobraziť zoznam Shared Parametrov na Wiki",
"Upraviť Parametre",
"Zrušiť"],
},
"Ramp":{
"text":
"POZOR!\n\n\
Rampy je lepšie modelovať ako Floor v spáde.\n\
- rampy nemajú možnosť pridávať vrstvy\n\
- na rampy sa nedá umiestniť šípka spádu ani plavák (pred Revitom 2022)\n\
- Rampy nepodporujú Structural parametre\n\
- v budúcnosti bude musieť po tebe niekto rampu premodelovať na Floor",
"buttons":
["Aj napriek tomu vytvoriť rampu",
"Zrušiť",
"Viac info o kategórii Ramp"],
},
"Architectural column":{
"text":
"POZOR!\n\n\
Všetky nosné stĺpy by mali byť vymodelované ako Structural a nie ako Architectural Column.\n\
- Architectural Columns sa nezobrazia v statickom modeli.\n\
- v budúcnosti bude musieť niekto po tebe upraviť všetky stĺpy na Structural",
"buttons":
["Vytvoriť aj napriek tomu Architectural Column",
"Zrušiť",
"Viac info o Architectural Columns"],
},
},
# ENGLISH
"EN":{
"Shared Parameters":{
"text":
"WARNING!\n\n\
When you create a new Shared Paramter, first see if a similar parameter is already created.\n\n\
- Use the 'Shared Parameter Schedule' tool.\n\
- Do not use accented characters.",
"buttons":
["View Shared Parameter  list on Wiki",
"Edit Parameters",
"Cancel"],
},
"Revit Build":{
"text":
"ATTENTION!\n\n\
You're using the wrong Revit Build! It can damage the model.\n\
\n\
The correct Revit Builds are ",
"buttons":
["I just want to open the file without syncing",
"How can I fix this problem?"],
},
"View, Schedule or Sheet Deletion":{
"text":
"WARNING!\n\n\
Do you really want to delete these views?\n",
"buttons":
["Cancel",
"Delete"],
},
"Save List Of Opened Views":{
"text":
"Do you want to save a list of open Views?",
"buttons":
["Save",
"Skip",
"Learn more"],
},
"Roof by Extrusion":{
"text":
"WARNING!\n\n\
Roof By Extrusion should be used only in excepional cases.\n\
If you need to model Sloped roof use Roof or Floor tool with defined slope.\n\
The floor plan boundaries of Roofs by Extrusion can be changed only using Voids",
"buttons":
["Create Roof by Extrusion",
"Cancel",
"More info about Roof by Extrusion"],
},
"Load Family":{
"text":
"WARNING!\n\n\
Family should be as small as possible. Preferably under 1 MB in size.\n\
Always check the file size before uploading.\n\n\
Isn't Family overmodelled?",
"buttons":
["Cancel",
"Load",
"More info about Family size"],
},
"Link CAD file in 3D":{
"text":
"WARNING!\n\n"
"You did not check the 'Current View Only' option.\n"
"You're linking a CAD file to 3D!",
"buttons":
["Cancel",
"OK, I need DWG in 3D",
"More info about Linking CAD files"],
},
"Link CAD file":{
"text":
"WARNING!\n\n\
CAD files can corrupt revit model.\n\
Did you follow the workaround on the link below?",
"buttons":
["Link CAD",
"Cancel",
"More info about linking of CAD files"],
},
"In Place Family":{
"text":
"WARNING!\n\n\
In Place Families should be used only in exceptional cases,\n\
hence they have lot of disadvantages:\n\
- problematic scheduling options\n\
- no Level asigned\n\
- each copy is independent family instance\n\
- limited support for parametric modeling\n\n\
Do you really want to create In Place Family?",
"buttons":
["Create",
"Cancel",
"More info about In Place Families"],
},
"Import CAD file":{
"text":
"WARNING!\n\n\
You should only import CAD files in exceptional cases.\n\
Never import CAD file directly into the model, but into a clean RVT file.\n\n\
Are you sure you know what you are doing?",
"buttons":
["Import",
"Cancel",
"More info about CAD file imports"],
},
"Unpin":{
"text":
"WARNING!\n\n\
Do you really want to unpin this element?\n\
Elements are usually pinned to prevent someone from accidentally moving them.\n\n\
Do you really want to do this?",
"buttons":
["Unpin",
"Cancel",
"More info about Pin/Unpin"],
},
"Project Parameters":{
"text":
"WARNING!\n\n\
When you create a new Shared Paramter, first see if a similar parameter is already created.\n\n\
- Use the 'Shared Parameter Schedule' tool.\n\
- Do not use accented characters.",
"buttons":
["View Shared Parameter  list on Wiki",
"Edit Parameters",
"Cancel"],
},
"Ramp":{
"text":
"WARNING!\n\n\
It is better to model Ramps as Floors with defined slope.\n\
- ramps have no options for creating layers\n\
- you cannot place a Spot Slope nor Spot Elevation on Ramps (prior to revit 2022)\n\
- no structural parameters\n\
- someone will have to change all of the Ramps to Floors in the future",
"buttons":
["Despite of that, Create the Ramp",
"Cancel",
"More info about the Ramp Category"],
},
"Architectural column":{
"text":
"WARNING!\n\n\
In general, Columns should be modeled as Structural Columns not as Architectural Columns.\n\
- Architectural Columns don't appear in the structural model.\n\
- Someone will have to change all the Architectural Columns to Structrural Columns in the Future.",
"buttons":
["Despite of that, create the Architectural Column",
"Cancel",
"More info about Architectural Columns"],
},
},
# GERMAN
"DE":{
"Shared Parameters":{
"text":
"WARNUNG!\n\n\
Wenn Sie einen neuen gemeinsam genutzten Parameter erstellen, prüfen Sie zunächst, ob ein ähnlicher Parameter bereits erstellt wurde.\n\n\
- Verwenden Sie das Werkzeug 'Liste gemeinsam genutzte Parameter'.\n\
- Verwenden Sie keine Akzente.",
"buttons":
["Liste gemeinsam genutzter Parameter im Wiki anzeigen",
"Parameter bearbeiten",
"Abbrechen"],
},
"Revit Build":{
"text":
"ACHTUNG!\n\n\
Sie verwenden den falschen Revit Build! Das Modell könnte beschädt werden.\n\
\n\
Die richtigen Revit Builds sind ",
"buttons":
["Ich möchte die Datei nur öffnen, ohne sie zu synchronisieren",
"Wie kann ich dieses Problem beheben?"],
},
"View, Schedule or Sheet Deletion":{
"text":
"WARNUNG!\n\n\
Wollen Sie dieses Ansichten wirklich löschen?\n",
"buttons":
["Abbrechen",
"Löschen"],
},
"Save List Of Opened Views":{
"text":
"Möchten Sie eine Liste der offenen Ansichten speichern?",
"buttons":
["Speichern",
"Überspringen",
"Mehr erfahren"],
},
"Roof by Extrusion":{
"text":
"WARNUNG!\n\n\
Dach über Extrusion sollte nur in Ausnahmefällen verwendet werden.\n\
Wenn Sie das Dach mit einer Neigung versehen müssen, verwenden Sie Geschossdecken und legen Sie die Neigung fest.\n\
Bei Dächern, die als Dach über Extrusion modelliert wurden, kann die Plankontur nur mit einem Abzugskörper angepasst werden.",
"buttons":
["Dach über Extrusion erstellen",
"Abbrechen",
"Mehr Informationen über Dach über Extrusion"],
},
"Load Family":{
"text":
"WARNUNG!\n\n\
Die Familie sollte kleiner als 1 MB sein.\n\
Prüfen Sie immer die Dateigröße vor dem Laden ins Modell.\n\n\
Ist die Familie nicht übermodelliert?",
"buttons":
["Abbrechen",
"Laden",
"Mehr Infos zur Familiengröße"],
},
"Link CAD file in 3D":{
"text":
"WARNUNG!\n\n"
"Sie haben die Option 'Nur aktuelle Ansicht' nicht aktiviert.\n"
"Sie verknüpfen eine CAD-Datei in das 3D Modell!",
"buttons":
["Abbrechen",
"OK, ich brauche DWG in 3D",
"Mehr Informationen über die Verknüpfung von CAD-Dateien"],
},
"Link CAD file":{
"text":
"WARNUNG!\n\n\
CAD Dateien können das Revitmodell beschädigen.\n\
Haben Sie den Workaround des u.a. Links befolgt?",
"buttons":
["CAD verknüpfen",
"Abbrechen",
"Mehr über das Verknüpfen von CAD Dateien"],
},
"In Place Family":{
"text":
"ACHTUNG!\n\n\
Projektfamilien sollten nur in Ausnahmefällen eingesetzt werden da sie\n\
Nachteile zu ladbaren Familien aufweisen:\n\
- schwierige Berichterstattung\n\
- keine assozierte Ebene\n\
- das Kopieren einer solchen Familie erzeugt ein neues unabhängiges Original\n\
- Begrenzte parametrische Modellierungsfähigkeiten\n\n\
Wollen Sie wirklich eine Projektfamilie erstellen?",
"buttons":
["Erstellen", 
"Abbrechen",
"Mehr Informationen über Projektfamilien"],
},
"Import CAD file":{
"text":
"WARNUNG!\n\n\
Sie sollten CAD Dateien nur in Ausnahmefällen importieren.\n\
Importieren Sie CAD niemals direkt in das Modell, sondern in eine saubere RVT-Datei.\n\n\
Sind Sie sicher, dass Sie wissen, was Sie tun?",
"buttons":
["Importieren",
"Abbrechen",
"Mehr Informationen über den Import von CAD-Dateien"],
},
"Unpin":{
"text":
"WARNUNG!\n\n\
Wollen Sie dieses Element wirklich entsperren?\n\
Die Elemente sind in der Regel gesperrt, sodass sie nicht versehentlich verschoben werden können.\n\n\
Wollen Sie das wirklich tun?",
"buttons":
["Entsperren",
"Abbrechen",
"Mehr Informationen über Sperren/Entsperren"],
},
"Project Parameters":{
"text":
"WARNUNG!\n\n\
Wenn Sie einen neuen gemeinsam genutzten Parameter erstellen, prüfen Sie zunächst, ob ein ähnlicher Parameter bereits erstellt wurde.\n\n\
- Verwenden Sie das Werkzeug 'Liste gemeinsam genutzte Parameter'.\n\
- Verwenden Sie keine Sonderzeichen.",
"buttons":
["Liste gemeinsam genutzter Parameter im Wiki anzeigen",
"Parameter bearbeiten",
"Abbrechen"],
},
"Ramp":{
"text":
"WARNUNG!\n\n\
Es ist besser, Rampen als Geschossdecken mit definierter Neigung zu modellieren.\n\
- Rampen haben keine Optionen für die Erstellung von Schichten\n\
- Sie können weder eine Punktneigung noch eine Punkthöhe auf Rampen platzieren (vor Revit 2022)\n\
- Rampen haben keine Strukturparameter\n\
- Jemand wird in Zukunft alle Rampen in Geschossdecken umwandeln müssen.",
"buttons":
["Trotzdem die Rampe anlegen",
"Abbrechen",
"Mehr Infos zur Kategorie Rampe"],
},
"Architectural column":{
"text":
"WARNUNG!\n\n\
Im Allgemeinen sollten Stützen als Tragwerkstützen und nicht als Architekturstützen modelliert werden.\n\
- Architektonische Stützen erscheinen nicht im Strukturmodell.\n\
- Jemand wird in Zukunft alle Architekturstützen in Tragwerksstützen ändern müssen.",
"buttons":
["Erstellen Sie trotzdem die Architekturstütze",
"Abbrechen",
"Mehr Informationen über Architekturstützen"],
},
},
# FRENCH
"FR":{
"Shared Parameters":{
"text":
"AVERTISSEMENT!\n\n\
Si vous créez un nouveau paramètre partagé, vérifiez d'abord si un paramètre similaire a déjà été créé.\n\n\
- Utilisez l'outil 'Liste des paramètres partagés'.\n\
- N'utilisez pas d'accents.",
"buttons":
["Afficher la liste des paramètres partagés dans le wiki",
"Modifier les paramètres",
"Annuler"],
},
"Revit Build":{
"text":
"ATTENTION!\n\n\
Vous utilisez le mauvais Build de Revit ! Le modèle pourrait être endommagé.\n\
Les builds Revit corrects sont ",
"buttons":
["Je veux seulement ouvrir le fichier sans le synchroniser",
"Comment puis-je résoudre ce problème ?"],
},
"View, Schedule or Sheet Deletion":{
"text":
"AVERTISSEMENT!\n\n\
Voulez-vous vraiment supprimer ces vues?\n",
"buttons":
["Annuler",
"Supprimer"],
},
"Save List Of Opened Views":{
"text":
"Souhaitez-vous enregistrer une liste des vues ouvertes ?",
"buttons":
["Enregistrer",
"Sauter l'étape",
"En savoir plus"],
},
"Roof by Extrusion":{
"text":
"AVERTISSEMENT!\n\n\
Le toit par extrusion ne doit être utilisé que dans des cas exceptionnels.\n\
Si vous devez donner une pente à la toiture, utilisez des planchers et déterminez la pente.\n\
Pour les toits modélisés comme toit par extrusion, le contour en plan ne peut être adapté qu'avec une forme vide.",
"buttons":
["Créer un toit par extrusion",
"Annuler",
"Plus d'informations sur les toits par extrusion"],
},
"Load Family":{
"text":
"AVERTISSEMENT!\n\n\
La famille doit être inférieure à 1 MO.\n\
Vérifiez toujours la taille du fichier avant de le charger dans le modèle.\n\n\
La famille n'est-elle pas surmodelée ?",
"buttons":
["Annuler",
"Charger",
"Plus d'infos sur la taille de la famille"],
},
"Link CAD file in 3D":{
"text":
"AVERTISSEMENT!\n\n"
"Vous n'avez pas activé l'option 'Vue active uniquement'.\n"
"Vous êtes en train de lier un fichier CAO dans le modèle 3D !",
"buttons":
["Annuler",
"OK, j'ai besoin du DWG en 3D",
"Plus d'informations sur la liaison des fichiers CAO"],
},
"Link CAD file":{
"text":
"AVERTISSEMENT!\n\n\
Les fichiers CAO peuvent endommager le modèle Revit.\n\
Avez-vous suivi la solution de \"workaround\" du lien ci-dessous ?",
"buttons":
["Lier la CAO",
"Annuler",
"En savoir plus sur l'association de fichiers CAO"],
},
"In Place Family":{
"text":
"AVERTISSEMENT!\n\n\
Les familles in situes ne doivent être utilisées que dans des cas exceptionnels car elles présentent des inconvienants par rapport aux familles chargeables:\n\
- Difficultés dans les nomenclatures\n\
- Pas de niveau associé\n\
- La copie d'une telle famille crée un nouvel original indépendant\n\
- Capacités de modélisation paramétrique limitées\n\
Vous voulez vraiment créer une famille in situe?",
"buttons":
["Créer", 
"Annuler",
"Plus d'infos sur les familles in situ"],
},
"Import CAD file":{
"text":
"AVERTISSEMENT!\n\n\
Vous ne devez importer des fichiers CAO que dans des cas exceptionnels.\n\
N'importez jamais de CAO directement dans le modèle, mais dans un fichier RVT propre.\n\n\
Êtes-vous sûr de savoir ce que vous faites ?",
"buttons":
["Importer",
"Annuler",
"Plus d'informations sur l'importation de fichiers CAO"],
},
"Unpin":{
"text":
"AVERTISSEMENT!\n\n\
Voulez-vous vraiment déverrouiller cet élément ? \n\
Les éléments sont généralement verrouillés, de sorte qu'ils ne peuvent pas être déplacés par inadvertance.\n\n\
Voulez-vous vraiment faire cela?",
"buttons":
["Déverrouiller",
"Annuler",
"Plus d'informations sur le verrouillage/déverrouillage"],
},
"Project Parameters":{
"text":
"AVERTISSEMENT!\n\n\
Si vous créez un nouveau paramètre partagé, vérifiez d'abord si un paramètre similaire a déjà été créé.\n\n\
- Utilisez l'outil 'Liste des paramètres partagés'.\n\
- N'utilisez pas d'accents.",
"buttons":
["Afficher la liste des paramètres partagés dans le wiki",
"Modifier les paramètres",
"Annuler"],
},
"Ramp":{
"text":
"AVERTISSEMENT!\n\n\
Il est préférable de modéliser les rampes comme des planchers avec une pente définie.\n\
- Les rampes n'ont pas d'options pour la création de couches\n\
- Vous ne pouvez pas placer une inclinaison ou une hauteur de point sur les rampes (avant Revit 2022)\n\
- Les rampes n'ont pas de paramètres de structure\n\
- Quelqu'un devra à l'avenir transformer toutes les rampes en planchers.",
"buttons":
["Créer quand même la rampe",
"Annuler",
"Plus d'infos sur la catégorie rampe"],
},
"Architectural column":{
"text":
"AVERTISSEMENT!\n\n\
En général, les poteaux doivent être modélisés comme des poteaux porteurs et non comme des poteaux architecturaux.\n\
- Les poteaux architecturaux n'apparaissent pas dans le modèle structurel.\n\
- Quelqu'un devra à l'avenir changer tous les poteaux architecturaux en poteaux porteurs.",
"buttons":
["Créer quand même un poteau architectural",
"Annuler",
"Plus d'informations sur les poteaux architecturaux"],
},
},
}