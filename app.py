import streamlit as st
from story_puzzles.db import init_db
from story_puzzles.scene.template import SceneTemplate
from story_puzzles.scene import Scene
from story_puzzles.entity.template import (
    CharacterTemplate, 
    ObjectPropTemplate, 
    LandmarkTemplate,
    EntityType
)

def init():
    """Initialize the database connection"""
    init_db()

def get_entity_options(entity_type: EntityType):
    """Get all entities of a specific type from the database"""
    if entity_type == EntityType.CHARACTER:
        return CharacterTemplate.objects.all()
    elif entity_type == EntityType.OBJECT_PROP:
        return ObjectPropTemplate.objects.all()
    elif entity_type == EntityType.LANDMARK:
        return LandmarkTemplate.objects.all()
    return []

def main():
    st.title("Story Scene Creator")
    
    # Initialize database connection
    init()
    
    # Get all available scene templates
    templates = SceneTemplate.objects.all()
    template_names = [t.name for t in templates]
    
    # Scene template selection
    selected_template_name = st.selectbox(
        "Choose a scene template:",
        options=template_names
    )
    
    if selected_template_name:
        # Get the selected template
        selected_template = SceneTemplate.objects(name=selected_template_name).first()
        
        # Display template information
        st.subheader("Template Details")
        st.write(f"Description: {selected_template.template_description}")
        st.write("Template:")
        st.info(selected_template.template)
        
        if st.button("Create Scene"):
            # Create a new scene instance
            scene = Scene(selected_template)
            
            # Get template tags
            template_tags = selected_template.get_template_tags()
            
            st.subheader("Fill in the Scene Elements")
            
            # Create a form for entity selection
            with st.form("entity_selection"):
                selections = {}
                
                # For each template tag, create a dropdown with valid entities
                for tag in template_tags:
                    # Get available entities for this tag type
                    available_entities = get_entity_options(tag.entity_type)
                    entity_options = {str(entity): entity for entity in available_entities}
                    
                    # Create dropdown for this tag
                    selected_entity = st.selectbox(
                        f"Choose {tag.entity_type.value} for '{tag.tag_name}':",
                        options=list(entity_options.keys())
                    )
                    
                    if selected_entity:
                        selections[tag] = entity_options[selected_entity]
                
                # Submit button for the form
                submitted = st.form_submit_button("Create Scene")
                
                if submitted:
                    # Add selected entities to the scene
                    for tag, entity in selections.items():
                        scene.create_entity_by_tag(tag, entity)
                    
                    st.success("Scene created successfully!")
                    # Here you could add more visualization of the created scene

if __name__ == "__main__":
    main() 