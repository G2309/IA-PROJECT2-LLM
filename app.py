# Dependencies
import streamlit as st
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.agents import create_csv_agent
from langchain_core.tools import Tool
from dotenv import load_dotenv
import datetime
import os

# Load environment variables
load_dotenv()

# Save and load history
def save_history(question, answer):
    with open("history.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} : {question} -> {answer}\n")

def load_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as f:
            return f.readlines()
    return []

# Main app function
def main():
    st.set_page_config(page_title="Agente Interactivo", page_icon=":robot:", layout="wide")

    # Sidebar options
    st.sidebar.header("Opciones de trabajo")
    options = [
        "Pantalla de inicio",
        "Usar Agente Python y CSV"
    ]
    selected_option = st.sidebar.selectbox("Selecciona una opción:", options)

    if selected_option == "Pantalla de inicio":
        st.markdown("""
        <style>
        @import url(https://fonts.googleapis.com/css?family=Press+Start+2P);

        html{
          background-color:#000;
          border-bottom:solid 5px blue;
          border-top:solid 5px blue;
          overflow-x:hidden;
          padding-bottom:142px;
        }

        body {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          background-color: #333;
          color: white;
        }

        p{
          color:#FFF;
          font: 50px 'Press Start 2P', cursive;
          margin:200px 139px;
          position:absolute;
          text-align:center;
        }

        p1{
          color:#FFF;
          font: 20px 'Press Start 2P', cursive;
          text-align:center;
        }

        .pacman{
          margin:40px 10px;
        }

        .pacman-top{
          background-color:yellow;
          height:100px;
          width:200px;
          border-radius:100px 100px 0 0;
          animation: spin1 0.5s infinite linear;
        }

        .pacman-bottom{
        background-color:yellow;
          height:100px;
          width:200px;
          border-radius:0 0 100px 100px;
          animation: spin2 0.5s infinite linear;
        }

        .feed {
        margin-top: -185px;
        margin-left:15px;
        width: 45px;
        height: 45px;
        border-radius: 30%;
        -moz-animation: eat 1s linear 0s infinite;
        -webkit-animation: eat 1s linear 0s infinite;
        animation: eat 1s linear 0s infinite;
        }   

        /* Animation*/

        @keyframes spin1 {
            0%  {transform: rotate(0deg);}
            50%{transform: rotate(-35deg);}
        }
        @keyframes spin2 {
            0%  {transform: rotate(0deg);}
          50%{transform: rotate(35deg);}  
        }

        @-moz-keyframes spin1 {
            0%  {transform: rotate(0deg);}
            50%{transform: rotate(-35deg);}

        }
        @-moz-keyframes spin2 {
            0%  {transform: rotate(0deg);}
          50%{transform: rotate(35deg);}  
        }

        @-webkit-keyframes spin1 {
            0%  {transform: rotate(0deg);}
            50%{transform: rotate(-35deg);}
        }
        @-webkit-keyframes spin2 {
            0%  {transform: rotate(0deg);}
          50%{transform: rotate(35deg);}  
        }

        @keyframes eat {
            0% { box-shadow: 
              100px 65px 0 0 white, 
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white,
              900px 65px 0 0 white, 
              1100px 65px 0 0 white, 
              1300px 65px 0 0 white;}

          100% { box-shadow: 
              0px 65px 0 0 white, 
              100px 65px 0 0 white,
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white, 
              900px 65px 0 0 white, 
              1100px 65px 0 0 white;}
        }

        @-moz-keyframes eat {
            0% { box-shadow: 
              100px 65px 0 0 white, 
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white,
              900px 65px 0 0 white, 
              1100px 65px 0 0 white, 
              1300px 65px 0 0 white;}

          100% { box-shadow: 
              0px 65px 0 0 white, 
              100px 65px 0 0 white,
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white, 
              900px 65px 0 0 white, 
              1100px 65px 0 0 white;}
        }

        @-webkit-keyframes eat {
            0% { box-shadow: 
              100px 65px 0 0 white, 
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white,
              900px 65px 0 0 white, 
              1100px 65px 0 0 white, 
              1300px 65px 0 0 white;}

          100% { box-shadow: 
              0px 65px 0 0 white, 
              100px 65px 0 0 white,
              300px 65px 0 0 white, 
              500px 65px 0 0 white, 
              700px 65px 0 0 white, 
              900px 65px 0 0 white, 
              1100px 65px 0 0 white;}
        }
        </style>
        <div class="pacman">
        <div class="pacman-top"></div>
        <div class="pacman-bottom"></div>
        <div class="feed"></div>
        </div>

        <p1>Gustavo Adolfo Cruz Bardales - 22779</p1>
        <br>
        <p1>Proyecto 2</p1>
        """, unsafe_allow_html=True)

    elif selected_option == "Usar Agente Python y CSV":
        st.title("Agente Interactivo con Python y CSV")

        # Instructions for the app
        st.markdown("""
        ### Instrucciones:
        - Este agente puede responder preguntas usando Python o realizar análisis sobre archivos CSV.
        - Puedes elegir entre solicitudes predefinidas o escribir tus propias preguntas.
        - Usa el botón correspondiente para ejecutar las tareas.
        """)

        # Setup agents
        base_prompt = hub.pull("langchain-ai/react-agent-template")
        instructions = """
            Eres un agente diseñado para responder preguntas utilizando Python o analizando archivos CSV.
            Usa el código de Python 3.11 para responder preguntas.
            Solo responde después de ejecutar el código necesario. Si no puedes responder, escribe 'No sé la respuesta'.
        """
        prompt = base_prompt.partial(instructions=instructions)

        # Define tools
        tools = [PythonREPLTool()]
        python_agent = create_react_agent(
            prompt=prompt,
            llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
            tools=tools
        )
        python_agent_executor = AgentExecutor(agent=python_agent, tools=tools, verbose=True)

        csv_agent = create_csv_agent(
            llm=ChatOpenAI(temperature=0, model="gpt-4"),
            path="data.csv",  # Replace with your CSV file path
            verbose=True,
            allow_dangerous_code=True,
        )

        # Wrapper for agents
        def python_agent_wrapper(prompt):
            return python_agent_executor.invoke({"input": prompt})

        tools = [
            Tool(
                name="Python Agent",
                func=python_agent_wrapper,
                description="Use this agent to write and execute Python code."
            ),
            Tool(
                name="CSV Agent",
                func=csv_agent.invoke,
                description="Use this agent to analyze CSV data."
            ),
        ]

        grand_agent = create_react_agent(
            llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
            tools=tools,
            prompt=prompt,
        )
        grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

        # Predefined tasks
        st.sidebar.header("Opciones de tarea")
        options = [
            "Haz un codigo para 'Hello World' en Python",
            "Haz una calculadora en Python",
            "Haz un ejemplo de uso de diccionarios en Python"
        ]
        task = st.sidebar.selectbox("Selecciona una tarea:", options)

        if st.sidebar.button("Ejecutar tarea seleccionada"):
            try:
                result = python_agent_wrapper(task)
                st.success("Resultado:")
                st.code(result["output"], language="python")
                save_history(task, result["output"])
            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Custom questions
        st.header("Haz una pregunta al agente")
        question = st.text_input("Escribe tu pregunta aquí:")
        if st.button("Ejecutar pregunta"):
            try:
                result = grand_agent_executor.invoke({"input": question})
                st.success("Resultado:")
                st.code(result["output"], language="python")
                save_history(question, result["output"])
            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Display history
        st.header("Historial")
        history = load_history()
        if history:
            for entry in history:
                st.text(entry)
        else:
            st.info("No hay historial todavía.")

if __name__ == "__main__":
    main()
