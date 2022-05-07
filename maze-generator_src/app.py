from datetime import timedelta

from flask import Flask, render_template, request, url_for, redirect, session, flash
from RectangleMaze import RectangleMaze
from MyGraph import Graph, tree_maker

app = Flask(__name__)
app.secret_key = "HBBJ.,bJHBjhjbjhBJqh)bqf11414YuvUVYVIVoHDIOd"


def get_maze(user_idx, graph_name):
    graph = user_graphs[user_idx][graph_name]
    maze = RectangleMaze(*graph.get_parameters())
    maze.build_on_graph(graph)
    return maze


def get_maze_txt(user_idx, graph_name):
    maze = get_maze(user_idx, graph_name)
    txt = ''
    for line in maze.get_str():
        for c in line:
            txt += c
        txt += '\n'
    return txt


@app.route('/', methods=["POST", "GET"])
def home():
    global users
    global user_graphs

    if request.method == "POST":
        if "new maze" in request.form:
            try:
                algo = tree_maker[request.form["algo"]]
                width = int(request.form["width"])
                height = int(request.form["height"])
                name = request.form["new name"]
                if not name:
                    raise
                graph = Graph(0)
                graph.construct_from_rectangle(width, height)
                algo(graph)
            except Exception:
                flash("Error occurred, check width, height or name")
                return render_template('index.html')

            session["graph_name"] = name
            if "user_idx" not in session:
                session["user_idx"] = users
                user_graphs[session["user_idx"]] = dict()
                users += 1
            user_graphs[session["user_idx"]][name] = graph

        if "existing name" in request.form:
            if "user_idx" not in session or request.form["existing name"] not in user_graphs[session["user_idx"]]:
                flash("Error occurred, check the name of your maze")
                return render_template('index.html')
            session["graph_name"] = request.form["existing name"]

        return redirect(url_for("process_maze"))
    else:
        if "user_idx" not in session:
            flash("Hello, this is maze generator", "info")
        elif user_graphs[session["user_idx"]]:
            message = "These are your current mazes: " + ", ".join([t for t in user_graphs[session["user_idx"]].keys()])
            flash(message, "info")
        else:
            flash("You don't have saved mazes", "info")

        return render_template('index.html')


@app.route('/process_maze', methods=["POST", "GET"])
def process_maze():
    if request.method == "POST":
        if "discard maze" in request.form:
            user_graphs[session["user_idx"]].pop(session["graph_name"])
            session.pop("graph_name")
            return redirect(url_for("home"))

        if "show path" in request.form:
            return redirect(url_for("show_path"))

        if "play" in request.form:
            return redirect(url_for("play"))

        if "save maze" in request.form:
            return redirect(url_for("home"))

    user_graphs[session["user_idx"]][session["graph_name"]].clear_marks()

    maze = get_maze_txt(session["user_idx"], session["graph_name"])
    return render_template('process_maze.html', maze=maze)


@app.route('/process_maze/show_path', methods=["POST", "GET"])
def show_path():
    if request.method == "POST":
        if "exit" in request.form:
            return redirect(url_for("process_maze"))

        graph = user_graphs[session["user_idx"]][session["graph_name"]]
        graph.clear_marks()
        width, height = graph.get_parameters()

        try:
            x1 = int(request.form["x1"])
            y1 = int(request.form["y1"])
            x2 = int(request.form["x2"])
            y2 = int(request.form["y2"])

            start = (y1 - 1) * width + (x1 - 1)
            finish = (y2 - 1) * width + (x2 - 1)
            user_graphs[session["user_idx"]][session["graph_name"]].mark_path(start, finish)
        except Exception:
            flash("Error occurred, check coordinates")
            user_graphs[session["user_idx"]][session["graph_name"]].clear_marks()

    maze = get_maze_txt(session["user_idx"], session["graph_name"])
    return render_template('show_path.html', maze=maze)


@app.route('/process_maze/play', methods=["POST", "GET"])
def play():
    if "position" not in session:
        session["position"] = (0, 0)

    if request.method == "POST":
        if "exit" in request.form:
            session.pop("position")
            return redirect(url_for("process_maze"))

        if "up" in request.form:
            direction = 0
        if "right" in request.form:
            direction = 1
        if "down" in request.form:
            direction = 2
        if "left" in request.form:
            direction = 3

        maze = get_maze(session["user_idx"], session["graph_name"])

        maze.set_current_player_pos(session["position"])

        if maze.make_turn(direction):
            flash("Well done")
            return redirect(url_for("process_maze"))

        session["position"] = maze.get_current_player_pos()

        txt = ''
        for line in maze.get_str():
            for c in line:
                txt += c
            txt += '\n'

        return render_template('play.html', maze=txt)

    else:
        maze_txt = get_maze_txt(session["user_idx"], session["graph_name"])
        return render_template('play.html', maze=maze_txt)


if __name__ == "__main__":
    users = 0
    user_graphs = dict()
    app.run()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
