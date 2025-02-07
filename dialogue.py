import streamlit as st
import openai

# Access the API key from Streamlit secrets
api_key = st.secrets["api_key"]

# OpenAI API Key
openai.api_key = api_key

# Function to generate lesson plan
def generate_lesson_plan(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating lesson plan: {str(e)}")
        return None

# Streamlit app
def main():
    st.title("Dialogue-Focused Lesson Plan Generator")

    # Input fields for teacher preferences
    grade = st.text_input('Grade', "8th")
    subject = st.text_input('Subject', "History")
    topic = st.text_input('Topic', "Great Depression")
    learning_objectives = st.text_area('Learning Objectives', "Students will examine how the economic practices of the 1920s contributed to the coming of the Great Depression.")

    if st.button('Generate Lesson Plan'):
        # Create prompt dynamically
        teacher_input = {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "learning_objectives": learning_objectives,
        }

        prompt_template = """
        You are a lesson plan generation assistant focused on promoting student agency. A teacher has provided the following details for a lesson:

        Grade: {grade}
        Subject: {subject}
        Topic: {topic}
        Learning Objectives: {learning_objectives}

        Please generate a detailed lesson that incorporates the following instructional phases throughout different parts of the lesson: 
        1.	Rote (Teacher-Class): Include opportunities for students to drill key facts, ideas, or routines through structured repetition. 
        2.	Recitation (Teacher-Class or Teacher-Group): Design a segment where students recall previously learned knowledge or deduce answers from teacher-provided clues
        3.	Instruction/Exposition (Teacher-Class, Teacher-Group, or Teacher-Individual): Ensure direct instruction or explanation is embedded in the lesson to introduce new concepts, procedures, or facts. 
        4.	Discussion (Teacher-Class, Teacher-Group, or Pupil-Pupil): Incorporate activities that encourage students to exchange ideas, explore concepts, and collaboratively solve problems. 
        5.	Dialogue (Teacher-Class, Teacher-Group, Teacher-Individual, or Pupil-Pupil): Integrate structured, cumulative questioning and guided discussions to clarify concepts and deepen understanding. 
        
        """

        prompt = prompt_template.format(
            grade=teacher_input["grade"],
            subject=teacher_input["subject"],
            topic=teacher_input["topic"],
            learning_objectives=teacher_input["learning_objectives"],
        )
       # Generate and display the lesson plan
        lesson_plan = generate_lesson_plan(prompt)
        st.write(lesson_plan)

if __name__ == "__main__":
    main()
