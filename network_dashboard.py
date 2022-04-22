from dash.dependencies import Input, Output
import jaal
from jaal.datasets import load_got
from jaal import layout
import dash_bootstrap_components as dbc
from dash import html, dash_table


class Jaal(jaal.Jaal):

    def plot(self, debug=False, host="127.0.0.1", port="8050", directed=True, vis_opts=None):
        """Plot the Jaal by first creating the app and then hosting it on default server

        Parameter
        ----------
            debug (boolean)
                run the debug instance of Dash?

            host: string
                ip address on which to run the dash server (default: 127.0.0.1)

            port: string
                port on which to expose the dash server (default: 8050)

            directed (boolean):
                whether the graph is directed or not (default: False)

            vis_opts: dict
                the visual options to be passed to the dash server (default: None)
        """
        # call the create_graph function
        app = self.create(directed=directed, vis_opts=vis_opts)
        nodes_description_area = layout.create_row(
            [dbc.Row(
                html.Div(id="edges-table")
                )])
        app.layout.children.append(nodes_description_area)

        @app.callback(
            Output("edges-table", "children"),
            [Input('graph', 'selection')])
        def myfun(x):

            if x and len(x['nodes']) > 0:
                return dash_table.DataTable(data=edge_df[edge_df["to"] == x["nodes"][0]].to_dict('rows'))



        # run the server
        app.run_server(debug=debug, host=host, port=port)


# load the data
edge_df, node_df = load_got()
# init Jaal and run server
Jaal(edge_df, node_df).plot()