"""
Jank Flappy Birb - Buttons (refer to main.py for full header)

Author: Adam Long

License: No license, freedom of use in commerical or non-commerical contexts. I do ask
that you contact me via email (adam.jacob.long@gmail.com) if you plan on using my work
within your own project.
"""

from datetime import datetime
import os
import json as json_jazz


def check_high_score(new_score, difficulty):
    """
                    Description:
                        Checks high_scores.json to see if a new high score has been reached.
                        If high_scores.json is not found then creates the directories & files
                        needed while filling them with default data.

                    Parameters:
                        new_score - The score to be checked. Integer.
                        difficulty - The level's difficulty level when played. String.

                    Returns:
                        True: if the new score is the highest score.
                        False: if the new score is not the highest score.
                        True: if high_scores.json is not found.

                    Raises:
                        OSError - Unable to create file.

                    Example:
                        *start of program*
                        *round ends*
                        if check_high_score(123):
                           high_score_data_write(123):
                        *...*

                    """
    try:
        with open("data_files/high_scores.json", "r") as read_file:
            loaded_data = json_jazz.load(read_file)
            read_file.close()

        if loaded_data["highest"][1] > new_score:
            return False
        else:
            return True

    except FileNotFoundError:
        new_dict = {
            "highest":
                [str(datetime.now()), new_score, difficulty],
            "previous": []
        }
        try:
            os.mkdir("./data_files")

            with open("data_files/high_scores.json", "w") as new_file:
                json_jazz.dump(new_dict, new_file)
                new_file.close()
        except IsADirectoryError:

            with open("data_files/high_scores.json", "w") as new_file:
                json_jazz.dump(new_dict, new_file)
                new_file.close()

        return True

def high_score_data_write(new_score, difficulty):
    """
                Description:
                    Writes the new highest score to the high_scores.json file.

                Parameters:
                    new_score - The new high score to be written. Integer.
                    difficulty - The level's difficulty level when played. String.

                Returns:
                    N/A

                Raises:
                    FileNotFoundError - Unable to find high_scores.json

                Example:
                    *start of program*
                    *round ends where a new high score has been achieved*
                    high_score_data_write(123)
                    *...*

                """
    time_instance = str(datetime.now())

    with open("data_files/high_scores.json", "r") as write_file:
        loaded_data = json_jazz.load(write_file)
        write_file.close()

        new_previous_score = loaded_data["highest"]
        new_high_score = [time_instance, new_score, difficulty]

        loaded_data["previous"].append(new_previous_score)
        loaded_data["highest"] = new_high_score

    with open("data_files/high_scores.json", "w") as override_file:
        json_jazz.dump(loaded_data, override_file)
        override_file.close()

def high_score_data_read():
    """
                Description:
                    Reads the current highest score from the high_scores.json file.

                Parameters:
                    N/A

                Returns:
                    Integer - Current highest score.

                Raises:
                    FileNotFoundError - Unable to find high_scores.json

                Example:
                    *start of program*
                    high_score_data_read()
                    *prints high score to screen*
                    *...*

                """

    with open("data_files/high_scores.json", "r") as read_file:
        loaded_data = json_jazz.load(read_file)
        read_file.close()

    return loaded_data["highest"][1]