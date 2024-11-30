from flask import Blueprint, render_template
from flask_babel import gettext

YOUTUBE_URLS = {
    "7ZdxZAfhwbA": "Voir la radioactivité avec son smartphone ?",
    "2yeNi4pWivI": "☢️ Un nouveau nuage radioactif ☢️ ? Les réseaux de mesures de la radioactivité.",
    "mFYyLVb5FpA": "Détecter les éclairs de chez soi ?",
    "attGxkaEQSw": "Le filtre inversé",
    "C-M1dAhmecY": "Le secret du paratonnerre : l'effet de pointe",
    "-cvyrq50ha4": "Le super-matériau le moins dense au monde : l'aérographène",
    "6gRR07qivpY": "Transformer les océans en mines d'uranium ?",
    "qoWuoKfnsI4": "L'aliment le plus radioactif au monde - La noix du Brésil",
    "RJSNhS3Wv4A": "Faire exploser une planète",
    "SR4D-O19rwo": "💀 Mourir de chaud à 35°C 🌡️",
    "UFhpLcGu5DY": "Transformer du gaz carbonique en alcool !",
    "f2qTK1yW7HU": "L'arme secrète de la crevette-pistolet : la cavitation",
    "iVOTScOXf_o": "La vérité derrière l'Ice ❄️ and Salt Challenge 🔥",
    "SxQddU2MuFk": "La substance la plus sombre au monde : le Vantablack",
    "5-rT10Mt72g": "Le matériau le plus solide au monde : les nanotubes de carbone",
    "n33JLc6W4wQ": "La Terre et le miroir ont 30% en commun : l'albédo",
    "RGC9Pbgm7Lc": "Le super matériau qu'on croyait impossible : le graphène",
    "zEofUJJxOUU": "Faire léviter une goutte d'eau chez soi : l'effet Leidenfrost",
    "i7hYy9xjc1w": "Voir la radioactivité dans un fluide : la chambre à brouillard !",
    "mPWqJj0YPpk": "Le gouffre cosmique : le trou noir !",
    "zn0Y8uvRqSY": "Voir les températures à distance : la caméra thermique !",
    "14XAQaNFQaM": "Super-matériau du futur : l'aérogel !",
    "sOXTcanDIeA": "Le cœur de démon",
}

youtube_blueprint = Blueprint("youtube_blueprint", __name__)


@youtube_blueprint.route(
    "/youtube/<uid>/",
    methods=[
        "GET",
    ],
)
def youtube(uid: str) -> str:
    return render_template(
        "youtube.html", uid=uid, title=gettext(YOUTUBE_URLS.get(uid)),
    )
