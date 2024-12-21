import os
import google.generativeai as genai

# image_path_1 = 'img1.jpg'  # Replace with the actual path to your first image
# image_path_2 = 'img2.jpg' # Replace with the actual path to your second image


#Choose a Gemini model.


prompt = "Select a desh Based on the mood of the user and available item list  and select the recipe from the image given"
def create_llm(api_key):
    genai.configure(api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
def take_input(available_item_list,image_list:list):
    choice = input("what kind of desh you wanna eat today: ")
    
    response = model.generate_content([prompt,available_item_list, image_list, choice])
    print(response.text)
