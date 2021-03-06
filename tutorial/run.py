import time
import six
import os

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, State, Event, Output

from server import app, server
import introduction
import html_components
import core_components
import basic_callbacks
import html_component_appendix
import callbacks_with_dependencies
import dynamic_content
import external_css_and_js
import open_problems
import architecture
import live_updates
import changelog
import plugins
import gallery
import performance
import support
import deployment
import authentication
import installation
import getting_started_part_1
import getting_started_part_2

dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-1.27.1.min.js'

def create_contents(contents):
    h = []
    for i in contents:
        if isinstance(i, list):
            h.append(create_contents(i))
        else:
            h.append(html.Li(i))
    return html.Ul(h)

toc = html.Div(
create_contents([

    html.A('Introduction', href="introduction"),
    [
        'Why Dash?',
        'Licensing'
    ],

    html.A('Announcement Letter', href="https://medium.com/@plotlygraphs/introducing-dash-5ecf7191b503"),

    html.A('Gallery', href="gallery"),

    html.A('Create Your First App - Installation', href="installation"),

    html.A('Create Your First App - Part 1: App Layout', href="getting-started"),

    html.A('Create Your First App - Part 2: Interactivity', href="getting-started-part-2"),
    # [
    #     'Installation',
    #     'Part 1 - Dash Layout',
    #     [
    #         'HTML Components',
    #         'Data Visualization in Dash',
    #         'Markdown',
    #         'Core Component Library',
    #         'Calling `help`'
    #     ],
    #     'Part 2 - Interactivity',
    #     [
    #         'Fundamentals',
    #         'Multiple Inputs',
    #         'Multiple Outputs',
    #         'Crossfiltering'
    #     ]
    # ],

    # html.A('Deploying', href="deployment"),
    # [
    #     'On Premise',
    #     'Cloud PaaS'
    # ],
    #
    # html.A('Authentication', href="authentication"),

    html.A('Performance', href="performance"),
    # [
    #     'Caching',
    #     'Fast Charting with WebGL',
    # ],

    html.A('Live Updates', href="live-updates"),

    html.A('External CSS and JS', href="external-resources"),

    html.A('Dash Core Components', href="dash-core-components"),
    # [
    #     'Graph',
    #     'Dropdown',
    #     'RadioItems',
    #     'TextInput',
    #     'Slider',
    #     'RangeSlider',
    #     'Markdown'
    # ],

    html.A('Dash HTML Components', href="dash-html-components"),

    html.A('Build Your Own Components', href="plugins"),

    # html.A('Base Components', href="/base-components"),
    # 'Best Practices',
    # [
    #     'Virtual Environments',
    #     'Styling Apps',
    #     'Basic User Interface',
    #     'Initial State'
    # ],
    # 'Roadmap',
    # [
    #     'Sponsoring Development',
    #     'Near Term',
    #     [
    #         'App Templates',
    #         'Authentication'
    #     ],
    #     'Long Term',
    #     [
    #         'Dash in Other Languages',
    #         'GUI App Builder',
    #         'Client-side Apps'
    #     ]
    # ],
    # 'Get Involved',
    html.A('Support and Contact', href="support")

]), className="toc-chapters"
)

chapters = {
    'index': {
        'url': '',
        'content': html.Div([
            html.H1('Dash User Guide'),
            toc
        ], className="toc")
    },

    'introduction': {
        'url': 'introduction',
        'content': introduction.layout
    },

    'installation': {
        'url': 'installation',
        'content': installation.layout
    },

    'getting-started': {
        'url': 'getting-started',
        'content': getting_started_part_1.layout
    },

    'getting-started-part-2': {
        'url': 'getting-started-part-2',
        'content': getting_started_part_2.layout
    },

    'dash-core-components': {
        'url': 'dash-core-components',
        'content': core_components.layout
    },

    'dash-html-components': {
        'url': 'dash-html-components',
        'content': [
            html_components.layout,
            # html_component_appendix.layout
        ]
    },

    'external': {
        'url': 'external-resources',
        'content': external_css_and_js.layout
    },

    'plugins': {
        'url': 'plugins',
        'content': plugins.layout
    },

    'gallery': {
        'url': 'gallery',
        'content': gallery.layout
    },

    'live-updates': {
        'url': 'live-updates',
        'content': live_updates.layout
    },

    'performance': {
        'url': 'performance',
        'content': performance.layout
    },

    'support': {
        'url': 'support',
        'content': support.layout
    },

    # 'deployment': {
    #     'url': 'deployment',
    #     'content': deployment.layout
    # },
    #
    # 'authentication': {
    #     'url': 'authentication',
    #     'content': authentication.layout
    # }
}

header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.A(html.Img(
                src="https://cdn.rawgit.com/plotly/dash-docs/b1178b4e/images/dash-logo-stripe.svg",
                className="logo"
            ), href='https://plot.ly/products/dash', className="logo-link"),

            html.Div(className="links", children=[
                html.A('pricing', className="link", href="https://plot.ly/products/on-premise"),
                html.A('user guide', className="link active", href="https://plot.ly/dash/"),
                html.A('plotly', className="link", href="https://plot.ly/")
            ])
        ]
    )
)

app.title = 'Dash User Guide and Documentation - Dash by Plotly'

app.layout = html.Div([
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Meta(
        name='description',
        content=('Dash User Guide and Documentation. '
                 'Dash is a Python framework for building '
                 'reactive web apps developed by Plotly.')
    ),
    header,
    html.Div([
        html.Div([
            html.Div([
                dcc.RadioItems(options=[
                    {'label': i, 'value': i} for i in chapters.keys()
                ], value='index', id='toc', labelStyle={'fontWeight': 400})
            ], style={'display': 'none'}),
            html.Div(
                html.Div(id="chapter", className="content"),
                className="content-container"
            ),
        ], className="container-width")
    ], className="background")
])


@app.callback(Output('chapter', 'children'), [Input('toc', 'value')])
def display_content(selected_chapter):
    content = chapters[selected_chapter]['content']
    if selected_chapter != 'index':
        content = html.Div([
            html.Div(content),
            html.Hr(),
            html.A(href='/dash/', children='Back to the Table of Contents')
        ])
    return content

app.routes = [
    {
        'pathname': chapter_object['url'],
        'state': {'toc.value': chapter_id}
    } for chapter_id, chapter_object in six.iteritems(chapters)
]

app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/f6fed04e3f23c2ac5b4ea88819c2c14c07e88442/dash-docs-base.css',
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/30b641e2e89753b13e6557b9d65649f13ea7c64c/dash-docs-custom.css',
        'https://fonts.googleapis.com/css?family=Dosis'
    )
})

if 'DYNO' in os.environ:
    app.scripts.config.serve_locally = False
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })
else:
    app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=8050)
