import markovify
import sys
import re

if len(sys.argv) < 2:
    print("Specify file as the first argument")
    exit(1)
else:
    with open(sys.argv[1], "r") as f:
            text = f.read()
    print("Generating the model...")
    text = re.sub("<delimiter>", "\n", text)
    text_model = markovify.Text(text)
    starting_words_count = len([key for key in text_model.chain.model.keys() if "___BEGIN__" in key])
    print(f"Model generated. # of starting words: {starting_words_count}")
    print("Exporting the model to JSON...")
    model_json = text_model.to_json()
    with open("mkmodel.json", "w") as f:
            f.write(model_json)
            print("mkmodel.json written successfully")
