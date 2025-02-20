import streamlit as st
from story_puzzles.db import init_db
from story_puzzles.scene.template import SceneTemplate, SceneTemplateTag
from story_puzzles.scene import Scene
from story_puzzles.entity.template import (
    CharacterTemplate, 
    ObjectPropTemplate, 
    LandmarkTemplate,
    CreatureTemplate,
    EntityType,
    BaseEntityTemplate
)
from story_puzzles.ui.types import SelectionState
from story_puzzles.ui.callbacks import on_entity_change, on_template_change

def init_app():
    """Initialize the database connection"""
    init_db()

    # Initialize session state for persistent objects
    if 'scene' not in st.session_state:
        st.session_state.scene = Scene(None)
    if 'template' not in st.session_state:
        st.session_state.template = None
    if 'selections' not in st.session_state:
        st.session_state.selections = {}
        st.session_state.used_entities = {}

def get_entity_options(entity_type: EntityType):
    """Get all entities of a specific type from the database"""
    if entity_type == EntityType.CHARACTER:
        return CharacterTemplate.objects.all()
    elif entity_type == EntityType.OBJECT_PROP:
        return ObjectPropTemplate.objects.all()
    elif entity_type == EntityType.LANDMARK:
        return LandmarkTemplate.objects.all()
    elif entity_type == EntityType.CREATURE:
        return CreatureTemplate.objects.all()
    return []

def scene_template_selector():
    """Render the scene template selector"""
    templates = SceneTemplate.objects.all()
    template_names = [t.name for t in templates]
    selected_template_name = st.selectbox(
        "Choose a scene template:",
        options=template_names,
        key="template_selector",
        on_change=on_template_change
    )
    st.session_state.template = SceneTemplate.objects(name=selected_template_name).first()

def scene_preview():
    """Render the scene preview"""
    st.write("Scene Preview")
    scene_template = st.session_state.template
    scene = Scene(scene_template)

    st.session_state.scene = scene
    scene_description = scene.get_filled_description()
    st.markdown(f"**{scene_description}**")

def render_left_panel():
    """Render the left panel containing the scene template and preview"""
    with st.container():
        st.subheader("Scene Template")
        
        # Scene template selector
        scene_template_selector()
        
        # Scene preview
        scene_preview()

def render_right_panel(template: SceneTemplate, scene: Scene):
    """Render the right panel containing entity selectors"""
    if not template:
        return None
    
    st.subheader("Choose Entities")
    
    # Initialize selection state if not exists
    if 'selection_state' not in st.session_state:
        st.session_state.selection_state = SelectionState({}, {}, scene)
    
    selection_state: SelectionState = st.session_state.selection_state
    
    # Group tags by sentence
    tags_by_sentence = template.get_tags_by_sentence()
    
    # Process each sentence
    for sentence_num, tags in sorted(tags_by_sentence.items()):
        st.markdown(f"**Sentence {sentence_num}**")
        
        for tag in tags:
            # Get available entities
            all_entities = get_entity_options(tag.entity_type)
            
            # Filter out entities used by other tags of the same type
            used_entities = selection_state.used_entities.get(tag.entity_type.value, set())
            available_entities = [e for e in all_entities if e.name not in used_entities or 
                               tag.tag_name in selection_state.selections and 
                               selection_state.selections[tag.tag_name][1].name == e.name]
            
            # Create options dictionary
            entity_options = {str(entity): entity for entity in available_entities}
            
            if entity_options:
                # Get currently selected entity for this tag if it exists
                current_selection = None
                if tag.tag_name in selection_state.selections:
                    current_selection = str(selection_state.selections[tag.tag_name][1])
                
                selected_entity = st.selectbox(
                    f"Choose {tag.entity_type.value} for '{tag.tag_name}':",
                    options=list(entity_options.keys()),
                    key=f"select_{tag.tag_name}",
                    index=list(entity_options.keys()).index(current_selection) if current_selection else 0,
                    on_change=lambda: on_entity_change(tag, entity_options[st.session_state[f"select_{tag.tag_name}"]])
                )
            else:
                st.error(f"No available {tag.entity_type.value} entities for '{tag.tag_name}'")

    if st.button("Reset Selections"):
        selection_state.clear()
        st.rerun()

def on_template_change():
    st.session_state.selections = {}
    st.session_state.used_entities = {}
    st.session_state.scene = Scene(st.session_state.template)

def on_entity_change(tag: SceneTemplateTag, new_entity: BaseEntityTemplate):
    """Handle entity selection changes"""
    selection_state: SelectionState = st.session_state.selection_state
    scene: Scene = st.session_state.scene
    
    # Remove any downstream selections that used the previously selected entity
    if tag.tag_name in selection_state.selections:
        old_tag, old_entity = selection_state.selections[tag.tag_name]
        
        # Find all downstream tags (higher sentence numbers)
        downstream_tags = []
        for other_tag_name, (other_tag, other_entity) in selection_state.selections.items():
            if (other_tag.sentence_num > tag.sentence_num and 
                other_entity.name == old_entity.name):
                downstream_tags.append(other_tag_name)
        
        # Remove downstream selections
        for tag_name in downstream_tags:
            selection_state.remove_selection(tag_name)
    
    # Add new selection
    selection_state.add_selection(tag, new_entity)
    
    # Update scene
    scene.create_entity_by_tag(tag, new_entity)
    
    # Force streamlit to update the preview
    st.rerun()

def main():
    """Main function to run the app"""
    init_app()

    # Layout
    st.set_page_config(layout="wide")
    st.title("Story Scene Creator")
    left_col, right_col = st.columns([1, 3])

    # Left panel (Scene Template)
    with left_col:
        template = render_left_panel()
        
        if template and (not st.session_state.scene or st.session_state.scene.scene_template != template):
            st.session_state.scene = Scene(template)
            st.session_state.template = template
            # Clear selections when template changes
            st.session_state.selections = {}
            st.session_state.used_entities = {}

    # Right panel (Entity Selection)
    with right_col:
        if st.session_state.template:
            render_right_panel(st.session_state.template, st.session_state.scene)

if __name__ == "__main__":
    main() 