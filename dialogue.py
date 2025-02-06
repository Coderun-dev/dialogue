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
    st.title("Student Agency-Focused Lesson Plan Generator")

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

        Please generate a detailed lesson plan that integrates a balanced sequence of dialogue types, as outlined by Alexander (2008). The lesson should include the following instructional talk phases, each aligned with a clear purpose:
        1. Rote (Teacher-Class): Introduce key facts, terminology, or foundational concepts through structured repetition to reinforce memory and establish baseline knowledge.
        2. Recitation (Teacher-Class or Teacher-Group): Use recall-based questioning to check students' retention and comprehension of prior learning, prompting them to retrieve information or deduce answers from contextual cues.
        3. Instruction/Exposition (Teacher-Class, Teacher-Group, or Teacher-Individual): Provide direct instruction, explanations, or demonstrations that clarify concepts, principles, or procedures essential for progressing in the lesson.
        4. Discussion (Teacher-Class, Teacher-Group, or Pupil-Pupil): Facilitate an open exchange of ideas where students collaborate, analyze perspectives, and co-construct understanding to deepen engagement with the topic.
        5. Dialogue (Teacher-Class, Teacher-Group, Teacher-Individual, or Pupil-Pupil): Guide structured, cumulative questioning and discourse to scaffold deeper learning, clarify misconceptions, and support students in making meaningful connections.

        Please generate a detailed lesson plan including Grade, Subject, Topic, Opening, Introduction, Guided Practice, Independent Practice, Closing, Assessment, Extension Activity, and Homework.
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
