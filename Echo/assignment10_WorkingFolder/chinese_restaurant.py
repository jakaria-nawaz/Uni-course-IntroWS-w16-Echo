import random
import json
import matplotlib.pyplot as plt

def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    #for all other customers do
    for cust in range(2, customers+1):
            # rand between 0 and 1
            rand = random.random()
            # Total probability to sit at a table
            prob = 0
            # No table found yet
            table_found = False
            # Iterate over tables
            for table, guests in enumerate(tables):
                # calc probability for actual table an add it to total probability
                prob += float(guests) / float(cust)
                # If rand is smaller than the current total prob., customer will sit down at current table
                if rand < prob:
                    # incr. #customers for that table
                    tables[table] += 1
                    # customer has found table
                    table_found = True
                    # no more tables need to be iterated, break out for loop
                    break
            # If table iteration is over and no table was found, open new table
            if not table_found:
                tables.append(1)
    return tables

def giniIt(list_of_values):
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area

def giniPlot(dist_list):
    dist_list = sorted(dist_list)
    var_dist_list = []
    var_gini_list = []
    for x in dist_list:
        var_dist_list.append(x)
        g = giniIt(var_dist_list)
        var_gini_list.append(g)
    plt.plot(var_dist_list, var_gini_list)
    plt.title('')
    plt.ylabel('Gini coefficient')
    plt.xlabel('Subjects (Customer Distribution in Tables)')
    plt.grid('on')
    plt.show()

restaurants = 1000
for i in range(5):
    dist_list = generateChineseRestaurant(restaurants)
    g = giniIt(dist_list)
    print dist_list, 'Gini coefficient = ', g
    giniPlot(dist_list)
    print '\n'

# network = generateChineseRestaurant(restaurants)
# with open('network_' + str(restaurants) + '.json', 'w') as out:
#     json.dump(network, out)
