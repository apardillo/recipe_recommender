
import pickle
import networkx as nx
import plotly.graph_objects as go
import streamlit as st


class NetworkGraph:

    def __init__(self):
        self.df_recipes = pickle.load(open('data/recipe_list.pkl', "rb"))
        self.df_similarities = pickle.load(open('data/similarity.pkl', "rb"))
    
    def plot_network(self,threshold,ingredient_filter,f=None):
        network_df_long=self.df_similarities

        filtered_all=network_df_long[(network_df_long.value>=threshold)]
        filtered_all=filtered_all.loc[~(filtered_all['index'] == filtered_all['variable'])]

        filtered_all.columns=["doc1","doc2","similarity_score"]

        filtered_ingredients=self.df_recipes[self.df_recipes.ingredients.str.contains(ingredient_filter)].index

        if f=="Similar":
            filtered_all=filtered_all[(filtered_all.doc1.isin(filtered_ingredients)) & (filtered_all.doc2.isin(filtered_ingredients)) ]
        elif f=="Complementary":
            filtered_all=filtered_all[filtered_all.doc1.isin(filtered_ingredients)]
        
        

        

        G = nx.Graph()
        for i in filtered_all.doc1.unique():
            if not G.has_node(i):
                G.add_node(i)
                #G.add_node(i)

        for i in filtered_all.index:
            #print(i)
            if not G.has_edge(filtered_all.loc[i].doc1,filtered_all.loc[i].doc2):
                G.add_edge(filtered_all.loc[i].doc1,filtered_all.loc[i].doc2)



        pos = nx.spring_layout(G)

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 =pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')


        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))


        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                            "Recipe Name:" + str(self.df_recipes .loc[adjacencies[0]].food) +"<br>" +
                            "Recipe ID: " + str(adjacencies[0]) +"<br>" + "<br>" +
                        
                            "Ingredients:<br>" + self.df_recipes .loc[adjacencies[0]].ingredients.replace(",","<br>") + "<br>"  + "<br>"  #+
                            #"Ingredients:<br>" + df_display.loc[adjacencies[0]].ingredients.replace(",","<br>")
                            )


        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text


        #Layout
        fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    #title='Network Of Similar Recipes. Specified Ingredient: ' + ingredient_filter.title() ,
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="", 
                        showarrow=False, 
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

        fig.update_layout(height=800, width=1600, 
                            #hovermode="x"
                            )
        #fig.show()
        st.plotly_chart(fig,use_container_width=True)

if __name__ == '__main__':
    ng=NetworkGraph()
    ng.plot_network(0.8,"beef",f="Similar")
    #NetworkGraph.plot_network()
    #pass