import streamlit as st
from database import SessionLocal, engine
from models import Base
from crud import add_task, list_tasks, mark_completed, export_tasks_to_json, import_tasks_from_json, delete_task_by_id

Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()

st.title("Gestor de Tareas 📝")

menu = ["Agregar Tarea", "Listar Tareas", "Marcar Completada", "Eliminar Tareas", "Importar/Exportar"]
choice = st.sidebar.selectbox("Menú", menu)

db = get_db()

if choice == "Agregar Tarea":
    st.subheader("Agregar Nueva Tarea")
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    if st.button("Agregar"):
        if title:
            add_task(db, title, description)
            st.success("Tarea agregada correctamente.")
        else:
            st.error("El título es obligatorio.")

elif choice == "Listar Tareas":
    st.subheader("Lista de Tareas")
    tasks = list_tasks(db)
    for task in tasks:
        st.write(f"**{task.id}. {task.title}**")
        st.write(f"Descripción: {task.description}")
        st.write(f"Estado: {'✅ Completada' if task.completed else '⏳ Pendiente'}")
        st.write("---")

elif choice == "Marcar Completada":
    st.subheader("📝 Marcar Tarea como Completada")

    tasks = list_tasks(db)
    pending_tasks = [task for task in tasks if not task.completed]

    if pending_tasks:
        selected_task_id = None

        st.write("### Tareas Pendientes")
        for task in pending_tasks:
            with st.expander(f"**{task.title}**", expanded=False):
                st.write(f"📄 **Descripción:** {task.description if task.description else 'No disponible'}")
                if st.button(f"✅ Marcar '{task.title}' como Completada", key=task.id):
                    selected_task_id = task.id

        if selected_task_id:
            mark_completed(db, selected_task_id)
            st.success("Tarea marcada como completada.")
    else:
        st.info("🎉 ¡No hay tareas pendientes!")


elif choice == "Eliminar Tareas":
    st.subheader("🗑️ Eliminar Tareas")

    tasks = list_tasks(db)

    if tasks:
        st.write("### Lista de Tareas")
        for task in tasks:
            status = "✅ Completada" if task.completed else "⏳ Pendiente"

            with st.expander(f"**{task.title}** ({status})", expanded=False):
                st.write(f"📄 **Descripción:** {task.description if task.description else 'No disponible'}")

                if st.button(f"🗑️ Eliminar '{task.title}'", key=f"del_{task.id}"):
                    from crud import delete_task_by_id 
                    if delete_task_by_id(db, task.id):
                        st.success(f"Tarea '{task.title}' eliminada correctamente.")
                    else:
                        st.error(f"No se pudo eliminar la tarea '{task.title}'.")
    else:
        st.info("🎉 ¡No hay tareas disponibles para eliminar!")



elif choice == "Importar/Exportar":
    st.subheader("Importar/Exportar Tareas")
    action = st.radio("Acción", ["Exportar", "Importar"])
    file_path = st.text_input("Ruta del archivo", "tasks.json")

    if action == "Exportar" and st.button("Exportar"):
        export_tasks_to_json(db, file_path)
        st.success(f"Tareas exportadas a {file_path}")

    if action == "Importar" and st.button("Importar"):
        import_tasks_from_json(db, file_path)
        st.success(f"Tareas importadas desde {file_path}")
