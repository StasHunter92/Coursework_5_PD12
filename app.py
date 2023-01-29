from flask import Flask, render_template, request, redirect, url_for

from application.models.base import Arena
from application.models.classes import unit_classes
from application.models.equipment import Equipment
from application.models.unit import PlayerUnit, EnemyUnit

# ----------------------------------------------------------------------------------------------------------------------
# Create application flask instance
app = Flask(__name__)

# ----------------------------------------------------------------------------------------------------------------------
# Create game settings
heroes = {}
arena = Arena()
equipment = Equipment()


# ----------------------------------------------------------------------------------------------------------------------
# Create routes for game
@app.route("/")
def menu_page():
    """
    Main start page
    """
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    """
    Arena start page
    """
    arena.start_game(heroes.get("player"), heroes.get("enemy"))
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    Hit button with game logic
    """
    if arena.game_is_running:
        result: str = arena.player_hit()
    else:
        result: str = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Skills button with game logic
    """
    if arena.game_is_running:
        result: str = arena.player_use_skill()
    else:
        result: str = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Pass turn button with game logic
    """
    if arena.game_is_running:
        result: str = arena.next_turn()
    else:
        result: str = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    End game button with game logic
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    """
    Start screen with player creation
    """
    if request.method == "GET":
        result: dict = {"header": "Кто ты?",
                        "classes": unit_classes.keys(),
                        "weapons": equipment.get_weapons_names(),
                        "armors": equipment.get_armors_names()
                        }

        return render_template("hero_choosing.html", result=result)

    if request.method == "POST":
        hero: dict = {
            "name": request.form.get("name"),
            "unit_class": unit_classes.get(request.form.get("unit_class"))
        }

        player: PlayerUnit = PlayerUnit(**hero)
        player.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        player.equip_armor(equipment.get_armor(request.form.get("armor")))

        heroes["player"] = player

        return redirect(url_for("choose_enemy"), 301)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    Start screen with enemy creation
    """
    if request.method == "GET":
        result: dict = {"header": "Кто ты?",
                        "classes": unit_classes.keys(),
                        "weapons": equipment.get_weapons_names(),
                        "armors": equipment.get_armors_names()
                        }

        return render_template("hero_choosing.html", result=result)

    if request.method == "POST":
        hero: dict = {
            "name": request.form.get("name"),
            "unit_class": unit_classes.get(request.form.get("unit_class"))
        }

        player = EnemyUnit(**hero)
        player.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        player.equip_armor(equipment.get_armor(request.form.get("armor")))

        heroes["enemy"] = player

        return redirect(url_for("start_fight"), 301)


# ----------------------------------------------------------------------------------------------------------------------
# Run game
if __name__ == "__main__":
    app.run()
