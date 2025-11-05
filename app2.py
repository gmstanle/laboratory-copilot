import os
openai_api_key = os.environ.get("OPENAI_API_KEY")
max_token_small = 300
max_token_limit = 1000

import json
from openai import OpenAI

model = 'gpt-4-1106-preview'

def response_json(chat_history, max_token_limit=2500):
  return client.chat.completions.create(model=model,
    response_format={ "type": "json_object" },
    messages=chat_history,
    max_tokens=max_token_limit,
    temperature=0.0)


client = OpenAI(api_key=openai_api_key)

print("Running")
# Biological System
model_organism = input("What is your model organism?: ")
organ = input("What organ are we analyzing: ")
measurement = input("What is the measurement we're performing on our biological system?: ") #rna sequencing, ATAC-sea, RT-qPCR, flow cytometry

# model_organism = "mouse"
# organ = "lung"
# measurement = "single-cell RNA seq 10x genomics chromium chip"




initial_prompt = f'''You are responsible for generating a detailed experiment protocol.
You are working with {model_organism}, specifically looking at the {organ}. We are trying to measure the following: {measurement}.

Before you provide a detailed protocol, please consider the experiment carefully and generate a list of questions for your supervisor. Example questions could include "What type of Sequencing Machine are you using?"

Provide a JSON output of the questions you would ask your supervisor before generating a detailed list of 
steps to take to generate the data. Keep in mind that you will need to provide all details, 
including quantities and timings that a novice lab technician would need to successfully complete the experiment. 
Provide a JSON with no more than 3 question.

DO NOT ASK GENERAL QUESTIONS, ESPECIALLY ABOUT THE PURPOSE OF THE EXPERIMENT!

Use the following format for each question:
    {{
        "questions": [
            {{"question": "What is the specific strain and age of the mice we are using for the lung single-cell RNA-seq experiment?"}},
            {{"question": "What is the target cell recovery number for the 10x Genomics Chromium chip, and do we have a preferred range of cell viability?"}},
            {{"question": "Which sequencing depth and read length are we aiming for, and is there a specific 10x Genomics library kit or version we should use for this experiment?"}}
        ]
    }}
'''



design_prompt = f'''Please generate a detailed experiment protocol.
You are working with {model_organism}, specifically looking at the {organ}. We are trying to measure the following: {measurement}.

Please consider the experiment carefully and generate a detailed list of steps to take to generate the data.

For each step in the experiment protocol, please provide the following information:
* Detailed instruction
* Consumables required (do not specify quantities)
* Safety Equipment Required (do not specify quantities)
* Lab Equipment (do not specify quantities)
* Details on timing

Return your answer in the following JSON format:

{{ "experiment_steps": [
    {{
      "step_number": 1,
      "instruction": "Prepare the extraction solution.",
      "consumables_required": [
        {{"item": "70% ethanol"}},
        {{"item": "salt"}}
      ],
      "safety_equipment_required": [
        {{"item": "Gloves"}},
        {{"item": "Goggles"}}
      ],
      "lab_equipment": [
        {{"item": "beaker"}},
        {{"item": "stirring rod"}},
      ],
      "details_on_timing": "Allow the solution to mix thoroughly for about 2 minutes."
    }},
    {{
      "step_number": 2,
      "instruction": "Break down the fruit to release cell contents.",
      "consumables_required": [
        {{"item": "ripe banana"}},
        {{"item": "salt"}}
      ],
      "safety_equipment_required": [
        {{"item": "Goggles"}}
      ],
      "lab_equipment": [
        {{"item": "blender"}}
      ],
      "details_on_timing": "Mash the banana thoroughly in the bag for about 5 minutes."
    }}}}


Keep in mind that you will need to provide all details, including quantities and timings that a novice lab technician would need to successfully complete the experiment.

BE SPECIFIC! USE MARKDOWN FORMAT! Do high quality work. Your career depends on this.
'''



quantity_prompt = '''Take the previous JSON output and update it to provide the quantities of each consumable, safety equipment, and lab equipment required for the experiment.

Do not change other elements of the prompt. Your format should be:

Return your answer in the following JSON format:

{{ "experiment_steps": [
    {{
      "step_number": 1,
      "instruction": "Prepare the extraction solution.",
      "consumables_required": [
        {{"item": "70% ethanol", "quantity": "100", "unit": "ml"}},
        {{"item": "salt", "quantity": "1", "unit": "teaspoon"}}
      ],
      "safety_equipment_required": [
        {{"item": "Goggles", "quantity": "1", unit: "pair"}},
        {{"item": "Gloves", "quantity": "1", unit: "pair"}}
      ],
      "lab_equipment": [
        {{"item": "beaker", "quantity": "1", "unit": "count"}},
        {{"item": "stirring rod", "quantity": "1", "unit": "count"}},
      ],
      "details_on_timing": "Allow the solution to mix thoroughly for about 2 minutes."
    }},
    {{
      "step_number": 2,
      "instruction": "Break down the fruit to release cell contents.",
      "consumables_required": [
        {{"item": "ripe banana", "quantity": "1", unit: "count"}},
        {{"item": "salt", "quantity": "1", unit: "teaspoon"}}
      ],
      "safety_equipment_required": [
        {{"item": "Goggles", "quantity": "1", unit: "pair"}}
      ],
      "lab_equipment": [
        {{"item": "blender", "quantity": "1", unit: "count"}}
      ],
      "details_on_timing": "Mash the banana thoroughly in the bag for about 5 minutes."
    }}}}
'''

chat_history = [
    {"role": "system", "content": "You are a knowledgeable experiment designer in the biotech space."},
    {"role": "user", "content": initial_prompt}
]

# print(initial_prompt)
# Call GPT-4 to generate a response
response = client.chat.completions.create(model=model,
    response_format={ "type": "json_object" },
    messages=chat_history,
    max_tokens=max_token_small,
    temperature=0.0)
# print("\n")

output_data = response.choices[0].message.content

try:
    # Attempt to parse the JSON
    data = json.loads(output_data)
    # Iterate through questions in the JSON data
    for item in data['questions']:
        print(item['question'])  # Print the question for clarity in this example
        answer = input("Your answer: ")
        chat_history.append({"role": "system", "content": item['question']})
        chat_history.append({"role": "user", "content": answer})
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)

chat_history.append({"role": "user", "content": design_prompt})


# Call GPT-4 to generate a response for the design prompt
print("***Generating Steps***")
response = response_json(chat_history, max_token_limit=max_token_limit)
experiment_design = response.choices[0].message.content
chat_history.append({"role": "system", "content": experiment_design})

chat_history.append({"role": "user", "content": quantity_prompt})
# print(experiment_design)
print("***Updating Quantities***")

# Call GPT-4 to generate a response including quantities
response = response_json(chat_history, max_token_limit=max_token_limit)

experiment_design = response.choices[0].message.content
# print(experiment_design)

lab_equipment_set = set()
consumables_set = set()
safety_equipment_set = set()

# Parse the JSON string into a Python dictionary
try:
  set_data = json.loads(experiment_design)
  # Define sets to collect unique items

  # print("set data", set_data)
  # Iterate through each step in the experiment
  for step in set_data['experiment_steps']:
      # Collect lab equipment
      for equipment in step['lab_equipment']:
          lab_equipment_set.add((equipment['item'], equipment['quantity'], equipment['unit']))

      for equipment in step['lab_equipment']:
          lab_equipment_set.add((equipment['item'], equipment['quantity'], equipment['unit']))
      
      # Collect consumables required
      for consumable in step['consumables_required']:
          consumables_set.add((consumable['item'], consumable['quantity'], consumable['unit']))
      
      # Collect safety equipment required
      for safety in step['safety_equipment_required']:
          safety_equipment_set.add((safety['item'], safety['quantity'], safety['unit']))

  # Print out the sets
  # print("Lab Equipment Required:")
  # for equipment in lab_equipment_set:
      # print(f"{equipment[0]}: {equipment[1]} {equipment[2]}")

  # print("\nConsumables Required:")
  # for consumable in consumables_set:
  #     # print(f"{consumable[0]}: {consumable[1]} {consumable[2]}")

  # print("\nSafety Equipment Required:")
  # for safety in safety_equipment_set:
  #     print(f"{safety[0]}: {safety[1]} {safety[2]}")
except json.JSONDecodeError as e:
    # print("Failed to decode JSON:", e)
    set_data = experiment_design  # Handle the error by setting to an empty dictionary or suitable default


final_prompt = '''Please provide a detailed experiment protocol from the following information:
Consumables Required: {consumables_set}
Lab Equipment Required: {lab_equipment_set}
Safety Equipment Required: {safety_equipment_set}
Full Detail on Steps: {set_data}

Use Markdown to write a detailed protocol for the experiment, with the following sections:
# Catchy Experiment Name

## Objective:

## Safety Equipment Required
 Be sure to include quantity

## Lab Equipment Required
 Be sure to include quantity

## Consumables Required
  Be sure to include quantity

## Step-by-Step Protocol
 Include all relevant details, including timing and quantities for each step. Be sure the details are sufficient to allow a novice lab technician would need to successfully complete the experiment.
 
## Expected Results
  Be sure to include what you expect to see at the end of the experiment.

## Additional Notes
Anything else to consider
'''
chat_history.append({"role": "user", "content": final_prompt})


# Call GPT-4 to generate a response
response = client.chat.completions.create(model=model,
    messages=chat_history,
    max_tokens=max_token_limit,
    temperature=0.0)

experiment_design = response.choices[0].message.content

# answer = input("(Optional) Provide feedback before re-generating a new protocol): ")

chat_history.append({"role": "user", "content": experiment_design})

# # Call GPT-4 to generate a response
# response = client.chat.completions.create(model=model,
#     messages=chat_history,
#     max_tokens=max_token_limit,
#     temperature=0.0)

# print("Complete Chat History:\n", chat_history)

print("PROPOSED EXPERIMENT PROTOCOL:\n",experiment_design)