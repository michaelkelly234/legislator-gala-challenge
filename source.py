import numpy as np
import networkx as nx
import pandas as pd
import random
import json

class seating_list:
    def __init__(self, num_tables, guest_list, planner_preferences):
        """Generates optimal seating list using gradient descent.
        
        Args:
            num_tables (int): 
                an integer, representing the number of tables at the gala
            guest_list (list of str): 
                an array of strings, representing the entire list of invited guests at the event
            planner_preferences (list of dict): 
                an array of dicts with preference avoid or pair and guests with those preferences
        Returns:
            writes file output.json with optimal table seating
        """
        self.num_tables = num_tables
        self.guest_list = guest_list
        self.planner_preferences = planner_preferences

        self.init_edges()
        self.init_matrix()
        

        
    def init_edges(self):
        relationships_edges = {}

        # negative is good (those two like each other), positive is bad (those two hate each other)
        for pref in self.planner_preferences:

            assert len(pref['guests']) == 2, 'guests array only accept 2 guests at a time'

            if(pref['preference'] == 'avoid'):
                relationships_edges[(pref['guests'][0],pref['guests'][1])] = 1
            elif(pref['preference'] == 'pair'):
                relationships_edges[(pref['guests'][0],pref['guests'][1])] = -1

        for guest in self.guest_list:
            relationships_edges[(guest,guest)] = 0
        
        self.relationships_edges = relationships_edges

    def init_matrix(self):    
        temp_graph = nx.Graph()
        for k, v in self.relationships_edges.items():
            temp_graph.add_edge(k[0], k[1], weight=v)
 
        relationships_mat_unnormed = nx.to_numpy_array(temp_graph.to_undirected(), nodelist=self.guest_list)
       
        self.relationships_matrix = relationships_mat_unnormed

    def reshape_to_table_seats(self, x):  
        table_seats = np.copy(x).reshape(self.num_tables, len(self.guest_list))
        return table_seats

    def cost(self, x):
        table_seats = self.reshape_to_table_seats(x)

        table_costs = np.dot(table_seats, np.dot(self.relationships_matrix, table_seats.T))
        table_cost = np.trace(table_costs)
        return table_cost

    def take_step(self, x):
        table_seats = self.reshape_to_table_seats(x)
        # randomly swap two guests
        #print(table_seats)

        table_from_guests = []
        table_to_guests = []
        while(len(table_from_guests) or len(table_to_guests)) < 1:
            table_from, table_to = np.random.choice(self.num_tables, 2, replace=False)

            table_from_guests = np.where(table_seats[table_from] == 1)[0]
            table_to_guests = np.where(table_seats[table_to] == 1)[0]

        #print(table_from_guests)
        #print(table_to_guests)

        table_guests = np.concatenate((table_from_guests,table_to_guests))
        table_from_guest = np.random.choice(table_guests)
        table_to_guest = np.random.choice(table_guests)

   
        if(table_from_guest == table_to_guest):
            table_seats[table_from, table_from_guest] = 1-table_seats[table_from, table_from_guest]
            table_seats[table_to, table_to_guest] = 1-table_seats[table_to, table_to_guest]
        else:
            table_seats[table_from, table_from_guest] = 1 - table_seats[table_from, table_from_guest]
            table_seats[table_from, table_to_guest] = 1 - table_seats[table_from, table_to_guest]
            table_seats[table_to, table_to_guest] = 1 - table_seats[table_to, table_to_guest]
            table_seats[table_to, table_from_guest] = 1 - table_seats[table_to, table_from_guest]
        return table_seats

    def prob_accept(self, cost_old:float, cost_new:float, temp:float)->float:
        """_summary_

        Args:
            cost_old (float): cost function of last seating arrangement
            cost_new (float): cost function of next seating arrangement
            temp (float): step size

        Returns:
            float: probability of accepting new seating arrangement, 1 if cost_new is lower
        """
        a = 1 if cost_new < cost_old else np.exp((cost_old - cost_new) / temp)
        return a

    def anneal(self, x, temp=2.0, temp_min=0.0001, alpha=0.9, n_iter=100, audit=False):
        cost_old = self.cost(x)

        audit_trail = []

        while temp > temp_min:
            for i in range(0, n_iter):
                x_new = self.take_step(x)
                cost_new = self.cost(x_new)
                p_accept = self.prob_accept(cost_old, cost_new, temp)
                if p_accept > np.random.random():
                    x = x_new
                    cost_old = cost_new
                if audit:
                    audit_trail.append((cost_new, cost_old, temp, p_accept))
            temp *= alpha

        return x, cost_old, audit_trail
    
    def solve(self):
        s = list(range(self.num_tables*len(self.guest_list)))
        random.shuffle(s)
        s = [ x+1 for x in s]

        Table_Arrangement=pd.DataFrame(zip(self.guest_list,s),columns=["Guest Name","Assigned Seat No"])
        Table_Arrangement["Assigned Table No"]=((Table_Arrangement["Assigned Seat No"]-1)//len(self.guest_list))+1

        # Table_Arrangement.sort_values(by=['Assigned Table No'])

        for i in range(1,self.num_tables+1):
            Table_Arrangement["Table No "+str(i)]=np.where(Table_Arrangement['Assigned Table No']!= i, 0, 1)
        Table_Arrangement_Transpose=Table_Arrangement.T
        initial_random_arrangement=Table_Arrangement_Transpose.tail(len(Table_Arrangement_Transpose)-3).values
        Table_Arrangement[["Guest Name","Assigned Table No"]]

        initial_random_arrangement_costs = np.dot(np.matrix(initial_random_arrangement), np.dot(self.relationships_matrix, initial_random_arrangement.T))



        result = self.anneal(initial_random_arrangement,temp=1.0, temp_min=0.00001, alpha=0.9, n_iter=100, audit=True)

        print("Cost Function Of Optimized Seating Arrangement:",self.cost(result[0]),"vs. Initial Seed Cost Function Value Of",np.trace(initial_random_arrangement_costs))
        print("NB: Lower Number = Better")

        multiplier_table=[]
        for i in range(1,self.num_tables+1):
            multiplier_table.append([i])
            
        suggested_arrangement=pd.DataFrame(np.array(result[0])*np.array(multiplier_table)).T
        suggested_arrangement.columns=Table_Arrangement.columns[-self.num_tables:]
        suggested_arrangement["Assigned_Table"]=suggested_arrangement.sum(axis=1)
        suggested_arrangement['Guest_Name']=Table_Arrangement['Guest Name']
        suggested_arrangement=suggested_arrangement[["Guest_Name","Assigned_Table"]]
        print(suggested_arrangement)
        print("Ordered By Table No")
        suggested_arrangement_by_tableNo=suggested_arrangement.sort_values(by=['Assigned_Table'])
        suggested_arrangement_by_tableNo[["Assigned_Table","Guest_Name"]]
        print(suggested_arrangement_by_tableNo)

        #handel file output
        df = suggested_arrangement_by_tableNo
        filename = 'output.json'
        output = {}
        for table_num in df.Assigned_Table.unique():
            output['table_'+str(int(table_num))] = list(df[df['Assigned_Table'] == table_num]['Guest_Name'])

        print('Wrinting output to '+filename)
        with open(filename, 'w') as fp:
            json.dump(output, fp)


