from flask import Flask, render_template, request, redirect
from graph import get_data, create_graph
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars["stock_ticker"] = request.form['ticker']
        app.logger.debug(app.vars["stock_ticker"])
        app.vars["columns_name"] = request.form.getlist('features')
        app.logger.debug(app.vars["columns_name"])
        final_data = get_data(
            app.vars["stock_ticker"], app.vars["columns_name"])
        plot = create_graph(final_data, app.vars["columns_name"])
        script, div = components(plot)
        return render_template('graph.html', script=script, div=div)


if __name__ == '__main__':
    app.run()
