# Reads video_games_raw.csv with pandas, lets the user inspect
# one game by row number and change its status, adds a
# Recommended column, shows the recommended games, and saves
# everything to video_games_cleaned.csv. The original file is
# never changed.

import pandas as pd

lstStatuses = ["Backlog", "Playing", "Completed", "Dropped"]


def main():
    print("VIDEO GAME CATALOG MANAGER")

    # Read the original catalog. It must be in the same folder as this program.
    try:
        dfGames = pd.read_csv("video_games_raw.csv")
    except FileNotFoundError:
        print("Could not find video_games_raw.csv. Put it in the same folder as game_catalog.py.")
        return

    iLastRow = len(dfGames) - 1

    # Ask for a row number until the user enters one that exists
    bValidRow = False
    while not bValidRow:
        sRow = input("Enter a row number to inspect: ")
        try:
            iRow = int(sRow)
            if iRow >= 0 and iRow <= iLastRow:
                bValidRow = True
            else:
                print(f"Please enter a row number from 0 to {iLastRow}.")
        except ValueError:
            print(f"'{sRow}' is not a number. Please enter a row number from 0 to {iLastRow}.")

    # .iloc[] gets the row by its position
    serGame = dfGames.iloc[iRow]
    print("\nSelected Game:")
    print(f"Title: {serGame['Title']}")
    print(f"Platform: {serGame['Platform']}")
    print(f"Genre: {serGame['Genre']}")
    print(f"Rating: {serGame['Rating']}")
    print(f"Current Status: {serGame['Status']}")

    # Ask for a new status until the user enters one of the four allowed values
    bValidStatus = False
    while not bValidStatus:
        print("\nEnter a new status:")
        sStatus = input().strip().title()   # "completed" becomes "Completed"
        if sStatus in lstStatuses:
            bValidStatus = True
        else:
            print("Status must be Backlog, Playing, Completed, or Dropped.")

    # .at[] changes one specific value: this row's Status
    dfGames.at[iRow, "Status"] = sStatus

    # Add the Recommended column. Every game starts as "No", then .loc[]
    # changes all the rows that meet both criteria to "Yes" at once.
    dfGames["Recommended"] = "No"
    dfGames.loc[(dfGames["Rating"] >= 8) & (dfGames["Price"] <= 40), "Recommended"] = "Yes"

    # .query() filters the catalog down to the recommended games
    dfRecommended = dfGames.query("Recommended == 'Yes'")
    print("\nRecommended Games:")
    print(dfRecommended[["Title", "Platform", "Price", "Rating"]])

    # Save to a new file so the original CSV stays unchanged
    dfGames.to_csv("video_games_cleaned.csv", index=False)
    print("\nThe catalog has been updated.")
    print("Saved as video_games_cleaned.csv.")


main()