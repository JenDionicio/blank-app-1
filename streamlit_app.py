import streamlit as st
# import replicate
# import time
# import os
# from dotenv import load_dotenv

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Fetch the API token from .env

# Initialize the Replicate client with the API token
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

st.title("Personalized Nutritious Meal Suggestion")

# Collect demographic data
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=100)
gender = st.selectbox("Select your gender:", options=["Male", "Female", "Other"])

st.subheader("Food Preferences")

# Create a multiselect for the user's preferences
preferences = st.multiselect("Select your preferred food types:",
                             options=["Vegetarian", "Vegan", "Gluten-Free", 
                                      "Dairy-Free", "Low-Carb", "High-Protein"])

# Collect three favorite foods
favorite_food_1 = st.text_input("Enter your first favorite food:")
favorite_food_2 = st.text_input("Enter your second favorite food:")
favorite_food_3 = st.text_input("Enter your third favorite food:")

# Step 3: Validate the favorite foods entered
if st.button("Verify Foods"):
    st.write(f"Your top 3 favorite foods are: {favorite_food_1}, {favorite_food_2}, {favorite_food_3}")

# Initialize meal_suggestion in session state if it doesn't exist
if 'meal_suggestion' not in st.session_state:
    st.session_state.meal_suggestion = ""

# Button to generate meal suggestion
if st.button("Generate Meal Suggestion"):
    
    # Simple logic to suggest a meal
    if "Vegetarian" in preferences:
        st.session_state.meal_suggestion = "Quinoa Salad with mixed vegetables and tofu"
    elif "Vegan" in preferences:
        st.session_state.meal_suggestion = "Chickpea and vegetable stir fry"
    elif "Gluten-Free" in preferences:
        st.session_state.meal_suggestion = "Grilled chicken with sweet potatoes"
    else:
        st.session_state.meal_suggestion = "Grilled salmon with a side of leafy greens"

    # Display meal suggestion
    st.subheader(f"Suggested Meal for {name}:")
    st.write(st.session_state.meal_suggestion)

    # Generate the prompt based on the suggestion and preferences
    st.subheader("Meal Prompt")
    if len(preferences) > 0:
        st.write(f"Meal that contains nutrients from {st.session_state.meal_suggestion}, with a texture suitable for a {preferences[0]} diet.")
    else:
        st.write(f"Meal that contains nutrients from {st.session_state.meal_suggestion}, with a texture suitable for your diet preferences.")

# Simulate sending the prompt to Google Gemini (mockup)
st.write("**Note**: This is a mockup for generating an image with Google Gemini based on the meal prompt. "
         "In the real application, this would send the following prompt to an API like Google Gemini.")

# Generate Image
if st.button("Generate Image"):
    # Check if meal suggestion and preferences are set
    if st.session_state.meal_suggestion and len(preferences) > 0:
        with st.spinner('Generating image…'):
            start_time = time.time()
            try:
                output = replicate_client.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "width": 1024,
                        "height": 1024,
                        "prompt": f"Meal that contains nutrients from {st.session_state.meal_suggestion}, with a texture suitable for a {preferences[0]} diet.",
                        "refine": "expert_ensemble_refiner",
                        "num_outputs": 1,
                        "apply_watermark": False,
                        "negative_prompt": "low quality, worst quality",
                        "num_inference_steps": 25
                    }
                )

                # Assuming the output contains a URL to the generated image
                if isinstance(output, list) and len(output) > 0:
                    st.image(output[0])  # Displaying the image
                else:
                    st.error("Failed to generate image. Please try again.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

            end_time = time.time()
            elapsed_time = end_time - start_time
            st.write(f"Image generated in {elapsed_time:.2f} seconds")
    else:
        st.error("Meal suggestion or preferences not found. Please generate a meal suggestion first.")
