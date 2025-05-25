from dash import Dash, html, dcc, Input, Output
import plotly.express as px 
import pandas as pd 

#app instantiation
app = Dash(external_stylesheets=['assets/styles.css'])

#data imports
tuition_trends = pd.read_csv('analysis/processed_data/tuition.csv').drop(columns=['Unnamed: 0'], axis=1)
class_grades = pd.read_csv('analysis/processed_data/class_grades.csv').drop(columns=['Unnamed: 0'], axis=1)
school_gpa = pd.read_csv('analysis/processed_data/course_gpa.csv').drop(columns=['Unnamed: 0'], axis=1)
genders = pd.read_csv('analysis/processed_data/genders.csv').drop(columns=['Unnamed: 0'], axis=1)
generations = pd.read_csv('analysis/processed_data/generations.csv').drop(columns=['Unnamed: 0'], axis=1)
loads = pd.read_csv('analysis/processed_data/loads.csv').drop(columns=['Unnamed: 0'], axis=1)
races = pd.read_csv('analysis/processed_data/races.csv').drop(columns=['Unnamed: 0'], axis=1)
residencies = pd.read_csv('analysis/processed_data/residencies.csv').drop(columns=['Unnamed: 0'], axis=1)
schools = pd.read_csv('analysis/processed_data/schools.csv').drop(columns=['Unnamed: 0'], axis=1)

app.layout = [
    # dashboard title
    html.Div('UVA Data Dashboard', className='dashboard-title'),
    html.Hr(),
    
    #UVA image 
    html.Img(src='assets/uva_logo.jpg', style={'height': '100px'}),

    # tuition trends
    html.Div([
        dcc.Graph(id='tuition-graph'), 
        dcc.RangeSlider(
            id='tuition-slider',
            min=1970,
            max=2025,
            value=[1970,2024],
            step=5,
            marks={i: str(i) for i in range(1970, 2026, 10)},
            pushable=10
        ),
    ]),

    # grade distribution
    html.Div([
        dcc.Graph(id='class-grade-fig'),
        dcc.Dropdown(
            id='class-filter',
            options=[{'label': course, 'value': course} for course in class_grades['Course Number'].values ],
            value='CS 2100',
            searchable=True,
            placeholder='Select a class...'
        )
    ]),

    #school gpa histogram 
    html.Div([
        dcc.Graph(id='school-hist'),
        dcc.Dropdown(
            id='school-filter',
            options=[
                {'label': 'School of Engineering and Applied Sciences', 'value': 'ENGR'},
                {'label': 'College of Arts and Sciences', 'value': 'CGAS'},
                {'label': 'School of Architecture', 'value': 'ARCH'},
                {'label': 'McIntire School of Commerce', 'value': 'COMM'},
                {'label': 'School of Continuing and Professional Studies', 'value': 'SCPS'},
                {'label': 'School of Law', 'value': 'LAW'},
                {'label': 'Frank Batten School of Leadership and Public Policy', 'value': 'LEAD'},
                {'label': 'Executive VP and Provost', 'value': 'PROV'},
                {'label': 'Medical School', 'value': 'MDS'},
                {'label': 'School of Data Science', 'value': 'DSCI'},
                {'label': 'School of Education and Human Development', 'value': 'EDUC'},
                {'label': 'McIntire Darden Grad Business', 'value': 'MCDG'},
                {'label': 'School of Nursing', 'value': 'NURS'},
                {'label': 'All', 'value': 'All'}
            ],
            value='All',
            searchable=True,
            placeholder='Select a school...'
        )
    ]),

    #demographic pie chart
    html.Div([
        dcc.RadioItems(
            id='demographic-radio',
            options = [
                {'label': 'Genders', 'value': 'Genders' },
                {'label': 'First Generation', 'value': 'First Generation' },
                {'label': 'Academic Load', 'value': 'Academic Load' },
                {'label': 'Race/Ethnicity', 'value': 'Race/Ethnicity' },
                {'label': 'In/Out of State', 'value': 'In/Out of State' },
                {'label': 'School/College', 'value': 'School/College' },
            ],
            value='School/College'
        ),
        dcc.Graph(id='demographics-fig')
    ])
]

#interactive functions

@app.callback(
    Output('tuition-graph', 'figure'),
    Input('tuition-slider', 'value')
)
def update_tuition(selected_value: list):
    '''
    Updates tuition trend chart based on slider value.

    Args:
        selected_value (list): Two integers denoting the range of the slider.
    
    Returns:
        px.line(): The updated line chart of tuition trends.

    '''
    updated_df = tuition_trends[(tuition_trends['Year'] >= selected_value[0]) & (tuition_trends['Year'] <= selected_value[1])]

    tuition_fig = px.line(
        updated_df, # data
        x=updated_df['Year'],
        y=updated_df['Tuition']
    )

    tuition_fig.update_traces(
        line=dict(
            width=3,
            color='#f84c1e'
        )
    )

    #axis label colors
    tuition_fig.update_xaxes(tickfont=dict(color='#f84c1e'))
    tuition_fig.update_yaxes(tickfont=dict(color='#f84c1e'))

    tuition_fig.update_layout(
        #figure
        width=850,
        height=500,
        #title
        title_text='Tuition Trends',
        title_x=0.5,
        title_font=dict(color='#f84c1e', family='Franklin Gothic', size=30),
        #axis properties
        xaxis_title='Year',
        xaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
        yaxis_title='Amount ($)',
        yaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
        paper_bgcolor='#222b4c',
        plot_bgcolor='#222b4c'
    )

    return tuition_fig

@app.callback(
    Output('class-grade-fig', 'figure'),
    Input('class-filter', 'value')
)
def update_classgrade(selected_value: str):
    '''
    Updates course grade histogram based on filter dropdown.

    Args:
        selected_value (str): The specific course to be represented.
    
    Returns:
        px.bar(): The updated bar chart of grade distributions.
    '''
    updated_df = class_grades[class_grades['Course Number'] == str(selected_value)]

    class_categories = list(updated_df.columns[1:])
    class_values = list(updated_df.values[0][1:])

    class_grade_fig = px.bar(
        x=class_categories,
        y=class_values,
        color_discrete_sequence=['#f84c1e'],
        width=850,
        height=500
    )

    class_grade_fig.update_xaxes(tickfont=dict(color='#f84c1e'))
    class_grade_fig.update_yaxes(tickfont=dict(color='#f84c1e'))

    class_grade_fig.update_layout(
        title=dict(
            text=f'Grade Distribution per course: {selected_value}',
            x=0.5,
            font=dict(size=30, family='Franklin Gothic', color='#f84c1e'),
        ),
        bargap=0,
        plot_bgcolor='#222b4c',
        paper_bgcolor='#222b4c',
        xaxis_title='Grades',
        xaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
        yaxis_title='Frequency',
        yaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
    )

    return class_grade_fig

@app.callback(
    Output('school-hist', 'figure'),
    Input('school-filter', 'value')
)
def update_hist(selected_value: str):
    '''
    Updates GPA histogram based on filter dropdown.

    Args:
        selected_value (str): The school or college to be represented.
    
    Returns:
        px.histogram(): The updated histogram of GPA distributions.
    '''
    if selected_value == 'All':
        updated_df = school_gpa.drop(columns=['Class Academic Group'], axis=1).groupby('Course Number').aggregate('mean')
    else:
        updated_df = school_gpa[school_gpa['Class Academic Group'] == selected_value].drop(columns=['Class Academic Group'], axis=1).groupby('Course Number').aggregate('mean')
    
    school_hist = px.histogram(
        updated_df,
        nbins=20,
        color_discrete_sequence=['#f84c1e'],
        width=850,
        height=500
    )

    school_hist.update_xaxes(tickfont=dict(color='#f84c1e'))
    school_hist.update_yaxes(tickfont=dict(color='#f84c1e'))

    school_hist.update_layout(
        title=dict(
            text=f"GPA Distribution per college: {selected_value}",
            x=0.5,
            font=dict(size=30, family='Franklin Gothic', color='#f84c1e')
        ),
        plot_bgcolor='#222b4c',
        paper_bgcolor='#222b4c',
        xaxis_title='Grade Point Average',
        xaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
        yaxis_title='Frequency',
        yaxis_title_font=dict(size=25, family='Franklin Gothic', color='#f84c1e'),
        showlegend=False
    )
    
    return school_hist

@app.callback(
    Output('demographics-fig', 'figure'),
    Input('demographic-radio', 'value')
)
def update_pie(selected_value: str):
    '''
    Updates pie chart of demographics.

    Args:
        selected_value (str): The feature to be represented.
    
    Returns:
        px.pie(): The updated pie chart of demographics.
    '''
    
    #colors: ['darkgray', '#232d4b', '#c9cbd2', '#e57200', 'lightgray', '#f9dcbe', '#222b4c', '#f84c1e', 'gray', ]

    #assigns appropriate dataframe and color set
    if selected_value == 'Genders':
        updated_df = genders
        colors = ['#222b4c', '#f84c1e']
    if selected_value == 'First Generation':
        updated_df = generations
        colors = ['#222b4c', '#f84c1e']
    if selected_value == 'Academic Load':
        updated_df = loads 
        colors = ['#222b4c', '#f84c1e']
    if selected_value == 'Race/Ethnicity':
        updated_df = races 
        colors=['darkgray', '#232d4b', '#c9cbd2', '#e57200', 'lightgray', '#f9dcbe', '#222b4c', '#f84c1e']
    if selected_value == 'In/Out of State':
        updated_df = residencies 
        colors = ['#222b4c', '#f84c1e']
    elif selected_value == 'School/College':
        updated_df = schools
        colors =['darkgray', '#232d4b', '#c9cbd2', '#e57200', 'lightgray', '#f9dcbe', '#222b4c', '#f84c1e', 'gray']

    demographic_pie = px.pie(
        updated_df,
        values = updated_df.iloc[:,1].values,
        names= updated_df.iloc[:,0].values,
        hole=0.3,
        color_discrete_sequence=colors
    )

    demographic_pie.update_traces(
        textfont=dict(
            size=14,
            family='Franklin Gothic',
            color='white'
        )
    )

    demographic_pie.update_layout(
        #size
        width=850,
        height=430,
        #title
        title_text='Demographics',
        title_x=0.5,
        title_font=dict(color='#f84c1e', family='Franklin Gothic', size=30),
        #figure and chart background color
        paper_bgcolor='#1c1c1b',
        plot_bgcolor='#1c1c1b',
        #legend properties
        legend=dict(
            font=dict(
                family='Franklin Gothic',
                size=16,
                color='white'
            )
        )
    )

    return demographic_pie

if __name__ == '__main__':
    app.run(debug=True)