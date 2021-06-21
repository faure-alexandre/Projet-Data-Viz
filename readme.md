Readme
============

- [Readme](#readme)
  - [Description](#description)
  - [Plan du dashboard](#plan-du-dashboard)
    - [`/apps`](#apps)
    - [`/assets`](#assets)
    - [`/data`](#data)
    - [`index.py`](#indexpy)
    - [`app.py`](#apppy)
  - [Ressources utilisées](#ressources-utilisées)


## Description
Le but de ce projet est de développer un dashboard Plotly/Dash multi-pages mettant en scène des données permettant d’évaluer l'impact de la pandémie Covid-19 sur l'économie mondiale, accessible via ce [lien](https://data.mendeley.com/datasets/b2wvnbnpj9/1).

<u>Contraintes:</u>
1. Récupération des données, leur nettoyage éventuel
ainsi que l’analyse de ces données et des pré-traitements nécessaires à cette analyse.
2. Le dashboard sera réalisé en Dash. Il devra permettre une interprétation évidente des données (les graphiques devront être sélectionnés avec soin).
3. Le dashboard doit également contenir l’analyse sémantique que vous faites des données suite à votre travail.
4. Le dashboard devra offrir un rendu visuel de qualité publiable (css, boostrap components...) et sera hébergé sur le serveur cloud Heroku afin de pouvoir être ommuniqué sur des supports numériques (LinkedIn, CV …).


## Plan du dashboard

### `/apps` 
Répertoire contenant un fichier `.py` par page du Dashboard, à savoir:

* `home_page.py` : script contenant le texte de la page d'accueil.
* `about_page.py` : script contenant le texte de la page à propos.
* `actions_app.py` : page permettant de mesurer l'impact de la crise sur le cours des actions.
* `commerce_app.py` : page permettant de mesurer l'impact de la crise sur les échanges internationaux (exportations, importations).
* `covid_app.py` : page contenant quelques graphiques relatifs à l'évolution de l'épidemie. 
* `HID_app.py` : page permettant de mesurer l'impact de la crise en fonction du développement des pays.
* `petrol_app.py` : page permettant de mesurer l'impact de la crise sur l'évolution des prix du pétrole.
* `pib_app.py` : page permettant de mesurer l'impact de la crise sur l'évolution du PIB.
* `travail_app.py` : page permettant de mesurer l'impact de la crise sur la situation du marché de l'emploi.
  
Chaque fichier (hormis `home_page.py` et `about_page.py`) se décompose en 3 parties:
1. Importation et traitement des données.
2. Création de la structure de la page (création des emplacements des graphiques, gestion des inputs...) dans la variable `layout`.
3. Gestion des Callbacks qui contiennent en général le code plotly permettant d'afficher les graphiques de manière interactive.


### `/assets`
Répertoire contenant un fichier `.css` de style ainsi que l'image de fond et l'icône du Dashboard.

### `/data`
Répertoire contenant les données.

### `index.py`
Script contenant la structure de base commune à toutes les pages du Dashboard à savoir la barre de naviguation et la gestion d'affichage des différentes pages. Ce script contient le code permettant de lancer le server en mode local, c'est donc lui qu'il faut executer pour lancer l'application en mode *localhost*.

### `app.py`
Script permettant d'initialiser une instance d'application Dash.


## Ressources utilisées
* [Données de l'OCDE](https://stats.oecd.org/index.aspx?lang=fr).
* [Documentation Dash](https://dash.plotly.com/).
* [Documentation Dash-Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/docs/).

