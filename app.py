from flask import Flask, render_template, request, redirect, url_for

from app.models.base import Arena
from app.models.classes import unit_classes
from app.models.equipment import Equipment
from app.models.unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(heroes.get("player"), heroes.get("enemy"))
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == "GET":
        result = {"header": "Кто ты?",
                  "classes": unit_classes.keys(),
                  "weapons": equipment.get_weapons_names(),
                  "armors": equipment.get_armors_names()
                  }

        return render_template("hero_choosing.html", result=result)

    if request.method == "POST":
        hero = {
            "name": request.form.get("name"),
            "unit_class": unit_classes.get(request.form.get("unit_class"))
        }

        player = PlayerUnit(**hero)
        player.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        player.equip_armor(equipment.get_armor(request.form.get("armor")))

        heroes["player"] = player

        return redirect(url_for("choose_enemy"), 301)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        result = {"header": "Кто ты?",
                  "classes": unit_classes.keys(),
                  "weapons": equipment.get_weapons_names(),
                  "armors": equipment.get_armors_names()
                  }

        return render_template("hero_choosing.html", result=result)

    if request.method == "POST":
        hero = {
            "name": request.form.get("name"),
            "unit_class": unit_classes.get(request.form.get("unit_class"))
        }

        player = EnemyUnit(**hero)
        player.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        player.equip_armor(equipment.get_armor(request.form.get("armor")))

        heroes["enemy"] = player

        return redirect(url_for("start_fight"), 301)


if __name__ == "__main__":
    app.run()
