import source


def test1(noOfGuests, num_tables):
    #Test and presets
    noOfGuests=10
    guest_list=list(range(1, noOfGuests+1))


    #User input
    num_tables = 2
    guest_list=["name_"+str(x) for x in guest_list]
    planner_preferences = [
        {
            "preference": "avoid",
            "guests": ["name_1", "name_2"]
        },
        {
            "preference": "avoid",
            "guests": ["name_2", "name_4"]
        },
        {
            "preference": "avoid",
            "guests": ["name_1", "name_4"]
        }
    ]

    seating_list = source.seating_list(num_tables, guest_list, planner_preferences)
    seating_list.solve()


    

if __name__ == "__main__":
    main()