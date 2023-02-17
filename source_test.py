import source


def test(noOfGuests, num_tables, planner_preferences):
    #Test and presets
    guest_list=list(range(1, noOfGuests+1))


    #User input
    guest_list=["name_"+str(x) for x in guest_list]

    seating_list = source.seating_list(num_tables, guest_list, planner_preferences)
    seating_list.solve()


    

if __name__ == "__main__":

    try:
        planner_preferences = [
            {
                "preference": "avoid",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "avoid",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_1", "name_3"]
            }
        ]
        test(10, 3, planner_preferences)
    except Exception as e: print(e)

    try:
        planner_preferences = [
            {
                "preference": "avoid",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "avoid",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_1", "name_3"]
            }
        ]
        test(10, 1, planner_preferences)
    except Exception as e: print(e)

    try:
        planner_preferences = [
            {
                "preference": "avoid",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "avoid",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_1", "name_3"]
            }
        ]
        test(10, 2, planner_preferences)
    except Exception as e: print(e)

    try:
        planner_preferences = [
            {
                "preference": "pair",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "pair",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_1", "name_3"]
            }
        ]
        test(10, 2, planner_preferences)
    except Exception as e: print(e)

    try:
        planner_preferences = [
            {
                "preference": "pair",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "pair",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_4", "name_5"]
            }
        ]
        test(10, 15, planner_preferences)
    except Exception as e: print(e)

    try:
        planner_preferences = [
            {
                "preference": "pair",
                "guests": ["name_1", "name_2"]
            },
            {
                "preference": "pair",
                "guests": ["name_2", "name_3"]
            },
            {
                "preference": "avoid",
                "guests": ["name_4", "name_5"]
            }
        ]
        test(2, 15, planner_preferences)
    except Exception as e: print(e)
