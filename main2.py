import json
import re
import pandas as pd
from tokenizer import *
from token_parser import *


with open("courses.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame.from_records(data)


parsed = []


# Brackets are escaped cause regex
useless_phrases = ["is strongly recommended",
                   "is recommended", "Take", "\(may be taken concurrently\)", "\([\w ]*or equivalent\)", r"Prerequisite\(s\): "]

for text in df["prerequisites"].to_list():
    # Remove courses
    # temp = re.sub(r"\w{2,4}\*[0-9]{4}", "___", text)
    temp = text

    # Remove useless phrases
    temp = re.sub(r"|".join(useless_phrases), "", temp)

    parsed.append(temp)

print(len(set(parsed)))


# First Brackets @ 9
# First n of @ 17

print("\n")

tree_dicts = []

for text in parsed:
    print(text, end=" -> ")
    print(Tokenizer(text).tokens)
    print()
    parser = Parser(Tokenizer(text).tokens)
    parser.tokens = parser.convert_n_of_to_or()
    print(parser.tokens)
    print()
    print(parser.gen_tree())
    print(parser.to_dict(parser.gen_tree()))
    tree_dicts.append(parser.to_dict(parser.gen_tree()))

for index, course in enumerate(data):
    course["parsed_prerequisites"] = tree_dicts[index]


def check_node(sub_dict: dict):
    # Recursively check if any child is of type Node
    if isinstance(sub_dict, dict):
        if "children" in sub_dict:
            result = True
            for child in sub_dict["children"]:
                result = result and check_node(child)

            if result:
                return True

            raise Exception("Node Found")

        return True

    elif isinstance(sub_dict, list):
        result = True
        for child in sub_dict:
            result = result and check_node(child)

        if result:
            return True

    raise Exception("Node Found")


check_node(tree_dicts)

with open("tree_dicts.json", "w") as f:
    json.dump(data, f, indent=4)


# print("\n\n\n")

# print(*set([tuple(Tokenizer(text).tokens) for text in parsed[:100]]), sep="\n")
