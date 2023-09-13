# student.py
# defines a Student class that reprents a student with name, student_id, quiz_scores
import re
from enum import Enum
from typing import Dict


class Student:
    # def __init__(self, name, student_id, quiz_scores):

    def __init__(self, full_name: str, student_email: str, res_dict: Dict[str, float]):
        self.student_full_name = full_name
        self.student_email = student_email
        self.res_dict = res_dict
        self.make_floats()
        self.lowercase_res_dict = self.modify_res_dict()
        self.changed_quizzes = {}
        self.comment = ""

    def make_floats(self):
        for key in self.res_dict.keys():
            self.res_dict[key] = float(self.res_dict[key])

    def bonus_retest_score(self, main_quiz_name: str, pattern: str):
        returned_scores = {}
        for key in self.lowercase_res_dict.keys():
            modified_key = ""
            pattern_exists = re.search(pattern=pattern, string=key)
            if pattern_exists:
                modified_key = key.replace(pattern_exists.group(), "")
            main_quiz_name_exists = re.search(pattern=main_quiz_name, string=modified_key)
            if main_quiz_name_exists and pattern_exists:
                quiz_type = pattern_exists.group()
                quiz_score = self.lowercase_res_dict[key][1]
                returned_scores[quiz_type] = quiz_score
        return returned_scores

    def modify_res_dict(self):
        modified_res_dict = {}
        for key, val in self.res_dict.items():
            modified_key_with_letters_and_nums = re.sub(r'[^a-zA-Z0-9]', '', key)
            modified_key_lowercase = modified_key_with_letters_and_nums.lower()
            modified_res_dict[modified_key_lowercase] = [key, val]
        return modified_res_dict

    def perform_logic(self):
        # If quiz score is greater than 80, then don't do anything
        # Else:
        # If there is bonus or retest score:
        # If bonus or retest is over 80, then make main score 80 and save the three scores
        # Else:
        # Set the max between main and bonus/retest to be main score, and save the three

        # Iterate over all keys that have become lowercase
        for name in self.lowercase_res_dict.keys():
            # Initialize original scores to be updated if main score gets updated
            orig_bonus_score = 0
            orig_retest_score = 0
            orig_main_score = 0
            # If current value is greater than 80, move to the next key
            not_main_quiz = re.search("bonus|retest", name)
            if not_main_quiz:
                continue
            else:
                curr_main_quiz_name = self.lowercase_res_dict[name][0]
                curr_main_score = float(self.lowercase_res_dict[name][1])
                if curr_main_score >= 80:
                    continue
                else:
                    bonus_retest_quizzes = self.bonus_retest_score(main_quiz_name=name,
                                                                   pattern="bonus|retest")
                    if bonus_retest_quizzes:
                        orig_main_score = float(curr_main_score)
                        if bonus_retest_quizzes.get("bonus"):
                            orig_bonus_score = float(bonus_retest_quizzes["bonus"])
                        if bonus_retest_quizzes.get("retest"):
                            orig_retest_score = float(bonus_retest_quizzes["retest"])

                        # checking here whether "bonus" or "retest"
                        if orig_main_score >= 75:
                            score_to_replace = orig_bonus_score
                        else:
                            score_to_replace = orig_retest_score

                        if score_to_replace >= 80:
                            self.res_dict[curr_main_quiz_name] = 80
                            self.comment = ("Main Score- {}, "
                                            "Bonus Score- {}, "
                                            "Retest Score- {}".format(orig_main_score,
                                                                      orig_bonus_score,
                                                                      orig_retest_score))
                            self.changed_quizzes[self.lowercase_res_dict[name][0]] = self.comment
                        else:
                            if orig_main_score > 0:
                                if score_to_replace == 0:
                                    self.comment = ("Please check the portal for the student quiz if the main quiz is "
                                                    "attempted twice (because there is no retest score)\n: Main "
                                                    "Score- {},"
                                                    "Bonus Score- {}, "
                                                    "Retest Score- {}".format(orig_main_score, orig_bonus_score,
                                                                              orig_retest_score))
                                    self.changed_quizzes[self.lowercase_res_dict[name][0]] = self.comment
                                # if curr_main_score > 0:  ##this condition should be when score_to_replace <80
                                else:
                                    if score_to_replace < 80:
                                        self.res_dict[curr_main_quiz_name] = max(orig_main_score, score_to_replace)
                                        self.comment = ("Main Score- {}, "
                                                        "Bonus Score- {}, "
                                                        "Retest Score- {}".format(orig_main_score,
                                                                                  orig_bonus_score,
                                                                                  orig_retest_score))
                                        self.changed_quizzes[self.lowercase_res_dict[name][0]] = self.comment
