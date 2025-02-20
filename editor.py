import streamlit as st
from story_puzzles.db import init_db
from story_puzzles.scene.template import SceneTemplate
from story_puzzles.entity.template import (
    CharacterTemplate, 
    ObjectPropTemplate, 
    LandmarkTemplate,
    EntityType,
    CreatureTemplate
)

def init():
    """Initialize the database connection"""
    init_db()

def main():
    st.title("Story Puzzle Editor")
    init()

    # Sidebar for navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Browse Templates", "Add Template", "Browse Entities", "Add Entity"]
    )

    if page == "Browse Templates":
        st.header("Scene Templates")
        templates = SceneTemplate.objects.all()
        
        for template in templates:
            with st.expander(f"Template: {template.name}"):
                # Create a form for each template
                with st.form(f"template_{template.name}"):
                    new_name = st.text_input("Name", template.name)
                    new_description = st.text_area("Description", template.template_description)
                    
                    if st.form_submit_button("Update"):
                        template.name = new_name
                        template.template_description = new_description
                        template.save()
                        st.success("Template updated!")
                    
                    if st.form_submit_button("Delete", type="secondary"):
                        template.delete()
                        st.success("Template deleted!")
                        st.rerun()

    elif page == "Add Template":
        st.header("Add New Scene Template")
        with st.form("new_template"):
            name = st.text_input("Template Name")
            description = st.text_area("Template Description (Use {type:name} for placeholders)")
            
            if st.form_submit_button("Create Template"):
                if name and description:
                    template = SceneTemplate(
                        name=name,
                        template_description=description
                    ).save()
                    st.success(f"Created template: {template.name}")
                else:
                    st.error("Please fill in all fields")

    elif page == "Browse Entities":
        st.header("Entities")
        entity_type = st.selectbox(
            "Filter by type",
            ["All", "Character", "Object", "Landmark", "Creature"]
        )
        
        if entity_type == "Character" or entity_type == "All":
            st.subheader("Characters")
            for entity in CharacterTemplate.objects.all():
                with st.expander(f"Character: {entity.name}"):
                    with st.form(f"character_{entity.name}"):
                        new_name = st.text_input("Name", entity.name)
                        new_desc = st.text_input("Description", entity.description)
                        
                        # Add states management
                        states_str = st.text_area(
                            "Possible States (one per line)", 
                            "\n".join(entity.possible_states)
                        )
                        
                        if st.form_submit_button("Update"):
                            entity.name = new_name
                            entity.description = new_desc
                            # Parse states from text area
                            entity.possible_states = [s.strip() for s in states_str.split('\n') if s.strip()]
                            entity.save()
                            st.success("Character updated!")
                        
                        if st.form_submit_button("Delete", type="secondary"):
                            entity.delete()
                            st.success("Character deleted!")
                            st.rerun()
        
        if entity_type == "Object" or entity_type == "All":
            st.subheader("Objects")
            for entity in ObjectPropTemplate.objects.all():
                with st.expander(f"Object: {entity.name}"):
                    with st.form(f"object_{entity.name}"):
                        new_name = st.text_input("Name", entity.name)
                        new_desc = st.text_input("Description", entity.description)
                        
                        # Add states management
                        states_str = st.text_area(
                            "Possible States (one per line)", 
                            "\n".join(entity.possible_states)
                        )
                        
                        if st.form_submit_button("Update"):
                            entity.name = new_name
                            entity.description = new_desc
                            # Parse states from text area
                            entity.possible_states = [s.strip() for s in states_str.split('\n') if s.strip()]
                            entity.save()
                            st.success("Object updated!")
                        
                        if st.form_submit_button("Delete", type="secondary"):
                            entity.delete()
                            st.success("Object deleted!")
                            st.rerun()
        
        if entity_type == "Landmark" or entity_type == "All":
            st.subheader("Landmarks")
            for entity in LandmarkTemplate.objects.all():
                with st.expander(f"Landmark: {entity.name}"):
                    with st.form(f"landmark_{entity.name}"):
                        new_name = st.text_input("Name", entity.name)
                        new_desc = st.text_input("Description", entity.description)
                        
                        # Add states management
                        states_str = st.text_area(
                            "Possible States (one per line)", 
                            "\n".join(entity.possible_states)
                        )
                        
                        if st.form_submit_button("Update"):
                            entity.name = new_name
                            entity.description = new_desc
                            # Parse states from text area
                            entity.possible_states = [s.strip() for s in states_str.split('\n') if s.strip()]
                            entity.save()
                            st.success("Landmark updated!")
                        
                        if st.form_submit_button("Delete", type="secondary"):
                            entity.delete()
                            st.success("Landmark deleted!")
                            st.rerun()
        
        if entity_type == "Creature" or entity_type == "All":
            st.subheader("Creatures")
            for entity in CreatureTemplate.objects.all():
                with st.expander(f"Creature: {entity.name}"):
                    with st.form(f"creature_{entity.name}"):
                        new_name = st.text_input("Name", entity.name)
                        new_desc = st.text_input("Description", entity.description)
                        
                        # Add states management
                        states_str = st.text_area(
                            "Possible States (one per line)", 
                            "\n".join(entity.possible_states)
                        )
                        
                        if st.form_submit_button("Update"):
                            entity.name = new_name
                            entity.description = new_desc
                            # Parse states from text area
                            entity.possible_states = [s.strip() for s in states_str.split('\n') if s.strip()]
                            entity.save()
                            st.success("Creature updated!")
                        
                        if st.form_submit_button("Delete", type="secondary"):
                            entity.delete()
                            st.success("Creature deleted!")
                            st.rerun()

    elif page == "Add Entity":
        st.header("Add New Entity")
        with st.form("new_entity"):
            entity_type = st.selectbox(
                "Entity Type",
                ["Character", "Object", "Landmark", "Creature"]
            )
            name = st.text_input("Name")
            description = st.text_input("Description")
            
            # Add states input
            states_str = st.text_area(
                "Possible States (one per line)", 
                "default"  # Default initial state
            )
            
            if st.form_submit_button("Create Entity"):
                if name:
                    # Parse states from text area
                    states = [s.strip() for s in states_str.split('\n') if s.strip()]
                    
                    if entity_type == "Character":
                        entity = CharacterTemplate(
                            name=name, 
                            description=description,
                            possible_states=states
                        ).save()
                    elif entity_type == "Object":
                        entity = ObjectPropTemplate(
                            name=name, 
                            description=description,
                            possible_states=states
                        ).save()
                    elif entity_type == "Landmark":
                        entity = LandmarkTemplate(
                            name=name, 
                            description=description,
                            possible_states=states
                        ).save()
                    elif entity_type == "Creature":
                        entity = CreatureTemplate(
                            name=name, 
                            description=description,
                            possible_states=states
                        ).save()
                    st.success(f"Created {entity_type}: {name}")
                else:
                    st.error("Please fill in the name field")

if __name__ == "__main__":
    main()