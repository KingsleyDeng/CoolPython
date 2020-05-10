from flask import Flask, request, render_template
from jinja2 import Markup

from pyecharts import options as opts
from pyecharts.charts import Bar

app = Flask(__name__, static_folder="templates")


def bar_base(names, subtitles) -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
            .set_global_opts(title_opts=opts.TitleOpts(title=names, subtitle=subtitles))
    )
    return c


# @app.route("/")
# def index():
#     c = bar_base()
#     return Markup(c.render_embed())

@app.route("/")
def index():
    data = request.args.to_dict()
    return render_template("indexs.html", data=data)


@app.route("/barChart")
def get_bar_chart():
    args = request.args.to_dict()
    print(args)
    result = eval(args.get("result"))
    name = result.get("name")
    subtitle = result.get("subtitle")
    c = bar_base(name, subtitle)

    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run(debug=True)
